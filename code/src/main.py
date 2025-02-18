import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from ibkr_client import IBKRClient
from strategies import SMACrossoverStrategy
from risk_management import RiskManager
from utils.market_hours import MarketHoursChecker

def main():
    config = load_config()  # Implement config loading
    ibkr_client = IBKRClient()
    risk_manager = RiskManager(ibkr_client, config['risk_parameters'])
    market_hours = MarketHoursChecker()
    
    strategies = []
    # Initialize strategies for all stocks
    for region, symbols in config['stocks'].items():
        exchange = 'SMART' if region == 'NorthAmerica' else 'SEHK'
        for symbol in symbols:
            strategy = SMACrossoverStrategy(
                symbol=symbol,
                exchange=exchange,
                risk_manager=risk_manager
            )
            strategies.append(strategy)
    
    scheduler = BlockingScheduler()
    for strategy in strategies:
        scheduler.add_job(
            strategy_check,
            'cron',
            day_of_week='mon-fri',
            hour='*',
            minute='*/5',
            args=[strategy, market_hours, ibkr_client]
        )
    scheduler.start()

def strategy_check(strategy, market_hours, ibkr_client):
    if market_hours.is_market_open(strategy.exchange):
        # Get latest market data
        bars = ibkr_client.get_realtime_bars(strategy.symbol)
        for bar in bars:
            strategy.on_bar(bar)

if __name__ == "__main__":
    main()