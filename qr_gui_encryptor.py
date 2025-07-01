import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json, base64, os, time, re
from datetime import datetime, timedelta
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import qrcode
import psycopg2

def dosya_sec():
    path = filedialog.askopenfilename()
    if path:
        dosya_path.set(path)
        dosya_label.config(text=os.path.basename(path))

def qr_olustur():
    file_path = dosya_path.get()
    role = role_var.get()
    try:
        sure = int(sure_var.get())
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir süre girin (saniye cinsinden).")
        return

    if not file_path or role not in ["admin", "user"]:
        messagebox.showerror("Hata", "Dosya ve rol seçmelisiniz.")
        return

    try:
        with open(file_path, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode("utf-8")
    except:
        messagebox.showerror("Hata", "Dosya okunamadı.")
        return

    file_name_raw = os.path.basename(file_path)
    file_name = re.sub(r'[^A-Za-z0-9_.-]', '_', file_name_raw)
    expires_at_time = (datetime.now() + timedelta(seconds=sure)).strftime("%Y-%m-%dT%H:%M:%S")

    speaker_info = {
        "name": "John Doe",
        "title": "Keynote Speaker",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "company": "Example Corp.",
        "topics": ["Technology", "Innovation", "Business Growth"],
        "additional_materials": "https://drive.google.com/drive/u/0/folders/17iDjIM3clHZlVdNxDjyOhyLkdXjyh_77",
        "expires_at": expires_at_time,
        "access_role": role,
        "file_name": file_name,
        "file_data": encoded_file
    }

    json_data = json.dumps(speaker_info)

    aes_key = get_random_bytes(16)
    aes_start = time.perf_counter()

    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    iv = cipher_aes.iv
    pad_len = 16 - (len(json_data) % 16)
    padded_data = json_data + chr(pad_len) * pad_len
    encrypted_data = cipher_aes.encrypt(padded_data.encode())
    combined_encrypted = iv + encrypted_data
    encrypted_data_b64 = base64.b64encode(combined_encrypted).decode()

    aes_duration = round((time.perf_counter() - aes_start) * 1000, 2)

    with open("keys/public_key.pem", "rb") as f:
        public_key = RSA.import_key(f.read())

    rsa_start = time.perf_counter()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    rsa_duration = round((time.perf_counter() - rsa_start) * 1000, 2)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

    payload = {
        "encrypted_data": encrypted_data_b64,
        "encrypted_key": encrypted_key_b64
    }

    payload_str = json.dumps(payload)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payload_str)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save("encrypted_qr.png")
    img.show()

    # ✅ Veritabanı Kayıt (qr_logs tablosuna)
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Robiko.2429",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        print("📡 Veritabanına bağlanıldı.")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS qr_logs (
            id SERIAL PRIMARY KEY,
            file_name TEXT,
            role TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            aes_duration REAL,
            rsa_duration REAL,
            file_path TEXT,
            qr_image_path TEXT
        )
        """)

        cur.execute("""
        INSERT INTO qr_logs (file_name, role, expires_at, aes_duration, rsa_duration, file_path, qr_image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            file_name,
            role,
            expires_at_time,
            aes_duration,
            rsa_duration,
            file_name,
            "encrypted_qr.png"
        ))

        conn.commit()
        cur.close()
        conn.close()
        print("📤 Veri eklendi.")

    except Exception as e:
        messagebox.showerror("Veritabanı Hatası", f"❌ Veritabanına yazılamadı:\n{e}")
        print("❌ Veritabanı Hatası:", e)

    messagebox.showinfo("Başarılı", "✅ QR kod oluşturuldu ve veritabanına kaydedildi.")

    print("✅ AES Süre:", aes_duration, "ms")
    print("✅ RSA Süre:", rsa_duration, "ms")
    print("✅ Dosya:", file_name)
    print("✅ Rol:", role)
    print("✅ Geçerlilik:", expires_at_time)

# === GUI Arayüzü ===
pencere = tk.Tk()
pencere.title("QR Kod Oluşturucu")
pencere.geometry("520x420")
pencere.configure(bg="#f2f2f2")

dosya_path = tk.StringVar()
role_var = tk.StringVar(value="user")
sure_var = tk.StringVar(value="60")

card = tk.Frame(pencere, bg="white", bd=1, relief="solid", padx=30, pady=30)
card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card, text="Dosya Seç", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
tk.Button(card, text="Gözat", command=dosya_sec).pack()
dosya_label = tk.Label(card, text="Henüz dosya seçilmedi", bg="white", fg="gray")
dosya_label.pack(pady=(0, 10))

tk.Label(card, text="Rol Seç (admin/user)", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
ttk.Combobox(card, values=["admin", "user"], textvariable=role_var, state="readonly").pack(pady=(0, 10))

tk.Label(card, text="Süre (saniye)", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
tk.Entry(card, textvariable=sure_var, width=30).pack(pady=(0, 20))

tk.Button(card, text="QR Kod Oluştur", command=qr_olustur,
          bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), padx=10, pady=5).pack()

pencere.mainloop()
