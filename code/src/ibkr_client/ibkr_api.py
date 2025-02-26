import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.account_summary_tags import AccountSummaryTags
import json

def load_config():
    with open("code/config/config.json", "r") as f:
        return json.load(f)

class IBKRConnection(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.account_data = {}
        self.positions = {}
        self.current_prices = {}
        self.reqId = 1
        self.next_order_id = None
        self.account_data_ready = threading.Event()
        self.historical_data = []
        self.historical_data_ready = threading.Event()
        self.reqId_to_symbol = {}
        self.subscribed_symbols = set()
        self.connection_ready = threading.Event()

    def nextValidId(self, orderId):
        self.next_order_id = orderId
        self.connection_ready.set()
        print(f"Received nextValidId: {orderId}")

    def updateAccountValue(self, key, value, currency, accountName):
        try:
            self.account_data[key] = float(value)
        except ValueError:
            self.account_data[key] = value
        if key == "NetLiquidation":
            self.account_data_ready.set()

    def position(self, account, contract, pos, avgCost):
        self.positions[contract.symbol] = {'position': pos, 'avg_cost': avgCost}

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        if errorCode in [2104, 2106, 2158]:
            print(f"INFO: {errorString}")
        else:
            print(f"ERROR: Code {errorCode} - {errorString}")

    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 4:  # Last price
            symbol = self.reqId_to_symbol.get(reqId)
            if symbol:
                self.current_prices[symbol] = price
                print(f"Received price for {symbol}: {price}")

    def historicalData(self, reqId, bar):
        print(f"Received historical bar for reqId {reqId}: {bar.date}, close: {bar.close}")
        self.historical_data.append({
            'date': bar.date,
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume
        })

    def historicalDataEnd(self, reqId, start, end):
        self.historical_data_ready.set()

class IBKRClient:
    def __init__(self):
        self.conn = IBKRConnection()
        self._connect()

    def _connect(self):
        config = load_config()
        self.conn.connect(config['ibkr']['host'], config['ibkr']['port'], config['ibkr']['client_id'])
        ib_thread = threading.Thread(target=self.conn.run, daemon=True)
        ib_thread.start()
        timeout = 10
        start_time = time.time()
        while not self.conn.isConnected() and (time.time() - start_time) < timeout:
            print("Waiting for connection...")
            time.sleep(1)
        if not self.conn.isConnected():
            raise ConnectionError("Failed to connect to IBKR after 10 seconds")
        print("Connected to IBKR")
        self.conn.connection_ready.wait(timeout=10)
        if not self.conn.connection_ready.is_set():
            raise ConnectionError("Connection not fully established after 10 seconds")
        print("Connection fully established")
        self._request_account_data()

    def _request_account_data(self):
        self.conn.reqAccountUpdates(True, "")
        self.conn.reqPositions()
        self.conn.account_data_ready.wait(timeout=10)

    def get_account_data(self):
        return self.conn.account_data

    def get_positions(self):
        return self.conn.positions

    def subscribe_market_data(self, symbol):
        if symbol not in self.conn.subscribed_symbols:
            contract = Contract()
            contract.symbol = symbol
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"
            reqId = self.conn.reqId
            self.conn.reqId += 1
            self.conn.reqMktData(reqId, contract, "", False, False, [])
            self.conn.reqId_to_symbol[reqId] = symbol
            self.conn.subscribed_symbols.add(symbol)

    def get_current_price(self, symbol):
        if symbol not in self.conn.current_prices:
            self.subscribe_market_data(symbol)
            time.sleep(2)  # Increased wait time
        return self.conn.current_prices.get(symbol)

    def get_historical_data(self, symbol, duration, bar_size):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        reqId = self.conn.reqId
        self.conn.reqId += 1
        self.conn.historical_data = []
        self.conn.historical_data_ready.clear()
        self.conn.reqHistoricalData(reqId, contract, "", duration, bar_size, "TRADES", 1, 1, False, [])
        self.conn.historical_data_ready.wait(timeout=10)
        return self.conn.historical_data

    def place_order(self, symbol, action, quantity):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity
        self.conn.placeOrder(self.conn.next_order_id, contract, order)
        self.conn.next_order_id += 1