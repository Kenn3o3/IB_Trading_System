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

class RLAgent:
    def __init__(self, symbol):
        self.model = TradingDQN(input_size=14)  # Technical features + sentiment
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.0001)
        
    def decide_action(self, state):
        with torch.no_grad():
            q_values = self.model(torch.FloatTensor(state))
        return torch.argmax(q_values).item()