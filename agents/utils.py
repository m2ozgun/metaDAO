from web3 import Web3
import json
import base58
import binascii
from web3.auto import w3


def get_dao():
    token_address = '0x21E73cfbe1F4196a8D9f80384c29eD39624343ca'
    dao_address = '0x3983E6fcB2174c3AD150695cC20F7eBa8eDcc4a9'

    with open('./build/contracts/Dao.json') as f:
        dao_file = json.load(f)
        dao_abi = dao_file['abi']

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    dao = w3.eth.contract(address=dao_address, abi=dao_abi)
    return dao


def _ipfs_to_bytes32(hash_str: str):
    """Ipfs hash is converted into bytes32 format."""
    bytes_array = base58.b58decode(hash_str)
    b = bytes_array[2:]
    return binascii.hexlify(b).decode("utf-8")


def ipfs_to_bytes32(ipfs_hash: str) -> str:
    """bytes32 is converted back into Ipfs hash format."""
    ipfs_hash_bytes32 = _ipfs_to_bytes32(ipfs_hash)
    return w3.toBytes(hexstr=ipfs_hash_bytes32)


def bytes32_to_ipfs(bytes_array):
    """Convert bytes_array into IPFS hash format."""
    merge = w3.toBytes(hexstr='1220') + bytes_array
    return base58.b58encode(merge).decode("utf-8")
