from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    def __init__(self, symbol, exchange, risk_manager):
        self.symbol = symbol
        self.exchange = exchange
        self.risk_manager = risk_manager
        
    @abstractmethod
    def on_bar(self, bar):
        pass