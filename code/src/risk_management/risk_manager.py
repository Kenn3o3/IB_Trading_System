class RiskManager:
    def __init__(self, ibkr_client, config):
        self.ibkr_client = ibkr_client
        self.config = config
        
    def approve_order(self, symbol, action):
        account_data = self.ibkr_client.get_account_data()
        positions = self.ibkr_client.get_positions()
        
        # Check available cash
        if action == 'BUY':
            usable_cash = account_data.get('available_cash', 0)
            if usable_cash <= 0:
                return False
            
        # Check position limits
        position = positions.get(symbol, 0)
        max_size = self.config['max_position_size'] * account_data['net_liquidation']
        
        if action == 'BUY' and position >= max_size:
            return False
        if action == 'SELL' and position <= 0:
            return False
            
        return True
