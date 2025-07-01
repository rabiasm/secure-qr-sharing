from Crypto.PublicKey import RSA
import os

os.makedirs("keys", exist_ok=True)

key = RSA.generate(2048)

with open("keys/private_key.pem", "wb") as priv_file:
    priv_file.write(key.export_key())

with open("keys/public_key.pem", "wb") as pub_file:
    pub_file.write(key.publickey().export_key())

print("✅ RSA anahtarları başarıyla oluşturuldu.")
