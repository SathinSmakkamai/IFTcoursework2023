

import pandas as pd
from pymongo import MongoClient


class input_mongoDB:

    def load_parquet_to_mongodb(conf):

        df = pd.read_parquet(conf['parquet_file']['parquet_file'])
        data = df.to_dict(orient='records')

        # Step 3: Connect to MongoDB
        client = MongoClient(conf['mongoDB']['mongo_uri'])
        db = client[conf['mongoDB']['db_name']]
        collection = db[conf['mongoDB']['collection_name']]

        # Step 4: Insert data into MongoDB collection
        collection.insert_many(data)

        # Close the connection
        client.close()