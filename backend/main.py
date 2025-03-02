from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from blockchain import store_hash_on_chain, verify_hash_on_chain
from encrypt import encrypt_data, decrypt_data
from pinata import upload_json_to_pinata  # Import hàm upload từ pinata.py
import uvicorn

app = FastAPI()

# Cấu hình CORS để cho phép frontend truy cập
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.6:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa model cho payload của endpoint /storeHash
class HashPayload(BaseModel):
    hash_value: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Blockchain Data Provenance API"}

@app.post("/storeHash")
def store_hash(payload: HashPayload):
    """
    Endpoint để lưu hash dữ liệu lên blockchain.
    Nhận JSON body theo định dạng: { "hash_value": "0x..." }
    """
    try:
        tx_hash = store_hash_on_chain(payload.hash_value)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/verifyHash/{hash_value}")
def verify_hash(hash_value: str):
    """
    Endpoint để kiểm tra hash dữ liệu
    """
    try:
        exists = verify_hash_on_chain(hash_value)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint mới: Upload dữ liệu lên Pinata
@app.post("/uploadToPinata")
def upload_to_pinata_endpoint(data: dict = Body(...)):
    """
    Endpoint để upload một đối tượng JSON lên Pinata.
    Nhận JSON body và trả về IPFS hash.
    """
    try:
        ipfs_hash = upload_json_to_pinata(data)
        return {"ipfs_hash": ipfs_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Hàm main để chạy server uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
