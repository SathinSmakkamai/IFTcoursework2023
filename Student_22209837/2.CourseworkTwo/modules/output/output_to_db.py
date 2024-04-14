"""

UCL -- Institute of Finance & Technology
Author  : Sathin Smakkamai
Topic   : output_to_db.py

"""

import sqlite3
from pymongo import MongoClient

from modules.model.trade_detection_model import invalid_trade_detection
from modules.db.connect_to_db import connect_to_db

class output_to_SQLite:

    def load_SQLite(conf):

        # connect to database
        client, db, collection, data = connect_to_db.connect_to_mongoDB(conf)
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        # inset data from mongoDB to SQLite
        for record in data:
            cur.execute(f"INSERT INTO trades "
                        "(_id, DateTime, TradeId, Trader, Symbol, Quantity, Notional, TradeType, Ccy, Counterparty) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (str(record['_id']), record['DateTime'], record['TradeId'], record['Trader'], record['Symbol'],
                         record['Quantity'], record['Notional'], record['TradeType'], record['Ccy'],record['Counterparty']))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        client.close()

    def get_portfolio_position(conf):

        # Connect to SQLite database
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        cur.execute("""
        INSERT INTO portfolio_positions (date, trader, symbol, ccy, total_quantity, total_notional, num_trades)
        SELECT 
            SUBSTR(DateTime, 1, 10) AS date,
            Trader,
            Symbol,
            Ccy,
            SUM(Quantity) AS total_quantity,
            SUM(Notional) AS total_notional,
            COUNT(*) AS num_trades
        FROM trades
        GROUP BY trader, ccy, symbol;
        """)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    def get_suspect_trades(conf):

        # connect to database
        conn, cur = connect_to_db.connect_to_SQLite(conf)
        client, db, collection, data = connect_to_db.connect_to_mongoDB(conf)

        for record in data:

            # perform trade detection model
            if (invalid_trade_detection.correct_trade_type(record) or invalid_trade_detection.notional_exceeding(record)
                    or invalid_trade_detection.exceed_avg_price(record)):

                cur.execute(f"INSERT INTO trades_suspects "
                            "(_id, DateTime, TradeId, Trader, Symbol, Quantity, Notional, TradeType, Ccy, Counterparty) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (str(record['_id']), record['DateTime'], record['TradeId'], record['Trader'], record['Symbol'],
                             record['Quantity'], record['Notional'], record['TradeType'], record['Ccy'],record['Counterparty']))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
