import os
import base64
import json
from Crypto.Cipher import AES
from dotenv import load_dotenv

load_dotenv()  # Tải các biến môi trường từ file .env

# Lấy giá trị AES_KEY từ biến môi trường và giải mã từ base64 thành bytes
AES_KEY_BASE64 = os.getenv("AES_KEY")
if not AES_KEY_BASE64:
    raise EnvironmentError("Vui lòng thiết lập AES_KEY trong file .env")
KEY = base64.b64decode(AES_KEY_BASE64)  # KEY sẽ có độ dài 32 byte nếu AES_KEY là mã hóa của 32 byte

def encrypt_data(data_str: str) -> dict:
    """
    Mã hóa chuỗi dữ liệu (data_str) bằng AES-256 ở chế độ EAX.
    Trả về ciphertext và nonce.
    """
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data_str.encode('utf-8'))
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(cipher.nonce).decode()
    }

def decrypt_data(encrypted: dict) -> str:
    """
    Giải mã dữ liệu đã mã hóa.
    """
    nonce = base64.b64decode(encrypted["nonce"])
    ciphertext = base64.b64decode(encrypted["ciphertext"])
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')

# Test
if __name__ == "__main__":
    sample = "Dữ liệu nhạy cảm"
    encrypted_dict = encrypt_data(sample)
    print("Encrypted:", json.dumps(encrypted_dict, indent=2))
    decrypted_str = decrypt_data(encrypted_dict)
    print("Decrypted:", decrypted_str)
