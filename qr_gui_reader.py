import tkinter as tk
from tkinter import filedialog, messagebox
import json, os, base64, webbrowser
from pyzbar.pyzbar import decode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from datetime import datetime
from PIL import Image

def qr_sec():
    path = filedialog.askopenfilename(filetypes=[("PNG Dosyası", "*.png")])
    if path:
        qr_path.set(path)
        file_label.config(text=os.path.basename(path))

def cozumle():
    file_path = qr_path.get()
    password = parola_entry.get()
    role = role_entry.get().strip().lower()

    if not file_path or not password or not role:
        messagebox.showerror("Eksik Bilgi", "Tüm alanları doldurun.")
        return

    if password != "erzincan24":
        messagebox.showerror("Parola Hatalı", "❌ Hatalı parola!")
        return

    try:
        img = Image.open(file_path)
        decoded = decode(img)
    except:
        messagebox.showerror("Hata", "QR görseli okunamadı.")
        return

    if not decoded:
        messagebox.showerror("Hata", "QR kod verisi çözülemedi.")
        return

    qr_data = json.loads(decoded[0].data.decode("utf-8"))

    try:
        with open("keys/private_key.pem", "rb") as f:
            private_key = RSA.import_key(f.read(), passphrase="Robiko.2429")  # 🛡️ Şifreli anahtar desteği
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(base64.b64decode(qr_data["encrypted_key"]))
    except:
        messagebox.showerror("Hata", "RSA çözümleme başarısız.")
        return

    try:
        enc_data = base64.b64decode(qr_data["encrypted_data"])
        iv = enc_data[:16]
        cipher_data = enc_data[16:]
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted = cipher_aes.decrypt(cipher_data).decode("utf-8")
        pad_len = ord(decrypted[-1])
        json_str = decrypted[:-pad_len]
        veri = json.loads(json_str)
    except:
        messagebox.showerror("Hata", "AES çözümleme başarısız.")
        return

    expires_at = datetime.strptime(veri["expires_at"], "%Y-%m-%dT%H:%M:%S")
    if datetime.now() > expires_at:
        messagebox.showerror("Süre Doldu", f"Bu QR kodun süresi dolmuştu.\nGeçerlilik: {veri['expires_at']}")
        return

    if role != veri["access_role"]:
        messagebox.showerror("Yetki Yok", "Bu veriye erişim yetkiniz yok.")
        return

    if role == "admin":
        html_goster(veri)
    else:
        msg = f"İsim: {veri['name']}\nÜnvan: {veri['title']}\nŞirket: {veri['company']}\nGeçerlilik: {veri['expires_at']}"
        messagebox.showinfo("Sınırlı Görünüm", msg)

    if "file_name" in veri and "file_data" in veri:
        os.makedirs("saved_files", exist_ok=True)
        path = os.path.join("saved_files", veri["file_name"])
        with open(path, "wb") as f:
            f.write(base64.b64decode(veri["file_data"]))
        messagebox.showinfo("Dosya Kaydedildi", f"{veri['file_name']} dosyası indirildi.")

def html_goster(data):
    html = f"""
    <html><head><meta charset='utf-8'><title>Veri</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head><body class="bg-light"><div class="container py-5"><div class="card shadow-lg"><div class="card-body">
    <h2 class="card-title text-center mb-4">🎤 Konuşmacı Bilgileri</h2>
    <p><strong>İsim:</strong> {data['name']}</p>
    <p><strong>Ünvan:</strong> {data['title']}</p>
    <p><strong>Email:</strong> {data['email']}</p>
    <p><strong>Telefon:</strong> {data['phone']}</p>
    <p><strong>Şirket:</strong> {data['company']}</p>
    <p><strong>Konular:</strong> {', '.join(data['topics'])}</p>
    <p><strong>Geçerlilik:</strong> {data['expires_at']}</p>
    <a href="{data['additional_materials']}" target="_blank" class="btn btn-primary">🔗 Drive Bağlantısı</a>
    </div></div></div></body></html>
    """
    with open("decrypted_data.html", "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open(f"file://{os.path.abspath('decrypted_data.html')}")

# === GUI ===
pencere = tk.Tk()
pencere.title("QR Çözümleyici")
pencere.geometry("460x400")
pencere.configure(bg="#f2f2f2")

qr_path = tk.StringVar()

card = tk.Frame(pencere, bg="white", bd=1, relief="solid", padx=30, pady=30)
card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card, text="QR Kod Seç", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
tk.Button(card, text="Gözat", command=qr_sec).pack(pady=3)
file_label = tk.Label(card, text="Henüz seçilmedi", bg="white", fg="gray")
file_label.pack(pady=(0, 10))

tk.Label(card, text="Parola", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
parola_entry = tk.Entry(card, show="*", width=30)
parola_entry.pack(pady=(0, 10))

tk.Label(card, text="Rol (admin/user)", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
role_entry = tk.Entry(card, width=30)
role_entry.pack(pady=(0, 20))

tk.Button(card, text="QR Çöz", command=cozumle, bg="#0d6efd", fg="white",
          font=("Segoe UI", 11, "bold"), padx=10, pady=5).pack()

pencere.mainloop()
