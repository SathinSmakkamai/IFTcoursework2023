


class InvalidTradeDetectionModel:
    @staticmethod
    def is_trade_valid(trade_data):
        # Check if the notional value is less than 1000000
        if trade_data['Notional'] < 1000000:
            return True
        return False






