from brownie import Dao, Token, accounts


def main():
    print(accounts)
    token = Token.at('0x6cE28e607A0A47d7634E0e4ed39EC4ecC66ABde6')
    print(token)
