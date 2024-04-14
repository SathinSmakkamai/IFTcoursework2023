"""

UCL -- Institute of Finance & Technology
Author  : Sathin Smakkamai
Topic   : connect_to_db.py

"""

class invalid_trade_detection:

    def correct_trade_type(data):

        invalid_trades = []

        for trade in data:
            if isinstance(trade, dict):

                trade_type = trade.get('TradeType')
                notional = trade.get('Notional')

                if trade_type == 'BUY' and notional < 0:
                    invalid_trades.append(trade)

                elif trade_type == 'SELL' and notional > 0:
                    invalid_trades.append(trade)

        return invalid_trades

    def notional_exceeding(data):

        if data['Notional'] > 30000000:

            return True
        return False

    def exceed_avg_price(data):

        symbol_total_notional = {}
        symbol_total_quantity = {}

        for trade in data:

            if isinstance(trade, dict):
                symbol = trade.get('Symbol')
                notional = trade.get('Notional', 0)
                quantity = trade.get('Quantity', 0)

                if symbol:
                    symbol_total_notional[symbol] = symbol_total_notional.get(symbol, 0) + notional
                    symbol_total_quantity[symbol] = symbol_total_quantity.get(symbol, 0) + quantity

        symbol_avg_price = {}

        for symbol, total_notional in symbol_total_notional.items():
            total_quantity = symbol_total_quantity.get(symbol, 0)
            avg_price = total_notional / total_quantity if total_quantity != 0 else 0
            symbol_avg_price[symbol] = avg_price

        for trade in data:

            if isinstance(trade, dict):
                symbol = trade.get('Symbol')
                notional = trade.get('Notional', 0)
                quantity = trade.get('Quantity', 0)
                avg_price = symbol_avg_price.get(symbol, 0)

                if quantity != 0:
                    trade_price = notional / quantity
                    if trade_price > 1.025 * avg_price:
                        return True

                    else:
                        return False
