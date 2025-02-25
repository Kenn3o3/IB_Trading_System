from ai_agents.trader import Trader

class ConservativeTrader(Trader):
    def make_decision(self, symbol, debate_outcome):
        tech_report = self.blackboard.get_report("Technical Analyst")
        if debate_outcome == "bullish" and tech_report.get("signal") == "buy":
            self.decision = "buy"
        else:
            self.decision = "hold"
        self.communicate({"decision": self.decision})