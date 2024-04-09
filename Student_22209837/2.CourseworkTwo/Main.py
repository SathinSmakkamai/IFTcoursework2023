import os
import sqlite3
from datetime import datetime

# import utils library
from modules.utils.info_logger import print_info_log
from modules.utils.args_parser import arg_parse_cmd
from modules.utils.config_parser import Config

# import database connection library
from modules.db.input_to_mongoDB import input_mongoDB
from modules.db.db_connection import TradeValidator_connection

# manipulate data in the mongo db library for mongoDB
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# import trade detection model
from modules.model.trade_detection_model import InvalidTradeDetectionModel


if __name__ == '__main__':

    print_info_log('Main.py Script started', 'progress')

    # set all variable using pre-set configuration from the conf.yaml file
    args = arg_parse_cmd()
    parsed_args = args.parse_args()
    conf = Config(parsed_args.env_type)

    # initial load EquityTrades_20231123110001.parquet into MongoDB
    input_mongoDB.insert_data_to_mongoDB(conf)

    db_processor = TradeValidator_connection(conf, conf)

    # store all trade to TradingRecord table
    db_processor.create_SQL_table()
    db_processor.load_into_sqlite()

    # check invalid trade and store it into trades_suspects table
    # DB_processor.get_suspect_trades_mongoDB()
    db_processor.get_suspect_trades_SQLite()

    print_info_log('Completed', 'progress')
