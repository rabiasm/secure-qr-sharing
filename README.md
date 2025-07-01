# 🔐 Secure QR Sharing System (AES + RSA + GUI)

A secure, GUI-based system that enables encrypted data sharing through QR codes. Designed with AES for data encryption and RSA for key security, this system provides an intuitive interface for encrypting, storing, and reading QR codes that contain protected data.

Developed as a graduation project by **Rabia SÜME**, this tool integrates cryptographic techniques into a user-friendly environment — ideal for sharing sensitive information through printed or digital QR codes.

---

## ✨ Features

- 🔒 AES Encryption for secure data
- 🔑 RSA Encryption for secure key exchange
- 📁 Embed files (text, PDF, image) via Base64
- 📸 Generate and read QR codes
- 🧑‍💻 GUI for both encryption and decryption
- 🛡️ Password & role-based access control
- ⏳ Time-limited QR codes
- 🌐 HTML visualization of decrypted output

---

## 🧠 How It Works

1. Input or select a file through the GUI
2. Data is encrypted with AES
3. AES key is encrypted with RSA public key
4. Encrypted data + key are encoded into a QR code
5. QR is shared
6. On receiving, the GUI decodes the QR
7. RSA private key decrypts AES key, and data is recovered
8. Output is shown as an HTML page

---

## 🗂️ Project Structure

```
secure_qr_gui/
├── qr_gui_encryptor.py              # GUI for encryption
├── qr_gui_reader.py                 # GUI for decryption
├── RSA_key_generator.py             # RSA key generator
├── RSA_key_generator_encrypted.py   # Encrypted RSA key version
├── encrypted_qr.png                 # Sample QR
├── decrypted_data.html              # Output file
├── dnm.txt                          # Example input
├── keys/                            # RSA keys
├── saved_files/                     # Embedded encrypted files
└── .gitignore
```

---

## 🛠️ Installation

```bash
pip install qrcode pycryptodome pillow
```

✅ Python 3.8+ recommended  
✅ `tkinter` comes with Python (usually preinstalled)

---

## 🚀 Usage

### Start Encryption GUI:
```bash
python qr_gui_encryptor.py
```

### Start Decryption GUI:
```bash
python qr_gui_reader.py
```

---

## 📌 Use Cases

- 📁 Secure file transfer
- 🏥 Health data sharing
- 🏢 Corporate document exchange
- 📧 QR email attachments
- 🕒 Expiring or time-limited data access

---

## 🔮 Future Ideas

- Mobile scanning app
- Cloud-based QR & key management
- Login system
- Digital signature verification
- Scan logs & tracking

---

## 🧑‍🎓 Author

Created by **Rabia SÜME**  
Graduation Project — *Secure Information Sharing via QR Codes with AES-RSA and GUI Integration*

---

## 📄 License

Licensed under the MIT License.
