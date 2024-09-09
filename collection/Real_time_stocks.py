'''
Description: This script fetches real-time stock data for a list of tickers and 
stores it in MongoDB.
'''


# Import modules
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime
import certifi
import numpy as np  # Import numpy for handling numpy.int64
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

# Create a connection to MongoDB
ca = certifi.where()
MONGO_URI = os.getenv('MONGO_DB_URI_RHEA')
DATABASE_NAME = 'real_time_stocks'
COLLECTION_NAME = 'stock_info'


# Function to convert numpy types to Python types
'''
@params: obj: object
@returns: object
'''
def convert_to_python_types(obj):
    if isinstance(obj, np.int64):
        return int(obj)  # Convert numpy.int64 to Python int
    elif isinstance(obj, np.float64):
        return float(obj)  # Convert numpy.float64 to Python float
    else:
        return obj  # Return unchanged for other types


# Function to fetch and store stock data in MongoDB
'''
@params: ticker: str
@returns: None
'''
def fetch_and_store_stock_data(ticker):
    # Connect to MongoDB
    ssl_ctx = ssl.create_default_context(cafile=ca)
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    client = MongoClient(MONGO_URI, tlsCAFile=ca)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return

    # Real-time data
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period='1d')

    # Check if stock_info is not empty
    if stock_info.empty:
        print(f"No data found for {ticker}")
        return

    # Prepare the data for MongoDB, converting numpy types to Python types
    stock_data = {
        'ticker': ticker,
        'date': datetime.now(),
        'open': convert_to_python_types(stock_info['Open'][0]),
        'high': convert_to_python_types(stock_info['High'][0]),
        'low': convert_to_python_types(stock_info['Low'][0]),
        'close': convert_to_python_types(stock_info['Close'][0]),
        'volume': convert_to_python_types(stock_info['Volume'][0])
    }

    # Upsert the data into MongoDB
    collection.update_one(
        {'ticker': ticker},
        {'$set': stock_data},
        upsert=True
    )

    print(f'Successfully upserted data for {ticker}')

# Main function
if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NVDA', 
               'JPM', 'JNJ', 'V', 'UNH', 'HD', 'PG', 'DIS', 'MA', 'PYPL', 
               'NFLX', 'INTC', 'CMCSA', 'PEP', 'KO', 'ADBE', 'CSCO', 'VZ', 'MRK', 
               'NKE', 'T', 'XOM', 'ABT', 'CRM', 'AVGO', 'LLY', 'ACN', 'COST', 
               'MCD', 'MDT', 'TXN', 'UNP', 'QCOM', 'NEE', 'BMY', 'UPS', 'PM', 
               'IBM', 'HON', 'LIN', 'LOW', 'CAT', 'MMM', 'RTX', 'GE', 'MS', 
               'BA', 'CVX', 'C', 'AMT', 'GS', 'BLK', 'CHTR', 'SPGI', 'PLD', 
               'SCHW', 'MO', 'AXP', 'AMGN', 'CL', 'TMO', 'BKNG', 'LMT', 'GILD', 
               'ANTM', 'FIS', 'BDX', 'ADP', 'SYK', 'TMUS', 'ISRG', 'TJX', 'DHR', 
               'EL', 'CI', 'AMAT', 'LRCX', 'CME', 'USB', 'PNC', 'ZTS', 'EQIX', 
               'ECL', 'NSC', 'MMC', 'AON', 'ICE', 'SO', 'DUK', 'D', 'ITW', 'CSX', 
               'APD', 'ETN', 'HUM', 'FISV', 'WM', 'PGR', 'MET', 'STT']
    
    for ticker in tickers:
        fetch_and_store_stock_data(ticker)



        


