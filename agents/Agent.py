from abc import ABC
from web3 import Web3
from utils import get_dao
import time

PROVIDER_URL = 'http://127.0.0.1:8545'


class Agent(ABC):
    def __init__(self, account):
        self.w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
        self.account = account
        self.dao = get_dao()

    @staticmethod
    def get_status(status_code):
        switch = {0: 'PENDING', 1: 'APPROVED', 2: 'REJECTED'}
        return switch[status_code]

    def create_proposal(self, proposal_hash):
        create_proposal_hash = self.dao.functions.newProposal(
            proposal_hash).transact({'from': self.account})
        create_proposal_receipt = self.w3.eth.wait_for_transaction_receipt(
            create_proposal_hash)
        print(create_proposal_receipt)

    def cast_vote(self, proposal_hash, vote):
        vote_hash = self.dao.functions.vote(
            proposal_hash, vote).transact({'from': self.account})
        vote_receipt = self.w3.eth.wait_for_transaction_receipt(vote_hash)
        print(vote_receipt)

    def get_proposal(self, proposal_hash):
        get_proposal_hash = self.dao.functions.getProposal(
            proposal_hash).call({'from': self.account})
        print(self.get_status(get_proposal_hash[-1]))

    def listen_proposals(self, poll_interval=5):
        event_filter = self.dao.events.ProposalCreated.createFilter(
            fromBlock='latest')
        while True:
            for event in event_filter.get_new_entries():
                print(event)
            time.sleep(poll_interval)
