'''
Description: This script scrapes the Investopedia website for financial terms and 
their definitions. The terms and definitions are stored in a MongoDB database.
'''


# import modules
import requests
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import certifi
import csv
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


# fetch_investopedia_term() finds the definition of a financial term on Investopedia
'''
@param url: the URL of the financial term on Investopedia
@return: the definition of the financial term
'''
def fetch_investopedia_term(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    session = requests.Session()
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve page: ", response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')

    key_takeaways_div = soup.find('div', {'id':'mntl-sc-block_5-0'})

    # Extract the bullet points if <ul> is found
    definition = ""
    if key_takeaways_div:
        ul_tag = key_takeaways_div.find('ul')
        if ul_tag:
            for li in ul_tag.find_all('li'):
                definition += li.text.strip() + ' '

    # Return the different definitions
    return definition


# fetch_investopedia_terms() finds all financial terms on Investopedia
'''
@return: a dictionary of financial terms and their definitions
'''
def fetch_investopedia_terms():
    url = "https://www.investopedia.com/financial-term-dictionary-4769738"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    session = requests.Session()
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve page:", response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the terms and their defintions and store in different arrays
    words = []
    definitions = []

    # Find all the <a> tags to get the words and definitions
    li_tags = soup.find_all('a')
    for tag in li_tags:
        url = tag.get('href')
        if '/terms/' in url:
            w = tag.find('span').text
            d = fetch_investopedia_term(url)
            if len(w) != 0 and len(d) != 0:
                words.append(w)
                definitions.append(d)

    # Create a dictionary of the words and definitions and return it
    return dict(zip(words, definitions))


# store_in_db() stores the financial terms and their definitions in a MongoDB database
def store_in_db():
	# Connect to MongoDB
    
    # Set up the MongoDB connection
	ca = certifi.where()
	MONGO_URI = os.getenv('MONGO_DB_URI_ALEX')
	DATABASE_NAME = 'FinanceTerms'
	COLLECTION_NAME = 'Investopedia'
     
	client = MongoClient(MONGO_URI, tlsCAFile = ca)
	db = client[DATABASE_NAME]
	collection = db[COLLECTION_NAME]

    # Drop the collection if it exists
	collection.delete_many({})

	# Send a ping to confirm a successful connection
	try:
		client.admin.command('ping')
		print("Pinged your deployment. You successfully connected to MongoDB!")
	except Exception as e:
		print(e)
		return

    # Fetch the financial terms and their definitions and add to a dataframe
	df = pd.read_csv('investopedia_terms.csv')
	df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: f"What is the definition of {x}?")
	
    # Convert the dataframe to a dictionary and insert into the MongoDB collection
	json_records = df.to_dict(orient='records')
	collection.insert_many(json_records)

	print("Data inserted successfully")


# Main function
if __name__ == '__main__':
    fetch_investopedia_terms()
    store_in_db()