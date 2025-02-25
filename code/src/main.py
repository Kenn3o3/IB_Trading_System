from apscheduler.schedulers.blocking import BlockingScheduler
from ibkr_client.ibkr_api import IBKRClient, load_config
from ibkr_client.data_pipeline import DataPipeline
from ai_agents.fundamental_analyst import FundamentalAnalyst
from ai_agents.sentiment_analyst import SentimentAnalyst
from ai_agents.technical_analyst import TechnicalAnalyst
from ai_agents.bull_researcher import BullResearcher
from ai_agents.bear_researcher import BearResearcher
from ai_agents.debate import Debate
from ai_agents.conservative_trader import ConservativeTrader
from ai_agents.aggressive_trader import AggressiveTrader
from ai_agents.rl_trader import RLTrader
from ai_agents.ensemble_strategy import ensemble_decision
from ai_agents.blackboard import Blackboard
from risk_management.risk_manager import RiskManager
from utils.market_hours import MarketHoursChecker
from ai_agents.base_agent import Agent

def main():
    config = load_config()
    ibkr_client = IBKRClient()
    data_pipeline = DataPipeline()
    blackboard = Blackboard()
    market_hours = MarketHoursChecker()

    # Initialize agents
    fundamental_analyst = FundamentalAnalyst("Fundamental Analyst", blackboard)
    sentiment_analyst = SentimentAnalyst("Sentiment Analyst", blackboard)
    technical_analyst = TechnicalAnalyst("Technical Analyst", blackboard)
    bull_researcher = BullResearcher("Bull Researcher", blackboard)
    bear_researcher = BearResearcher("Bear Researcher", blackboard)
    facilitator = Agent("Facilitator", blackboard)
    trader_agents = [
        ConservativeTrader("Conservative Trader", blackboard),
        AggressiveTrader("Aggressive Trader", blackboard),
        RLTrader("RL Trader", blackboard)
    ]
    risk_manager = RiskManager(ibkr_client, config['risk_parameters'])

    # Subscribe to market data for all symbols at startup
    for symbol in config['stocks']['NorthAmerica']:
        ibkr_client.subscribe_market_data(symbol)

    scheduler = BlockingScheduler()
    for symbol in config['stocks']['NorthAmerica']:
        scheduler.add_job(
            trading_cycle,
            'cron',
            day_of_week='mon-fri',
            hour='*',
            minute='*/5',
            args=[symbol, ibkr_client, data_pipeline, market_hours, blackboard, fundamental_analyst, sentiment_analyst, technical_analyst, bull_researcher, bear_researcher, facilitator, trader_agents, risk_manager]
        )
    scheduler.start()

def trading_cycle(symbol, ibkr_client, data_pipeline, market_hours, blackboard, fundamental_analyst, sentiment_analyst, technical_analyst, bull_researcher, bear_researcher, facilitator, trader_agents, risk_manager):
    if not market_hours.is_market_open('SMART'):
        print(f"Market closed for {symbol}.")
        return

    # Fetch data
    historical_data = data_pipeline.fetch_historical_data(symbol, "30 D", "5 mins")
    news = data_pipeline.fetch_news(symbol, "2024-01-01", "2024-12-31")
    social_media = data_pipeline.fetch_social_media(symbol, "2024-01-01", "2024-12-31")
    financials = data_pipeline.fetch_financial_statements(symbol)
    current_price = ibkr_client.get_current_price(symbol)
    if current_price is None:
        print(f"Unable to fetch current price for {symbol}.")
        return

    # Analysts process data
    fundamental_analyst.analyze(financials)
    sentiment_analyst.analyze(news + social_media)
    technical_analyst.analyze(historical_data)

    # Conduct debate
    debate = Debate(bull_researcher, bear_researcher, facilitator, blackboard)
    debate_outcome = debate.conduct_debate(symbol)

    # Traders decide
    for trader in trader_agents:
        trader.make_decision(symbol, debate_outcome)

    # Ensemble decision
    trader_decisions = [trader.blackboard.get_report(trader.name)["decision"] for trader in trader_agents]
    final_decision = ensemble_decision(trader_decisions)

    # Risk management and execution
    closes = [bar['close'] for bar in historical_data]
    approved, shares = risk_manager.approve_order(symbol, final_decision.upper(), closes, current_price)
    if final_decision != "hold" and approved:
        ibkr_client.place_order(symbol, final_decision.upper(), shares)
        print(f"Executed {final_decision} order for {symbol} with {shares} shares.")
    else:
        print(f"No trade executed for {symbol}.")

if __name__ == "__main__":
    main()