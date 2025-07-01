from Crypto.PublicKey import RSA
import os

# Şifre olarak kullanmak istediğin parolayı yaz
parola = "Robiko.2429"

# RSA anahtarı oluştur
anahtar = RSA.generate(2048)

# Özel anahtarı şifreli kaydet (parola ile koruma)
private_key = anahtar.export_key(
    passphrase=parola,
    pkcs=8,
    protection="scryptAndAES128-CBC"
)

# Genel anahtar
public_key = anahtar.publickey().export_key()

# keys klasörü oluştur (varsa geç)
os.makedirs("keys", exist_ok=True)

# Dosyalara yaz
with open("keys/private_key.pem", "wb") as f:
    f.write(private_key)

with open("keys/public_key.pem", "wb") as f:
    f.write(public_key)

print("✅ Şifreli RSA anahtarları oluşturuldu.")
