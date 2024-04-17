from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
from selenium.common.exceptions import WebDriverException
import random  # Import the random module

import sys
sys.excepthook = lambda type, value, traceback: print(value)

import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


csv_file = "pags.csv"
extension_path = 'grass_extension.crx'  # Path to your .crx file

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_extension(extension_path)  # Add the extension
chrome_options.add_argument("--disable-features=SameSiteByDefaultCookies")  # Disable SameSite by default cookies
chrome_options.add_argument("--start-maximized")

# Initialize the browser with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Load all URLs from CSV file into a list
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        urls = [row['url'] for row in reader]  # Create a list of URLs
    
    random.shuffle(urls)  # Shuffle the list of URLs randomly

    # Process each URL in the randomized list
    for url in urls:
        try:
            # Visit the URL
            driver.get(url)
            print("Visiting:", url)
            
            # Gradually scroll down to the bottom of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(0, total_height, 20):  # Increment by 50 pixels
                driver.execute_script(f"window.scrollTo(0, {i});")
            
            # Scroll back up to the top of the page quickly
            driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

        except WebDriverException as e:
            print(f"Could not load URL {url}: {str(e)}")
            continue  # Move to the next URL
finally:
    # Close the browser when done
    driver.quit()
