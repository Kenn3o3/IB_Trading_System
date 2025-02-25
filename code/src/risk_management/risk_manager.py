from risk_management.adaptive_sizing import AdaptivePositionSizer

class RiskManager:
    def __init__(self, ibkr_client, config):
        self.ibkr_client = ibkr_client
        self.config = config
        self.sizer = AdaptivePositionSizer()

    def approve_order(self, symbol, action, historical_data, current_price):
        account_data = self.ibkr_client.get_account_data()
        positions = self.ibkr_client.get_positions()
        net_liq = account_data.get('NetLiquidation', 0)
        max_position_value = self.config['max_position_size'] * net_liq
        current_position = positions.get(symbol, {}).get('position', 0)
        current_position_value = current_position * current_price if current_position > 0 else 0

        if action == 'BUY':
            position_fraction = self.sizer.calculate_fraction(historical_data)
            position_value = position_fraction * net_liq
            shares = int(position_value / current_price)
            new_position_value = (current_position + shares) * current_price
            if new_position_value > max_position_value or account_data.get('AvailableFunds', 0) < (shares * current_price):
                return False, 0
            return True, shares
        elif action == 'SELL':
            if current_position > 0:
                return True, current_position  # Sell entire position
            return False, 0