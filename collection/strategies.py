'''
Description: This script scrapes the website 
'https://www.bankrate.com/investing/investment-strategies-for-beginners/' 
to get the investment strategies for beginners.
'''


# Import modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL of the website to scrape
url = 'https://www.bankrate.com/investing/investment-strategies-for-beginners/'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was succhessful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    headers = soup.find_all('h3')

    # Loop through each <h2> tag and print associated paragraphs
    data = []
    for header in headers:
        if len(header.text) > 0:
            if header.text[0].isdigit():
                clean_header = re.sub(r'^[\d.]+', '', header.text.strip())
                sentence = f"Can you explain {clean_header.strip()} topic?"
                # Find all <p> tags that are siblings until the next <h2>
                paragraphs = []
                next_element = header.find_next_sibling()
                while next_element and next_element.name != 'h3':
                    if next_element.name == 'p':
                        paragraphs.append(next_element.text.strip())
                    next_element = next_element.find_next_sibling()
                
                # Print or process paragraphs as needed
                paragraph_string = ""
                for paragraph in paragraphs:
                    #print(f"Paragraph: {paragraph}")
                    paragraph_string += paragraph
                #print("---")
                data.append({'Title': sentence, 'Description': paragraph_string})

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('investing_strategies.csv', index=False)