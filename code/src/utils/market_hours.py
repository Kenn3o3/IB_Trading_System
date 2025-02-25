from datetime import datetime, time
import pytz

class MarketHoursChecker:
    def __init__(self):
        self.holidays = {
            'NorthAmerica': [
                '2024-01-01', '2024-01-15', '2024-02-19'
            ],
            'AsiaHK': [
                '2024-01-01', '2024-02-10'
            ]
        }
        
    def is_market_open(self, exchange):
        exchange_region_map = {"SMART": "NorthAmerica", "NYSE": "NorthAmerica", "NASDAQ": "NorthAmerica", "HKEX": "AsiaHK"}
        region = exchange_region_map.get(exchange, exchange)
        now = datetime.now(pytz.utc)
        if region == "NorthAmerica":
            return self._is_nyse_open(now)
        elif region == "AsiaHK":
            return self._is_hkex_open(now)
        return False

    def _is_nyse_open(self, dt):
        et = dt.astimezone(pytz.timezone('America/New_York'))
        if et.weekday() >= 5 or et.strftime('%Y-%m-%d') in self.holidays['NorthAmerica']:
            return False
        market_open, market_close = time(9, 30), time(16, 0)
        return market_open <= et.time() <= market_close

    def _is_hkex_open(self, dt):
        hkt = dt.astimezone(pytz.timezone('Asia/Hong_Kong'))
        if hkt.weekday() >= 5 or hkt.strftime('%Y-%m-%d') in self.holidays['AsiaHK']:
            return False
        market_open, market_close = time(9, 30), time(16, 0)
        return market_open <= hkt.time() <= market_close