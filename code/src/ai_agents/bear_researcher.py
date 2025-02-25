from ai_agents.base_agent import Agent

class BearResearcher(Agent):
    def generate_argument(self, symbol):
        prompt = f"As a bear researcher, argue why {symbol} is not a good investment based on available data."
        return self.llm.generate(prompt)