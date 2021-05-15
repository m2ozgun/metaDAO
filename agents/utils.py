from web3 import Web3
import json

def get_dao():
    token_address = '0x21E73cfbe1F4196a8D9f80384c29eD39624343ca'
    dao_address = '0x3983E6fcB2174c3AD150695cC20F7eBa8eDcc4a9'

    with open('./build/contracts/Dao.json') as f:
        dao_file = json.load(f)
        dao_abi = dao_file['abi']

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    dao = w3.eth.contract(address=dao_address, abi=dao_abi)
    return dao
