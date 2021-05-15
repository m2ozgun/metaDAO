import multiprocessing
from RandomAgent import RandomAgent
from web3 import Web3
import time
PROVIDER_URL = 'http://127.0.0.1:8545'


def spawn_agent(input_queue):
    inputs = input_queue.get()
    agent = inputs['Agent']
    account = inputs['Account']

    agent = RandomAgent(account)
    agent.get_proposal(
        '0x1362237400400000000000000000000000000000000000000000000000000000')
    agent.listen_proposals()


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
    for i in range(len(accounts)):
        agent_inputs = {'Agent': i, 'Account': accounts[i]}
        input_queue.put(agent_inputs)
    time.sleep(2)


if __name__ == '__main__':
    master()
