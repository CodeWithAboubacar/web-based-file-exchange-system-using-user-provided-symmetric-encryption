from flask import Flask, render_template, request, redirect, send_file, flash, send_from_directory, session, url_for
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os
import pandas as pd
import shutil


app = Flask(__name__)
app.secret_key = 'secret_key'   #Needed for flashing messages

# Dummy users 
USERS = {

}

# Directories
UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted'
DECRYPTED_FOLDER = 'decrypted'
SHARED_FOLDER = 'shared'

for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER, SHARED_FOLDER]:
    os.makedirs(folder, exist_ok=True)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash(f"Welcome, {username}!")
            return redirect('/')
        else:
            flash('❌ Invalid username or password')
    return render_template('login.html')

# Home page
@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out.")
    return redirect('/login')

# Encrypt and store in shared/
@app.route('/upload_to_shared', methods=['POST'])
def upload_to_shared():
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect('/')

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Encrypt
    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open(filepath, 'rb') as f:
        encrypted = fernet.encrypt(f.read())

    encrypted_filename = filename + '.enc'
    encrypted_path = os.path.join(SHARED_FOLDER, encrypted_filename)
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)

    return render_template('result.html',
                           key=key.decode(),
                           download_link=url_for('download_file', filename=encrypted_filename, folder='shared'))

# Download route (shared files)
@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    path = os.path.join(folder, filename)
    return send_file(path, as_attachment=True)

# Show list of shared encrypted files
@app.route('/shared')
def shared_files():
    files = [f for f in os.listdir(SHARED_FOLDER) if f.endswith('.enc')]
    return render_template('shared.html', files=files)

# Decrypt shared file
@app.route('/decrypt_shared', methods=['POST'])
def decrypt_shared():
    filename = request.form['filename']
    key = request.form['key'].encode()

    fernet = Fernet(key)
    encrypted_path = os.path.join(SHARED_FOLDER, filename)
    decrypted_path = os.path.join(DECRYPTED_FOLDER, filename.replace('.enc', ''))

    try:
        with open(encrypted_path, 'rb') as f:
            decrypted_data = fernet.decrypt(f.read())

        with open(decrypted_path, 'wb') as f:
            f.write(decrypted_data)

        # Try to preview if it's CSV
        preview_data = None
        if decrypted_path.endswith('.csv'):
            df = pd.read_csv(decrypted_path)
            preview_data = df.head().to_html(classes='table table-bordered')

        return render_template('decrypted.html',
                               filename=filename.replace('.enc', ''),
                               preview=preview_data)

    except Exception as e:
        flash(f'Decryption failed: {str(e)}')
        return redirect('/shared')

@app.route('/reset')
def reset_data():
    for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER, SHARED_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    flash("✅ All data has been cleared.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


