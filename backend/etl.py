import os
import pandas as pd
import hashlib
import json
from encrypt import encrypt_data
from pinata import upload_json_to_pinata  # Import hàm upload từ pinata.py

# Lấy đường dẫn tuyệt đối tới thư mục "backend"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn tuyệt đối tới thư mục data
data_dir = os.path.join(BASE_DIR, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Đường dẫn file CSV
raw_data_path = os.path.join(data_dir, "AI_in_HealthCare_Dataset.csv")

# Đọc dữ liệu từ file CSV bằng Pandas
df = pd.read_csv(raw_data_path)

# Chuyển DataFrame thành chuỗi JSON
data_json = df.to_json(orient="records")

# Tính hash SHA-256 cho chuỗi dữ liệu JSON
data_hash = hashlib.sha256(data_json.encode("utf-8")).hexdigest()
print("Data SHA-256 hash:", data_hash)

# Mã hóa dữ liệu sử dụng AES-256
encrypted_data = encrypt_data(data_json)
print("Encrypted data:", json.dumps(encrypted_data, indent=2))

# Lưu dữ liệu đã mã hóa vào file encrypted_data.json
enc_file_path = os.path.join(data_dir, "encrypted_data.json")
with open(enc_file_path, "w") as f:
    json.dump(encrypted_data, f, indent=2)

# Upload dữ liệu đã mã hóa lên Pinata và lấy IPFS hash
try:
    ipfs_hash = upload_json_to_pinata(encrypted_data)
    print("Uploaded to Pinata, IPFS hash:", ipfs_hash)
except Exception as e:
    print("Upload to Pinata failed:", e)
    ipfs_hash = None

# Lưu data_hash và IPFS hash (nếu có) vào file ipfs_hashes.json
hash_file_path = os.path.join(data_dir, "ipfs_hashes.json")
output = {"data_hash": data_hash}
if ipfs_hash:
    output["ipfs_hash"] = ipfs_hash
with open(hash_file_path, "w") as f:
    json.dump(output, f, indent=2)
