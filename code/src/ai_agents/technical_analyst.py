from ai_agents.base_agent import Agent
import pandas as pd
import ta

class TechnicalAnalyst(Agent):
    def analyze(self, data):
        df = pd.DataFrame(data)
        df['sma_short'] = ta.trend.sma_indicator(df['close'], window=50)
        df['sma_long'] = ta.trend.sma_indicator(df['close'], window=200)
        signal = "buy" if df['sma_short'].iloc[-1] > df['sma_long'].iloc[-1] else "sell"
        self.communicate({
            "signal": signal,
            "sma_short": df['sma_short'].iloc[-1],
            "sma_long": df['sma_long'].iloc[-1]
        })