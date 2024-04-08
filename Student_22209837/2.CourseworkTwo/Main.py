import os
import sqlite3
from datetime import datetime

# load library from repo
from modules.utils.info_logger import print_info_log
from modules.utils.args_parser import arg_parse_cmd
from modules.utils.config_parser import Config
from modules.db.mongo_db import LoadMongo

# manipulate data in the mongo db library for mongoDB
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class Load_Data_to_DB:

    @staticmethod
    def load_into_mongoDB():
        print_info_log('Command line argument parsed & main config loaded', 'progress')
        mongo_loader = LoadMongo(conf['config']['Database']['Mongo'],
                                 conf['params']['OutputFile'],
                                 './static/file_load_logger.txt')
        mongo_loader.get_latest_input_file()
        mongo_loader.load_mongo_data()
        print_info_log('Script completed', 'progress')

    @staticmethod
    def load_into_sqlite():
        # Create SQLite table if not exists
        conn = sqlite3.connect('trades_suspects.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS TradingRecord (
                        _id TEXT PRIMARY KEY,
                        Notional REAL,
                        Date TEXT,
                        OtherColumns TEXT)''')
        conn.commit()

        # Insert data into SQLite table
        trades = self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find()
        # trades = db[mongo_config['config']['Database']['Mongo']['Collection']].find()
        for trade in trades:
            cur.execute('''INSERT INTO TradingRecord (_id, Notional, Date, OtherColumns) 
                            VALUES (?, ?, ?, ?)''',
                         (str(trade['_id']), trade['Notional'], trade['Date'],
                          'OtherData'))  # Modify 'OtherData' accordingly
        conn.commit()
        print("Data loaded into SQLite table")

class TradeValidator:

    def __init__(self, mongo_config, sqlite_config):
        self.mongo_config = mongo_config
        # self.sqlite_config = sqlite_config
        self.connect_to_mongo()
        # self.connect_to_sqlite()

    def connect_to_mongo(self):
        mongo_url = self.mongo_config['config']['Database']['Mongo']['url']
        client = MongoClient(mongo_url)
        db_name = self.mongo_config['config']['Database']['Mongo']['Db']
        self.db = client[db_name]
        print("Connected to MongoDB")

    def connect_to_sqlite(self):
        self.conn = sqlite3.connect(self.sqlite_config['config']['Database']['SQLite']['file'])
        self.cur = self.conn.cursor()
        print("Connected to SQLite")

    def is_trade_valid(self, trade_data):
        # Check if the notional value is less than 1000000
        if trade_data['Notional'] < 1000000:
            return True
        return False

    def store_valid_trades_mongo(self):
        # change collection for each time we load information to the database
        # Connect to the validDB database
        valid_client = MongoClient(self.mongo_config['config']['Database']['Mongo']['url'])
        valid_db = valid_client['validDB3']

        # Create a new collection for valid trades
        valid_collection = valid_db['ValidTrades']

        # Iterate over all documents in the original collection
        for trade in self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find():
            if self.is_trade_valid(trade):
                # Store the document in the new collection
                valid_collection.insert_one(trade)
        print("Valid trades stored in 'validDB3.ValidTrades'")


    def store_valid_trades_sqlite(self):
        # Connect to SQLite database
        conn = sqlite3.connect('trades_suspects.db')
        c = conn.cursor()

        # Read creation statements from CreateTable.sql file
        with open(create_table_file_path, "r") as create_table_file:
            create_statements = create_table_file.read()

        # Execute creation statements
        c.executescript(create_statements)

        # Iterate over all documents in the original collection
        for trade in self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find():
            if self.is_trade_valid(trade):
                # Insert valid trades into SQLite table
                c.execute("INSERT INTO trades_suspects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (str(trade['_id']),
                           str(trade['DateTime']),
                           trade['Trader'],
                           trade['ISIN'],
                           trade['Quantity'],
                           trade['Notional'],
                           trade['TradeType'],
                           trade['Ccy'],
                           trade['Counterparty']))

        # Execute query to insert into portfolio_positions
        c.execute(insert_into_portfolio_positions_sql)

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Valid trades loaded into 'trades_suspects' table in SQLite database")



insert_into_portfolio_positions_sql = """
INSERT INTO portfolio_positions (date, trader, symbol, ccy, total_quantity, total_notional)
SELECT 
    SUBSTR(datetime, 1, 10) AS date,
    trader,
    isin AS symbol,
    ccy,
    SUM(quantity) AS total_quantity,
    SUM(notional) AS total_notional
FROM trades_suspects
GROUP BY date, trader, isin, ccy;
"""


# Define the path for the CreateTable file
create_table_file_path = "./modules/db/SQL/CreateTable.sql"

if __name__ == '__main__':
    print_info_log('Script started', 'progress')

    args = arg_parse_cmd()
    parsed_args = args.parse_args()

    # load information from conf.yaml file
    conf = Config(parsed_args.env_type)
    # print(conf)

    # load data from parquet to mongoDB
    # Load_Data_to_DB.load_into_mongoDB()
    # Load_Data_to_DB.load_into_sqlite()

    validator = TradeValidator(conf, conf)

    # validator.store_valid_trades_mongo()
    validator.store_valid_trades_sqlite()
