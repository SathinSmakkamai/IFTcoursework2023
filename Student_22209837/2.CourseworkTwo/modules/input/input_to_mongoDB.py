"""

UCL -- Institute of Finance & Technology
Author  : Sathin Smakkamai
Topic   : input_to_mongoDB.py

"""

import pandas as pd
from modules.db.connect_to_db import connect_to_db

class input_mongoDB:

    def load_parquet_to_mongodb(conf):

        # read information from parquet file
        df = pd.read_parquet(conf['parquet']['parquet_file_path'])
        parquet_data = df.to_dict(orient='records')

        # connect to mongoDB
        client, db, collection, data = connect_to_db.connect_to_mongoDB(conf)

        # insert data to mongoDB
        collection.insert_many(parquet_data)

        client.close()