import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")

def upload_json_to_pinata(json_data: dict) -> str:
    """
    Upload một đối tượng JSON lên Pinata và trả về IPFS hash (CID).
    """
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    if response.status_code == 200:
        ipfs_hash = response.json().get("IpfsHash")
        return ipfs_hash
    else:
        raise Exception(f"Failed to upload to Pinata: {response.text}")
