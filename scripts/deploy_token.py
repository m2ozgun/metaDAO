from brownie import Token, Dao, Wei, accounts
from web3 import Web3

def main():
    token = Token.deploy({'from': accounts[0]})
    dao = Dao.deploy(token, {'from': accounts[0]})
    for account in accounts:
        token.transfer(account, Wei('1 ether'))
        token.approve(dao.address, Wei('0.1 ether'), {'from': account})
        dao.deposit(Wei('0.01 ether'), {'from': account})
    print(len(Dao))
