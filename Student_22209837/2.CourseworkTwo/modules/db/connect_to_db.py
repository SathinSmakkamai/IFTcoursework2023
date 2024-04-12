import sqlite3
from modules.utils.info_logger import print_info_log
from modules.model.trade_detection_model import InvalidTradeDetectionModel

from pymongo import MongoClient


class connect_to_db:

    def connect_to_mongoDB(conf):

        client = MongoClient(conf['mongoDB']['mongo_uri'])
        db = client[conf['mongoDB']['db_name']]
        collection = db[conf['mongoDB']['collection_name']]
        data = list(collection.find())

        return client, data

    def connect_to_SQLite(conf):

        conn = sqlite3.connect(conf['SQLite']['sqlite_db'])
        cur = conn.cursor()

        return conn, cur