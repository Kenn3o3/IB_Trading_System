from ai_agents.bull_researcher import BullResearcher
from ai_agents.bear_researcher import BearResearcher

class Debate:
    def __init__(self, bull, bear, facilitator, blackboard):
        self.bull = bull
        self.bear = bear
        self.facilitator = facilitator
        self.blackboard = blackboard

    def conduct_debate(self, symbol):
        bull_arg = self.bull.generate_argument(symbol)
        bear_arg = self.bear.generate_argument(symbol)
        prompt = f"Evaluate these arguments:\nBull: {bull_arg}\nBear: {bear_arg}\nDecide: BULLISH/NEUTRAL/BEARISH."
        decision = self.facilitator.llm.generate(prompt)
        outcome = "bullish" if "BULLISH" in decision else "bearish" if "BEARISH" in decision else "neutral"
        self.blackboard.post_report("Debate", {"outcome": outcome})
        return outcome