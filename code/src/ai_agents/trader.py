from ai_agents.base_agent import Agent

class Trader(Agent):
    def make_decision(self, symbol, debate_outcome):
        raise NotImplementedError