"""

UCL -- Institute of Finance & Technology
Author  : Sathin Smakkamai
Topic   : connect_to_db.py

"""

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
from modules.model.trade_detection_model import invalid_trade_detection

# import output library (load result to database)
from modules.output.output_to_db import output_to_SQLite


if __name__ == '__main__':

    print_info_log('Main.py Script started', 'progress')

    # set all variable using pre-set configuration from the conf.yaml file
    args = arg_parse_cmd()
    parsed_args = args.parse_args()
    conf = Config(parsed_args.env_type)

    # input parquet data to mongoDB
    input_mongoDB.load_parquet_to_mongodb(conf)

    # connect to database
    client, db, collection, data = connect_to_db.connect_to_mongoDB(conf)
    conn, cur = connect_to_db.connect_to_SQLite(conf)

    # create SQLite table using .sql file
    create_table.create_SQL_table_new(conf)

    # insert trading record to SQL table
    output_to_SQLite.load_SQLite(conf)

    # get portfolio position from trading records
    output_to_SQLite.get_portfolio_position(conf)

    # get suspect trades to SQLite database
    output_to_SQLite.get_suspect_trades(conf)

