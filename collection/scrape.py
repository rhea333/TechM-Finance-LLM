'''
Description: This script scrapes the content of a webpage using Selenium and 
stores it in a MongoDB database.
'''


# Import the modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Set up options for headless browsing
options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Set up the WebDriver (ensure the path to chromedriver is correct)
webdriver_service = Service('C:\chromedriver-win64\chromedriver.exe')  # Adjust path accordingly
driver = webdriver.Chrome(service=webdriver_service, options=options)

# URL of the page to scrape
url = 'https://www.cdic.ca/depositors/videos-and-resources/oversight-of-canadas-financial-system/'

# Open the webpage
driver.get(url)

# Wait for the page to fully load (adjust wait time as needed)
driver.implicitly_wait(10)

# Extract content using Selenium
content = driver.find_element(By.CSS_SELECTOR, 'body').text

# Close the WebDriver
driver.quit()

# MongoDB connection URI (replace with your actual MongoDB URI)
mongo_uri = os.getenv('MONGO_DB_URI_ROSIE')
db_name = 'Regulations'
c_name = 'finance_posts'

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[c_name]

# Prepare data to insert into MongoDB
data = {
    'url': url,
    'content': content
}

# Insert data into MongoDB
result = collection.insert_one(data)
print(f"Data inserted with ID: {result.inserted_id}")

# Close MongoDB connection
client.close()

''' Websites

Canada

'https://www.lexpert.ca/legal-faq/the-financial-institutions-act-of-canada-a-guide/377009'
'https://www.cdic.ca/depositors/videos-and-resources/oversight-of-canadas-financial-system/'
'https://laws.justice.gc.ca/eng/acts/F-11/index.html'
'https://www.iiroc.ca/'

America

'https://www.investopedia.com/ask/answers/063015/what-are-some-major-regulatory-agencies-responsible-overseeing-financial-institutions-us.asp'
'https://www.aba.com/banking-topics/compliance/acts#sort=%40stitle%20ascending'

'''


