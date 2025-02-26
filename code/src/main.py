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
from utils.llm_client import LLMClient
from ai_agents.base_agent import Agent
def main():
    config = load_config()
    llm_client = LLMClient(api_key=config['llm']['api_key'], model=config['llm']['model'])
    ibkr_client = IBKRClient()
    # Update NewsAPI key in DataPipeline to match SentimentAnalyst
    data_pipeline = DataPipeline(ibkr_client)
    data_pipeline.news_api_key = "YOUR API KEYS"  # Replace if different (NewsAPI key)
    blackboard = Blackboard()
    market_hours = MarketHoursChecker()

    fundamental_analyst = FundamentalAnalyst("Fundamental Analyst", blackboard, llm_client)
    sentiment_analyst = SentimentAnalyst("Sentiment Analyst", blackboard, llm_client)
    technical_analyst = TechnicalAnalyst("Technical Analyst", blackboard, llm_client)
    bull_researcher = BullResearcher("Bull Researcher", blackboard, llm_client)
    bear_researcher = BearResearcher("Bear Researcher", blackboard, llm_client)
    facilitator = Agent("Facilitator", blackboard, llm_client)
    trader_agents = [
        ConservativeTrader("Conservative Trader", blackboard, llm_client),
        AggressiveTrader("Aggressive Trader", blackboard, llm_client),
        RLTrader("RL Trader", blackboard, llm_client)
    ]
    risk_manager = RiskManager(ibkr_client, config['risk_parameters'])

    for symbol in config['stocks']['NorthAmerica']:
        ibkr_client.subscribe_market_data(symbol)
        print(f"Subscribed to market data for {symbol}")

    scheduler = BlockingScheduler()
    for symbol in config['stocks']['NorthAmerica']:
        scheduler.add_job(
            trading_cycle,
            'cron',
            day_of_week='mon-fri',
            hour='*',
            minute='*/5',  # Change to '*/1' for testing every minute
            args=[symbol, ibkr_client, data_pipeline, market_hours, blackboard, fundamental_analyst, sentiment_analyst, technical_analyst, bull_researcher, bear_researcher, facilitator, trader_agents, risk_manager]
        )
    print("Scheduler configured. Starting trading cycle every 5 minutes.")
    
    # Run trading_cycle once immediately for debugging
    for symbol in config['stocks']['NorthAmerica']:
        print(f"Running initial trading cycle for {symbol}")
        trading_cycle(symbol, ibkr_client, data_pipeline, market_hours, blackboard, fundamental_analyst, sentiment_analyst, technical_analyst, bull_researcher, bear_researcher, facilitator, trader_agents, risk_manager)
    
    scheduler.start()

def trading_cycle(symbol, ibkr_client, data_pipeline, market_hours, blackboard, fundamental_analyst, sentiment_analyst, technical_analyst, bull_researcher, bear_researcher, facilitator, trader_agents, risk_manager):
    print(f"Starting trading cycle for {symbol}")
    if not market_hours.is_market_open('SMART'):
        print(f"Market closed for {symbol}.")
        return

    print(f"Market is open for {symbol}. Fetching data...")
    try:
        historical_data = data_pipeline.fetch_historical_data(symbol, "30 D", "5 mins")
        print(f"Fetched historical data for {symbol}: {len(historical_data)} bars")
        news = data_pipeline.fetch_news(symbol, "2024-01-01", "2024-12-31")
        print(f"Fetched {len(news)} news articles for {symbol}: {news[:2] if news else 'None'}")
        social_media = data_pipeline.fetch_social_media(symbol, "2024-01-01", "2024-12-31")
        print(f"Fetched social media for {symbol}: {social_media}")
        financials = data_pipeline.fetch_financial_statements(symbol)
        print(f"Fetched financials for {symbol}: {financials}")
        current_price = ibkr_client.get_current_price(symbol)
        if current_price is None:
            print(f"Unable to fetch current price for {symbol}.")
            return
        print(f"Current price for {symbol}: {current_price}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return

    print("Analyzing data with agents...")
    try:
        fundamental_analyst.analyze(financials)
        print(f"Fundamental analysis posted: {blackboard.get_report('Fundamental Analyst')}")
        sentiment_analyst.analyze(news + social_media)
        print(f"Sentiment analysis posted: {blackboard.get_report('Sentiment Analyst')}")
        technical_analyst.analyze(historical_data)
        print(f"Technical analysis posted: {blackboard.get_report('Technical Analyst')}")
    except Exception as e:
        print(f"Error during analysis for {symbol}: {e}")
        return

    print("Conducting debate...")
    debate = Debate(bull_researcher, bear_researcher, facilitator, blackboard)
    debate_outcome = debate.conduct_debate(symbol)
    print(f"Debate outcome for {symbol}: {debate_outcome}")

    print("Traders making decisions...")
    for trader in trader_agents:
        trader.make_decision(symbol, debate_outcome)
        print(f"{trader.name} decision: {blackboard.get_report(trader.name)['decision']}")

    trader_decisions = [trader.blackboard.get_report(trader.name)["decision"] for trader in trader_agents]
    final_decision = ensemble_decision(trader_decisions)
    print(f"Ensemble final decision for {symbol}: {final_decision}")
    if final_decision in ["buy", "sell"]:
        closes = [bar['close'] for bar in historical_data]
        approved, shares = risk_manager.approve_order(symbol, final_decision.upper(), closes, current_price)
        print(f"Risk manager approval: {approved}, Shares: {shares}")
        if approved:
            ibkr_client.place_order(symbol, final_decision.upper(), shares)
            print(f"Executed {final_decision} order for {symbol} with {shares} shares.")
        else:
            print(f"Order not approved by risk manager for {symbol}.")
    else:
        print(f"No trade executed for {symbol} because decision is {final_decision}.")

if __name__ == "__main__":
    main()