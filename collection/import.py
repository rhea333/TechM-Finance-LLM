'''
Description: This script fetches data from MongoDB collections and writes it to 
a YAML file. It performs this for Loan_Approval collection but the collection 
name can be changed to any within the database to create a question answer form.
'''


# Import modules
import pymongo
import yaml
from dotenv import load_dotenv
import os

load_dotenv()


collection_list = ['BA_History', 'Canada_Laws', 'Finance_Posts', 'Fuel',
                   'Loan_Approval', 'US_General']

# MongoDB connection setup
client = pymongo.MongoClient(os.getenv('MONGO_DB_URI_ROSIE'))
db = client['Regulations']

# Collections to include in the YAML file
collections = [collection_list[4]]

# Function to fetch data from collections and convert it to a dictionary
'''
@param: db: MongoDB database object
'''
def fetch_data_from_collections(db, collections):
    qa_pairs = []

    # Fetch data from each collection
    for collection_name in collections:
        collection = db[collection_name]
        documents = list(collection.find())
        # Convert MongoDB ObjectId to string for YAML serialization
        
        # Append question and answer pairs to the list
        for doc in documents:
            qa_pair = {
                'question': doc.get('question', 'No question found'),
                'answer': doc.get('answer', 'No answer found')
            }
            qa_pairs.append(qa_pair)
    # Return the list of question and answer pairs
    return qa_pairs


# Fetch data from specified collections
data = fetch_data_from_collections(db, collections)

# Write data to a YAML file
with open('out.yaml', 'w') as file:
    for qa_pair in data:
        yaml.dump([{'question': qa_pair['question']}], file, default_flow_style=False)
        yaml.dump([{'answer': qa_pair['answer']}], file, default_flow_style=False)

print("Data written to output.yaml successfully.")
