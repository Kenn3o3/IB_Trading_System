import numpy as np

class AdaptivePositionSizer:
    def __init__(self, volatility_lookback=20):
        self.volatility_lookback = volatility_lookback
        
    def calculate_size(self, historical_data, current_price):
        # Calculate volatility-adjusted position size
        returns = np.diff(np.log(historical_data))
        volatility = np.std(returns[-self.volatility_lookback:])
        return min(0.2 / (volatility + 1e-8), 0.05)  # Cap at 5% account size