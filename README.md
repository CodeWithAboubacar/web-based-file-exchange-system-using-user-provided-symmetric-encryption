🔐 Secure Web-Based File Exchange System

A project for MSc Cybersecurity & Digital Forensics

📌 Overview

This project implements a secure web-based file exchange system where users can upload, encrypt, download, and decrypt files using their own symmetric encryption keys. The system empowers users with encryption control, ensuring data confidentiality and security in file sharing.

The system is built using Python Flask (backend), MySQL (database), and Fernet encryption from the cryptography library.

🚀 Features

🔑 User-provided symmetric encryption keys for file security

👤 User authentication (login & registration)

📂 Secure file upload, storage, and download

🔒 File encryption & decryption with Fernet

📊 Minimal latency performance confirmed through testing

🌐 Web-based interface (HTML, CSS, Bootstrap)

🛠️ Technologies Used

Backend: Python Flask

Database: MySQL (via SQLAlchemy)

Encryption: Cryptography (Fernet)

Frontend: HTML, CSS, Bootstrap

Version Control: Git & GitHub

📂 Project Structure
secure-file-exchange/
│── app.py              # Main Flask application  
│── requirements.txt    # Dependencies  
│── static/             # CSS, images, JS  
│── templates/          # HTML templates  
│── uploads/            # Encrypted/Decrypted files  
│── database/           # MySQL scripts and schema  

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/YourUsername/secure-file-exchange.git
cd secure-file-exchange


Create a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux  
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Set up MySQL database

Import the schema from /database/schema.sql

Update DB credentials in app.py

Run the application

flask run


Access the app at: http://127.0.0.1:5000/

🔑 Usage

Register or log in to the system

Upload a file and provide your own encryption key

Download the encrypted file securely

Decrypt files locally by re-entering your key

📊 Results & Analysis

✅ Successful encryption & decryption with user-provided keys

🔒 Confidentiality maintained — only correct key grants access

⚡ Performance tests show minimal latency

📌 Future Work

Multi-user file sharing & collaboration

Stronger encryption algorithms (AES, hybrid approaches)

Cloud deployment for scalability

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License
