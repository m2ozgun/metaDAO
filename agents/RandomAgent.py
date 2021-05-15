from Agent import Agent


class RandomAgent(Agent):
    def __init__(self, account):
        super().__init__(account)


if __name__ == "__main__":
    agent = RandomAgent('0xEaed2042ba922e8e26F8D7bdBCADe131Cbb40f45')
    agent.get_proposal(
        '0x1362237400400000000000000000000000000000000000000000000000000000')
    agent.listen_proposals()