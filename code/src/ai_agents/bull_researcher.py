from ai_agents.base_agent import Agent

class BullResearcher(Agent):
    def generate_argument(self, symbol):
        prompt = f"As a bull researcher, argue why {symbol} is a good investment based on available data."
        return self.llm.generate(prompt)