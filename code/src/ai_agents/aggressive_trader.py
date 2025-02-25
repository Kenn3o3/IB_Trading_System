from ai_agents.trader import Trader

class AggressiveTrader(Trader):
    def make_decision(self, symbol, debate_outcome):
        sentiment_report = self.blackboard.get_report("Sentiment Analyst")
        if debate_outcome == "bullish" or sentiment_report.get("sentiment") > 0:
            self.decision = "buy"
        else:
            self.decision = "sell"
        self.communicate({"decision": self.decision})