class RiskManager:
    def __init__(self, ibkr_client, config):
        self.ibkr_client = ibkr_client
        self.config = config

    def approve_order(self, symbol, action):
        account_data = self.ibkr_client.get_account_data()
        positions = self.ibkr_client.get_positions()

        # Check available cash (if action is BUY, ensure we have positive funds).
        if action == 'BUY':
            usable_cash = account_data.get('AvailableFunds', 0)  # IB often labels 'AvailableFunds'
            if usable_cash <= 0:
                return False

        # Check net liquidation if available
        net_liq = account_data.get('NetLiquidation', 0)
        max_size = self.config['max_position_size'] * net_liq

        # Current position
        current_position = positions.get(symbol, {}).get('position', 0)

        if action == 'BUY' and current_position >= max_size:
            return False
        if action == 'SELL':
            # Even if we hold 0, a SELL will open a short if the broker allows
            # But if you want to limit how big the short can get, also check abs(current_position)
            if abs(current_position) >= max_size:
                return False

        return True
