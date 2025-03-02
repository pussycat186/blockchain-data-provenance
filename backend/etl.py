import os
import pandas as pd
import hashlib
import json
from encrypt import encrypt_data

# Lấy đường dẫn tuyệt đối tới thư mục "backend"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn tuyệt đối tới thư mục data
data_dir = os.path.join(BASE_DIR, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Đường dẫn file CSV
raw_data_path = os.path.join(data_dir, "AI_in_HealthCare_Dataset.csv")

df = pd.read_csv(raw_data_path)

data_json = df.to_json(orient="records")
data_hash = hashlib.sha256(data_json.encode("utf-8")).hexdigest()
print("Data SHA-256 hash:", data_hash)

encrypted_data = encrypt_data(data_json)
print("Encrypted data:", json.dumps(encrypted_data, indent=2))

# Lưu dữ liệu đã mã hóa
enc_file_path = os.path.join(data_dir, "encrypted_data.json")
with open(enc_file_path, "w") as f:
    json.dump(encrypted_data, f, indent=2)

# Lưu hash
hash_file_path = os.path.join(data_dir, "ipfs_hashes.json")
with open(hash_file_path, "w") as f:
    json.dump({"data_hash": data_hash}, f, indent=2)
