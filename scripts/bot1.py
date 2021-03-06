from web3 import Web3
import json
import os
import random
import base58
import binascii

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
accounts = w3.eth.get_accounts()


def _ipfs_to_bytes32(hash_str: str):
    """Ipfs hash is converted into bytes32 format."""
    bytes_array = base58.b58decode(hash_str)
    b = bytes_array[2:]
    return binascii.hexlify(b).decode("utf-8")


def ipfs_to_bytes32(ipfs_hash: str) -> str:
    """bytes32 is converted back into Ipfs hash format."""
    ipfs_hash_bytes32 = _ipfs_to_bytes32(ipfs_hash)
    return w3.toBytes(hexstr=ipfs_hash_bytes32)


EXAMPLE_HASH = ipfs_to_bytes32(
    'QmUEQFgFBpnwmPNY8GBNmCHWBvqak3DaGEvRWDqstZ93kK')
print(EXAMPLE_HASH)

token_address = '0x21E73cfbe1F4196a8D9f80384c29eD39624343ca'
dao_address = '0x3983E6fcB2174c3AD150695cC20F7eBa8eDcc4a9'

with open('./build/contracts/Dao.json') as f:
    dao_file = json.load(f)
    dao_abi = dao_file['abi']


dao = w3.eth.contract(address=dao_address, abi=dao_abi)


def get_status(status_code):
    switch = {0: 'PENDING', 1: 'APPROVED', 2: 'REJECTED'}
    return switch[status_code]


def create_proposal():
    create_proposal_hash = dao.functions.newProposal(
        EXAMPLE_HASH).transact({'from': accounts[0]})
    create_proposal_receipt = w3.eth.wait_for_transaction_receipt(
        create_proposal_hash)
    print(create_proposal_receipt)


def cast_vote(account, vote):
    vote_hash = dao.functions.vote(
        EXAMPLE_HASH, vote).transact({'from': account})
    vote_receipt = w3.eth.wait_for_transaction_receipt(vote_hash)
    print(vote_receipt)


def get_proposal(proposal_hash):
    get_proposal_hash = dao.functions.getProposal(
        proposal_hash).call({'from': accounts[0]})
    print(get_status(get_proposal_hash[-1]))


# vote_hash = dao.functions.vote(EXAMPLE_HASH, 0).transact({'from': accounts[1]})
# vote_receipt = w3.eth.wait_for_transaction_receipt(vote_hash)


#vote_hash = dao.functions.vote(EXAMPLE_HASH, 0).transact({'from': accounts[0]})
#vote_receipt = w3.eth.wait_for_transaction_receipt(vote_hash)
# print(vote_receipt)

create_proposal()
# for account in accounts:
#     vote = random.randint(0, 1)

#     print('casting:', vote)
#     cast_vote(account, vote)
# get_proposal(EXAMPLE_HASH)
