import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# Adjust imports to match your folder structure
from ibkr_client.ibkr_api import IBKRClient, load_config
from strategies.sma_crossover import SMACrossoverStrategy
from risk_management.risk_manager import RiskManager
from utils.market_hours import MarketHoursChecker

def main():
    config = load_config()
    ibkr_client = IBKRClient()
    account_data = ibkr_client.get_account_data()
    print("=== FULL ACCOUNT DATA ===")
    for k, v in account_data.items():
        print(f"{k}: {v}")
    print("=========================")
    risk_manager = RiskManager(ibkr_client, config['risk_parameters'])
    market_hours = MarketHoursChecker()
    config['stocks'] = {"NorthAmerica": ["NVDA"]}
    strategies = []
    for region, symbols in config['stocks'].items():
        exchange = 'SMART' if region == 'NorthAmerica' else 'SEHK'
        for symbol in symbols:  # Correct: use current region's symbols
            strategy = SMACrossoverStrategy(
                symbol=symbol,
                exchange=exchange,  # Pass exchange code (e.g., 'SMART')
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
    try:
        if market_hours.is_market_open(strategy.exchange):
            print(f"Market open for {strategy.symbol}. Fetching data...")
            bars = ibkr_client.get_realtime_bars(strategy.symbol)
            for bar in bars:
                strategy.on_bar(bar)
    except Exception as e:
        print(f"Error in strategy_check: {e}")


if __name__ == "__main__":
    main()