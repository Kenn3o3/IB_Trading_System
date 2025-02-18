import pandas as pd
import ta

class SMACrossoverStrategy(TradingStrategy):
    def __init__(self, symbol, exchange, risk_manager, short_period=50, long_period=200):
        super().__init__(symbol, exchange, risk_manager)
        self.short_period = short_period
        self.long_period = long_period
        self.historical_data = pd.DataFrame()
        
    def on_bar(self, bar):
        self.historical_data = self.historical_data.append({
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume
        }, ignore_index=True)
        
        if len(self.historical_data) > self.long_period:
            self.historical_data['sma_short'] = ta.trend.sma_indicator(
                self.historical_data['close'], self.short_period)
            self.historical_data['sma_long'] = ta.trend.sma_indicator(
                self.historical_data['close'], self.long_period)
            
            if self._cross_above():
                if self.risk_manager.approve_order(self.symbol, 'BUY'):
                    self._place_order('BUY')
            elif self._cross_below():
                if self.risk_manager.approve_order(self.symbol, 'SELL'):
                    self._place_order('SELL')

    def _cross_above(self):
        return (self.historical_data['sma_short'].iloc[-2] < self.historical_data['sma_long'].iloc[-2] and
                self.historical_data['sma_short'].iloc[-1] > self.historical_data['sma_long'].iloc[-1])

    def _cross_below(self):
        return (self.historical_data['sma_short'].iloc[-2] > self.historical_data['sma_long'].iloc[-2] and
                self.historical_data['sma_short'].iloc[-1] < self.historical_data['sma_long'].iloc[-1])
