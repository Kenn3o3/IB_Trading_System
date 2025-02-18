import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.account_summary_tags import AccountSummaryTags

class IBKRConnection(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.account_data = {}
        self.positions = {}
        self.reqId = 1
        
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        
    def updateAccountValue(self, key, value, currency, accountName):
        if key == AccountSummaryTags.AvailableFunds:
            self.account_data['available_cash'] = float(value)
            
    def position(self, account, contract, pos, avgCost):
        self.positions[contract.symbol] = {
            'position': pos,
            'avg_cost': avgCost
        }

class IBKRClient:
    def __init__(self):
        self.conn = IBKRConnection()
        self._connect()
        
    def _connect(self):
        config = load_config()  # Implement config loader
        self.conn.connect(config['ibkr']['host'], config['ibkr']['port'], config['ibkr']['client_id'])
        ib_thread = threading.Thread(target=self._run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        self._request_account_data()
        
    def _run_loop(self):
        self.conn.run()
        
    def _request_account_data(self):
        self.conn.reqAccountUpdates(True, "")
        self.conn.reqPositions()