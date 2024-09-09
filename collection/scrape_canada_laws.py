'''
Description: This script scrapes the content of the Canadian laws from the website 
https://laws.justice.gc.ca/eng/acts/F-11/index.html and writes the extracted 
information to a JSON file.
'''


# Import modules
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


# Function to extract information from a link
'''
@param link: str
@return: tuple
'''
def extract_information(link):
    # Open link in a new tab and switch to it
    driver.execute_script(f"window.open('{link}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Extract page title and content
    page_title = driver.title
    page_content = driver.find_element(By.TAG_NAME, "body").text
    
    # Close the tab and switch back to the main page
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    return page_title, page_content


# Main
try:
    # Open the main page
    url = "https://laws.justice.gc.ca/eng/acts/F-11/index.html"
    driver.get(url)

    # Get all the links on the main page
    links = driver.find_elements(By.CSS_SELECTOR, "a")

    # Filter out the links that are relevant
    filtered_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and "F-11" in link.get_attribute("href")]

    # Loop through each link and extract information
    all_information = []
    for link in filtered_links:
        title, content = extract_information(link)
        all_information.append({"title": title, "content": content})

    # Write the extracted information to a JSON file
    with open('results/canada_laws.json', 'w', newline='', encoding='utf-8') as file:
        json.dump(all_information, file, indent=4, ensure_ascii=False)

finally:
    # Close the WebDriver
    driver.quit()


