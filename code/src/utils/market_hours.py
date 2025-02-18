# code/src/utils/market_hours.py

from datetime import datetime, time
import pytz
from dateutil import parser

class MarketHoursChecker:
    def __init__(self):
        self.holidays = {  # Basic holiday template (expand as needed)
            'NorthAmerica': [
                '2024-01-01',  # New Year's
                '2024-01-15',  # MLK Day
                '2024-02-19',  # Presidents Day
                # Add other NYSE holidays
            ],
            'AsiaHK': [
                '2024-01-01',  # New Year
                '2024-02-10',  # Lunar New Year
                # Add other HKEX holidays
            ]
        }
        
    def is_market_open(self, exchange: str) -> bool:
        """Check if market is open based on exchange and current time."""
        # Map IBKR exchange codes to regions
        exchange_region_map = {
            "SMART": "NorthAmerica",
            "NYSE": "NorthAmerica",
            "NASDAQ": "NorthAmerica",
            "HKEX": "AsiaHK"
        }
        region = exchange_region_map.get(exchange, exchange)
        if region not in ["NorthAmerica", "AsiaHK"]:
            raise ValueError(f"Unsupported exchange: {exchange}")

        now = datetime.now(pytz.utc)

        if region == "NorthAmerica":
            return self._is_nyse_open(now)
        elif region == "AsiaHK":
            return self._is_hkex_open(now)
        else:
            return False

    def _is_nyse_open(self, dt: datetime) -> bool:
        """NYSE trading hours 9:30 AM - 4:00 PM ET, Mon-Fri"""
        et = dt.astimezone(pytz.timezone('America/New_York'))
        
        # Check weekday
        if et.weekday() >= 5:  # Saturday(5) or Sunday(6)
            return False
            
        # Check holidays
        date_str = et.strftime('%Y-%m-%d')
        if date_str in self.holidays['NorthAmerica']:
            return False
            
        # Check time
        market_open = time(9, 30)
        market_close = time(16, 0)
        return market_open <= et.time() <= market_close

    def _is_hkex_open(self, dt: datetime) -> bool:
        """HKEX trading hours 9:30 AM - 4:00 PM HKT, Mon-Fri"""
        hkt = dt.astimezone(pytz.timezone('Asia/Hong_Kong'))
        
        if hkt.weekday() >= 5:
            return False
            
        date_str = hkt.strftime('%Y-%m-%d')
        if date_str in self.holidays['AsiaHK']:
            return False
            
        market_open = time(9, 30)
        market_close = time(16, 0)
        return market_open <= hkt.time() <= market_close

    def add_custom_holiday(self, exchange: str, date_str: str):
        """Add custom holiday dates (YYYY-MM-DD format)"""
        try:
            parsed_date = parser.parse(date_str).date()
            self.holidays[exchange].append(date_str)
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")
    def is_market_open(self, exchange: str) -> bool:
        # Map IBKR exchange codes to regions
        exchange_region_map = {
            "SMART": "NorthAmerica",  # Assuming SMART is used for North American stocks
            "NYSE": "NorthAmerica",
            "NASDAQ": "NorthAmerica",
            "HKEX": "AsiaHK"
        }
        region = exchange_region_map.get(exchange, exchange)
        if region not in ["NorthAmerica", "AsiaHK"]:
            raise ValueError(f"Unsupported exchange: {exchange}")
        
        # Rest of the method remains the same
        if region == "NorthAmerica":
            return self._is_nyse_open(now)
        elif region == "AsiaHK":
            return self._is_hkex_open(now)