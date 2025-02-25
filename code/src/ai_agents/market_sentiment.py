import requests
from utils.llm_client import LLMClient

class SentimentAnalyzer:
    def __init__(self):
        self.llm = LLMClient()
        self.news_api_key = "YOUR_NEWSAPI_KEY"  # Replace with your NewsAPI key
        
    def get_real_time_sentiment(self, symbol):
        news = requests.get(
            f"https://newsapi.org/v2/everything?q={symbol}&apiKey={self.news_api_key}"
        ).json()
        
        prompt = f"""Analyze market sentiment for {symbol} from these headlines:
        {[article['title'] for article in news['articles'][:5]]}
        Output: BULLISH/NEUTRAL/BEARISH and 1-sentence reasoning"""
        
        analysis = self.llm.generate(prompt)
        return self._parse_sentiment(analysis)
    
    def _parse_sentiment(self, text):
        if "BULLISH" in text:
            return 1
        elif "BEARISH" in text:
            return -1
        return 0