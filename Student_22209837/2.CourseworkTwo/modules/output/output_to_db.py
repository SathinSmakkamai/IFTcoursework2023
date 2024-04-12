import sqlite3
from modules.utils.info_logger import print_info_log
from modules.model.trade_detection_model import InvalidTradeDetectionModel

from pymongo import MongoClient


from modules.db.connect_to_db import connect_to_db

class output_to_mongoDB:

    def get_suspect_trades_new(conf):

        # Connect to source MongoDB database
        client, data = connect_to_db.connect_to_mongoDB(conf)

        # Connect to "suspect_trade" MongoDB database
        db_dest = client['suspect_trade']

        for record in data:
            if InvalidTradeDetectionModel.is_trade_valid(record):
                # Insert invalid trades into "suspect_trade" database
                db_dest.trades_suspects.insert_one(record)

        # Commit changes and close connections
        client.close()


class output_to_SQLite:

    def load_mongodb_to_sqlite_new(conf):

        # connect to mongoDB database
        client, data = connect_to_db.connect_to_mongoDB(conf)

        # connect to SQLite database
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        # inset data from mongoDB to SQLite
        for record in data:
            cur.execute(f"INSERT INTO trades "
                        "(_id, DateTime, TradeId, Trader, Symbol, Quantity, Notional, TradeType, Ccy, Counterparty) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (str(record['_id']), record['DateTime'], record['TradeId'], record['Trader'], record['Symbol'],
                         record['Quantity'], record['Notional'], record['TradeType'], record['Ccy'],
                         record['Counterparty']))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        client.close()


    def get_suspect_trades_new(conf):

        # connect to SQLite database
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        client, data = connect_to_db.connect_to_mongoDB(conf)


        for record in data:
            if InvalidTradeDetectionModel.is_trade_valid(record):

                cur.execute(f"INSERT INTO trades_suspects "
                            "(_id, DateTime, TradeId, Trader, Symbol, Quantity, Notional, TradeType, Ccy, Counterparty) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (str(record['_id']), record['DateTime'], record['TradeId'], record['Trader'],
                             record['Symbol'],
                             record['Quantity'], record['Notional'], record['TradeType'], record['Ccy'],
                             record['Counterparty']))

        conn.commit()
        conn.close()



    def get_portfolio_position_from_trades_suspects(conf):

        # Connect to SQLite database
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        # Define SQL query to insert portfolio positions from trades_suspects table
        insert_into_portfolio_positions_sql = """
        INSERT INTO portfolio_positions (date, trader, symbol, ccy, total_quantity, total_notional)
        SELECT 
            SUBSTR(DateTime, 1, 10) AS date,
            Trader,
            Symbol,
            Ccy,
            SUM(Quantity) AS total_quantity,
            SUM(Notional) AS total_notional
        FROM trades_suspects
        GROUP BY date, trader, symbol, ccy;
        """

        # Execute the SQL query
        cur.execute(insert_into_portfolio_positions_sql)

        # Commit changes and close connection
        conn.commit()
        conn.close()

