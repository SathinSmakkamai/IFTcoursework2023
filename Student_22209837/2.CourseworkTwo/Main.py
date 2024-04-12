
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
import sqlite3

# import utils library
from modules.utils.info_logger import print_info_log
from modules.utils.args_parser import arg_parse_cmd
from modules.utils.config_parser import Config

# import input library
from modules.input.input_to_mongoDB import input_mongoDB

# import database connection library
from modules.db.connect_to_db import connect_to_db

# import trade_detection_model library
from modules.model.create_table import create_table
from modules.model.trade_detection_model import InvalidTradeDetectionModel

# import output library (load result to database)
from modules.output.output_to_db import output_to_mongoDB
from modules.output.output_to_db import output_to_SQLite


if __name__ == '__main__':

    print_info_log('Main.py Script started', 'progress')

    # set all variable using pre-set configuration from the conf.yaml file
    args = arg_parse_cmd()
    parsed_args = args.parse_args()
    conf = Config(parsed_args.env_type)

    # load parquet data to mongoDB
    input_mongoDB.load_parquet_to_mongodb(conf)

    # create SQLite table using .sql file
    create_table.create_SQL_table_new(conf)

    # load all trading record to SQL table
    output_to_SQLite.load_mongodb_to_sqlite_new(conf)

    # Get suspect trades to database
    output_to_SQLite.get_suspect_trades_new(conf)
    # output_to_mongoDB.get_suspect_trades_new(conf)

    # Get portfolio position and input to SQLite
    output_to_SQLite.get_portfolio_position_from_trades_suspects(conf)


    print_info_log('Completed', 'progress')

