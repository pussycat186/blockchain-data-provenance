import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Sử dụng WEB3_PROVIDER_URL từ file .env
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not WEB3_PROVIDER_URL or not CONTRACT_ADDRESS or not PRIVATE_KEY:
    raise EnvironmentError("Vui lòng thiết lập WEB3_PROVIDER_URL, CONTRACT_ADDRESS, và PRIVATE_KEY trong file .env")

w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

if not w3.is_connected():
    raise ConnectionError("Không thể kết nối tới blockchain tại URL: " + WEB3_PROVIDER_URL)

# ABI của contract, giữ nguyên
ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "_hash", "type": "bytes32"}],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "_hash", "type": "bytes32"}],
        "name": "verifyHash",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Sử dụng hàm to_checksum_address của Web3.py v6
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

def store_hash_on_chain(hash_value: str):
    if not hash_value.startswith("0x"):
        hash_value = "0x" + hash_value

    account = w3.eth.account.from_key(PRIVATE_KEY)
    nonce = w3.eth.get_transaction_count(account.address)
    
    tx = contract.functions.storeHash(Web3.to_bytes(hexstr=hash_value)).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 300000,
        'gasPrice': w3.to_wei(10, 'gwei'),
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.transaction_hash.hex()

def verify_hash_on_chain(hash_value: str):
    """
    Kiểm tra hash có tồn tại trên blockchain hay không.
    """
    if not hash_value.startswith("0x"):
        hash_value = "0x" + hash_value
    return contract.functions.verifyHash(Web3.to_bytes(hexstr=hash_value)).call()
