from ai_agents.trader import Trader
import torch
import torch.nn as nn

class TradingDQN(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3)  # [HOLD, BUY, SELL]
        )
    
    def forward(self, x):
        return self.net(x)

class RLTrader(Trader):
    def __init__(self, name, blackboard):
        super().__init__(name, blackboard)
        self.model = TradingDQN(input_size=4)  # Simplified state size

    def get_state(self, symbol):
        tech_report = self.blackboard.get_report("Technical Analyst") or {}
        sentiment_report = self.blackboard.get_report("Sentiment Analyst") or {}
        debate_report = self.blackboard.get_report("Debate") or {}
        state = [
            tech_report.get("sma_short", 0),
            tech_report.get("sma_long", 0),
            sentiment_report.get("sentiment", 0),
            1 if debate_report.get("outcome") == "bullish" else -1 if debate_report.get("outcome") == "bearish" else 0
        ]
        return torch.FloatTensor(state)

    def make_decision(self, symbol, debate_outcome):
        state = self.get_state(symbol)
        with torch.no_grad():
            q_values = self.model(state)
        action = torch.argmax(q_values).item()
        self.decision = ["hold", "buy", "sell"][action]
        self.communicate({"decision": self.decision})