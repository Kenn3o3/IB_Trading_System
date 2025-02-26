# AI-Powered Algorithmic Trading System with Interactive Brokers

This project is an algorithmic trading system that integrates multiple LLM-based AI agents with Interactive Brokers (IBKR) for automated market analysis and trade execution. Using a blackboard architecture, the system employs a collaborative multi-agent approach to analyze market data, conduct debates on market outlook, and execute trades with robust risk management.

## Features

- **Multi-Agent AI System**: Includes agents for fundamental analysis, sentiment analysis, technical analysis, bullish/bearish research, and diverse trading strategies (conservative, aggressive, RL-based).
- **Debate Mechanism**: Bull and bear researchers debate to determine a bullish, bearish, or neutral market outlook.
- **Ensemble Decision-Making**: Combines decisions from multiple trader agents for a final trade action.
- **Risk Management**: Features adaptive position sizing and risk approval based on volatility and account constraints.
- **Real-Time Integration**: Connects to Interactive Brokers for live market data and trade execution.
- **Scheduled Trading**: Executes trading cycles every 5 minutes during market hours.
- **LLM-Powered Insights**: Utilizes Alibaba's Qwen LLM for generating analysis and decision-making content.

## Architecture

The system is built around a **blackboard pattern**, enabling collaboration among AI agents. Key components include:

- **Data Pipeline**: Retrieves historical price data, news, and (mock) financial statements/social media data.
- **AI Agents**:
  - **Fundamental Analyst**: Evaluates financial statements for valuation and growth insights.
  - **Sentiment Analyst**: Analyzes news and social media for market sentiment.
  - **Technical Analyst**: Applies SMA crossover and other technical indicators.
  - **Bull & Bear Researchers**: Debate market outlook based on available data.
  - **Trader Agents**: Propose buy/sell/hold decisions (Conservative, Aggressive, RL-based).
- **Debate System**: Facilitates structured debates to determine market sentiment.
- **Ensemble Strategy**: Aggregates trader decisions for a unified trade action.
- **Risk Manager**: Ensures trades align with risk parameters (e.g., max position size, daily loss limits).
- **IBKR Client**: Handles real-time data and order execution via the Interactive Brokers API.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   https://github.com/Kenn3o3/IB_Trading_System
   ```
2. **Navigate to the project directory**:
   ```bash
   cd IB_Trading_System
   ```
3. **Create a conda environment**:
   ```bash
   conda create --name ib_trade python=3.8
   ```
4. **Activate the environment**:
   ```bash
   conda activate ib_trade
   ```
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

**Note**: Ensure Interactive Brokers Trader Workstation (TWS) or IB Gateway is running and configured to accept API connections (default: `127.0.0.1:7497`).

## Configuration

Before running the system, configure the following files with your API keys and preferences:

1. **`code/config/config.json`**:
   - **Interactive Brokers Settings**:
     - `"host"`: IBKR host (default: `"127.0.0.1"`)
     - `"port"`: IBKR port (default: `7497`)
     - `"client_id"`: IBKR client ID (default: `1`)
   - **Stock Symbols**:
     - `"stocks"`: Add symbols under `"NorthAmerica"` (e.g., `["NVDA", "AAPL"]`) or `"AsiaHK"`.
   - **Risk Parameters**:
     - `"max_position_size"`: Max portfolio fraction per position (default: `0.05`).
     - `"max_daily_loss"`: Max daily loss limit (default: `0.02`).
     - `"order_size"`: Default order size fraction (default: `0.1`).
   - **LLM Settings**:
     - `"api_key"`: Your Alibaba Qwen API key (replace `"YOUR_API_KEYS"`).
     - `"model"`: LLM model (default: `"qwen-turbo"`).

   Example:
   ```json
   {
       "ibkr": {
           "host": "127.0.0.1",
           "port": 7497,
           "client_id": 1
       },
       "stocks": {
           "NorthAmerica": ["NVDA", "AAPL"],
           "AsiaHK": []
       },
       "risk_parameters": {
           "max_position_size": 0.05,
           "max_daily_loss": 0.02,
           "order_size": 0.1
       },
       "llm": {
           "provider": "alibaba",
           "api_key": "your-alibaba-api-key-here",
           "model": "qwen-turbo"
       }
   }
   ```

2. **Additional API Key Replacements**:
   - Search for `"YOUR_API_KEY"` or `"YOUR API KEYS"` in the following files and replace with your NewsAPI key:
     - `code/src/ai_agents/sentiment_analyst.py`
     - `code/src/ai_agents/market_sentiment.py`
     - `code/src/main.py`
     - `code/src/ibkr_client/data_pipeline.py`

## Usage

To start the trading system:

```bash
python code/src/main.py
```

The system will:
- Connect to Interactive Brokers and subscribe to market data for configured stocks.
- Run trading cycles every 5 minutes during market hours (Monday–Friday, 9:30 AM–4:00 PM ET for North America).
- Fetch data, perform analyses, conduct debates, make trading decisions, and execute approved trades.

**Sample Output**:
```
Subscribed to market data for NVDA
Scheduler configured. Starting trading cycle every 5 minutes.
Starting trading cycle for NVDA
Market is open for NVDA. Fetching data...
Fetched historical data for NVDA: 5760 bars
...
Ensemble final decision for NVDA: buy
Risk manager approval: True, Shares: 10
Executed buy order for NVDA with 10 shares.
```

## Project Structure

```
code/
├── config/              # Configuration files
│   ├── config.json      # Main config (IBKR, stocks, risk, LLM)
│   └── prompts/         # Prompt templates for LLM agents
├── src/                 # Source code
│   ├── main.py          # Entry point for the trading system
│   ├── ai_agents/       # AI agent implementations
│   ├── ibkr_client/     # IBKR API and data pipeline
│   ├── risk_management/ # Risk management and position sizing
│   ├── strategies/      # Trading strategies (e.g., SMA crossover)
│   └── utils/           # Utility modules (LLM client, market hours)
```

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please report issues or suggest enhancements via the GitHub Issues tab.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Interactive Brokers API](https://www.interactivebrokers.com/api/doc.html) – For real-time market data and trading capabilities.
- [Alibaba Qwen LLM](https://www.alibabacloud.com/en/product/qwen) – For advanced language model support.
- [NewsAPI](https://newsapi.org/) – For news data integration.
- [Trading Agents AI](https://tradingagents-ai.github.io/) – Reference material and inspiration.
