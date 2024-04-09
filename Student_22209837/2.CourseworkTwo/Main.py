import os
import sqlite3
from datetime import datetime

# import utils library
from modules.utils.info_logger import print_info_log
from modules.utils.args_parser import arg_parse_cmd
from modules.utils.config_parser import Config

# import database connection library
from modules.db.mongo_db import LoadMongo

# manipulate data in the mongo db library for mongoDB
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# import trade detection model
from modules.model.trade_detection_model import InvalidTradeDetectionModel

class LoadDataToDB:
    @staticmethod
    def load_into_mongodb(conf):
        print_info_log('Command line argument parsed & main config loaded', 'progress')
        mongo_loader = LoadMongo(conf['config']['Database']['Mongo'],
                                 conf['params']['OutputFile'],
                                 './static/file_load_logger.txt')
        mongo_loader.get_latest_input_file()
        mongo_loader.load_mongo_data()
        print_info_log('Script completed', 'progress')

class TradeValidator:
    def __init__(self, mongo_config, sqlite_config):
        self.mongo_config = mongo_config
        self.sqlite_config = sqlite_config
        self.connect_to_mongo()
        self.connect_to_sqlite()

    def connect_to_mongo(self):
        mongo_url = self.mongo_config['config']['Database']['Mongo']['url']
        client = MongoClient(mongo_url)
        db_name = self.mongo_config['config']['Database']['Mongo']['Db']
        self.db = client[db_name]
        print_info_log("Connected to MongoDB")

    def connect_to_sqlite(self):
        self.conn = sqlite3.connect(self.sqlite_config['config']['Database']['SQLite']['file'])
        self.cur = self.conn.cursor()
        print_info_log("Connected to SQLite")

    def load_into_sqlite(self):
        # Create SQLite table if not exists


        create_table_file_path = "./modules/db/SQL/CreateTable.sql"
        with open(create_table_file_path, "r") as create_table_file:
            create_statements = create_table_file.read()

        self.cur.executescript(create_statements)

        for trade in self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find():

            self.cur.execute("INSERT INTO TradingRecord VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (str(trade['_id']),
                 str(trade['DateTime']),
                 trade['Trader'],
                 trade['ISIN'],
                 trade['Quantity'],
                 trade['Notional'],
                 trade['TradeType'],
                 trade['Ccy'],
                 trade['Counterparty']))

        self.conn.commit()
        print_info_log("Data loaded into SQLite table")


    def store_valid_trades_mongo(self):
        valid_client = MongoClient(self.mongo_config['config']['Database']['Mongo']['url'])
        valid_db = valid_client['validDB1']
        valid_collection = valid_db['ValidTrades']

        for trade in self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find():
            if InvalidTradeDetectionModel.is_trade_valid(trade):
                valid_collection.insert_one(trade)
        print_info_log("Valid trades stored in 'validDB1.ValidTrades'")

    def store_valid_trades_sqlite(self):
        create_table_file_path = "./modules/db/SQL/CreateTable.sql"
        with open(create_table_file_path, "r") as create_table_file:
            create_statements = create_table_file.read()
        self.cur.executescript(create_statements)

        for trade in self.db[self.mongo_config['config']['Database']['Mongo']['Collection']].find():
            if InvalidTradeDetectionModel.is_trade_valid(trade):
                self.cur.execute("INSERT INTO trades_suspects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                 (str(trade['_id']),
                                  str(trade['DateTime']),
                                  trade['Trader'],
                                  trade['ISIN'],
                                  trade['Quantity'],
                                  trade['Notional'],
                                  trade['TradeType'],
                                  trade['Ccy'],
                                  trade['Counterparty']))

        self.cur.execute(insert_into_portfolio_positions_sql)
        self.conn.commit()
        self.conn.close()
        print_info_log("Valid trades loaded into 'trades_suspects' table in SQLite database")


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

if __name__ == '__main__':

    print_info_log('Main.py Script started', 'progress')


    # set all variable using pre-set configuration from the conf.yaml file
    args = arg_parse_cmd()
    parsed_args = args.parse_args()
    conf = Config(parsed_args.env_type)

    # initial load EquityTrades_20231123110001.parquet into MongoDB
    LoadDataToDB.load_into_mongodb(conf)

    validator = TradeValidator(conf, conf)

    # store all trade to TradingRecord table
    validator.load_into_sqlite()

    # check invalid trade and store it into trades_suspects table
    validator.store_valid_trades_mongo()
    validator.store_valid_trades_sqlite()
