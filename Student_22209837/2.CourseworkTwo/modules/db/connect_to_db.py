"""

UCL -- Institute of Finance & Technology
Author  : Sathin Smakkamai
Topic   : connect_to_db.py

"""

import sqlite3
from pymongo import MongoClient

class connect_to_db:

    def connect_to_mongoDB(conf):

        client = MongoClient(conf['mongoDB']['mongo_uri'])
        db = client[conf['mongoDB']['db_name']]
        collection = db[conf['mongoDB']['collection_name']]
        data = list(collection.find())

        return client, db, collection, data

    def connect_to_SQLite(conf):

        conn = sqlite3.connect(conf['SQLite']['sqlite_db'])
        cur = conn.cursor()

        return conn, cur