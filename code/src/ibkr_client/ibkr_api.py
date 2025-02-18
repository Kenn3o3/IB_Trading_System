import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.account_summary_tags import AccountSummaryTags
import random

def load_config():
    # NOTE: Provide the actual implementation or import from a shared config loader
    import json
    with open("code/config/config.json", "r") as f:
        return json.load(f)

class IBKRConnection(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.account_data = {}
        self.positions = {}
        self.reqId = 1
        self.next_order_id = None
        self.account_data_ready = threading.Event()

    def nextValidId(self, orderId):
        self.next_order_id = orderId

    def updateAccountValue(self, key, value, currency, accountName):
        """
        Store each key/value in a dictionary for later use/printing.
        Example keys: 'AvailableFunds', 'NetLiquidation', 'BuyingPower', etc.
        """
        try:
            # Attempt to store as float if numeric
            self.account_data[key] = float(value)
        except ValueError:
            # Otherwise, store as string
            self.account_data[key] = value
        if key == "NetLiquidation":  # Final key in updates
            self.account_data_ready.set()
    def position(self, account, contract, pos, avgCost):
        self.positions[contract.symbol] = {
            'position': pos,
            'avg_cost': avgCost
        }
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        if errorCode in [2104, 2106, 2158]:
            print(f"INFO: {errorString}")  # Demote to informational message
        else:
            print(f"ERROR: Code {errorCode} - {errorString}")

class IBKRClient:
    def __init__(self):
        self.conn = IBKRConnection()
        self._connect()

    def _connect(self):
        config = load_config()
        self.conn.connect(
            config['ibkr']['host'],
            config['ibkr']['port'],
            config['ibkr']['client_id']
        )
        ib_thread = threading.Thread(target=self._run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        self._request_account_data()

    def _run_loop(self):
        self.conn.run()

    def _request_account_data(self):
        # Request account values & positions
        # self.conn.reqMarketDataType(3)
        self.conn.reqAccountUpdates(True, "")
        self.conn.reqPositions()
        self.conn.account_data_ready.wait(timeout=10)

    def get_account_data(self):
        """
        Returns the entire account_data dictionary.
        """
        return self.conn.account_data

    def get_positions(self):
        """
        Returns the positions dictionary.
        """
        return self.conn.positions

    def get_realtime_bars(self, symbol):
        """
        Placeholder for real-time bar data retrieval.
        You would implement TWS API calls here.
        """
        # For illustration, returning a mock bar
        # In production, you'd subscribe to real-time bars from IBKR
        class Bar:
            def __init__(self, open, high, low, close, volume):
                self.open = open
                self.high = high
                self.low = low
                self.close = close
                self.volume = volume
        # Generate slightly varying prices
        close = 200 + random.randint(-5, 5)
        return [Bar(200.0, 202.0, 198.0, close, 10000)]


    def _handle_data_farm_disconnect(self):
        print("Reconnecting to market data...")
        self._request_account_data()  # Re-request account/positions
        # Re-subscribe to real-time data streams here