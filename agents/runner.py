import multiprocessing
from RandomAgent import RandomAgent
from web3 import Web3

PROVIDER_URL = 'http://127.0.0.1:8545'


def spawn_agent(input_queue):
    account = input_queue.get()


def master():

    input_queue = multiprocessing.Queue()
    workers = []

    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
    accounts = w3.eth.get_accounts()

    # Create workers.
    for _ in range(len(accounts)):
        p = multiprocessing.Process(target=spawn_agent, args=(input_queue, ))
        workers.append(p)
        p.start()

    # Distribute work.
    for account in accounts:
        input_queue.put(account)


if __name__ == '__main__':
    master()
