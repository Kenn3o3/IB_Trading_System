from ai_agents.base_agent import Agent
import requests

class SentimentAnalyst(Agent):
    def __init__(self, name, blackboard, llm_client):
        super().__init__(name, blackboard, llm_client)
        self.news_api_key = "YOUR_API_KEY"  # Replace with your NewsAPI key

    def analyze(self, texts):
        prompt = f"Analyze sentiment of these texts: {texts}. Output: BULLISH/NEUTRAL/BEARISH and reasoning."
        sentiment = self.llm.generate(prompt)
        sentiment_value = 1 if "BULLISH" in sentiment else -1 if "BEARISH" in sentiment else 0
        self.communicate({"sentiment": sentiment_value, "reasoning": sentiment})