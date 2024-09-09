'''
Description: This script fetches data from a CSV file and stores it in a MongoDB collection.
'''


# Import modules
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import certifi
import csv
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

ca = certifi.where()
MONGO_URI = os.getenv('MONGO_DB_URI_ISHREET')
DATABASE_NAME = 'Finance_Strategies'
COLLECTION_NAME = 'Strategies'

def fetch_and_store_data():
    # Connect to MongoDB
    
    client = MongoClient(MONGO_URI, tlsCAFile = ca)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return

    df = pd.read_csv('investing_strategies.csv')
    json_records = df.to_dict(orient='records')
    filtered_records = [{k: v for k, v in record.items() if pd.notnull(v) and v != ""} for record in json_records]
    print(filtered_records)
    collection.insert_many(filtered_records)

    print("Data inserted successfully")

# Example usage
if __name__ == '__main__':
    fetch_and_store_data()