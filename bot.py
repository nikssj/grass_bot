from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
from selenium.common.exceptions import WebDriverException, TimeoutException
import logging

# Setup logging
logging.basicConfig(filename='selenium_log.log', level=logging.INFO)

csv_file = "pags.csv"
extension_path = 'grass_extension.crx'  # Path to your .crx file

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_extension(extension_path)  # Add the extension
chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images to speed up load time

# Initialize the browser with the options
driver = webdriver.Chrome(options=chrome_options)

# Set the page load timeout
driver.set_page_load_timeout(3)  # Increased timeout to 3 seconds for better reliability

try:
    while True:  # Infinite loop to keep cycling through the URLs
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                try:
                    # Attempt to visit the URL
                    driver.get(url)
                    logging.info(f"Visiting: {url}")
                except TimeoutException:
                    logging.warning(f"Timeout reached while loading {url}, proceeding with partially loaded page.")
                
                try:
                    # Gradually scroll down to the bottom of the page
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    for i in range(0, total_height, 50):  # Increment by 50 pixels
                        driver.execute_script(f"window.scrollTo(0, {i});")
                    
                    # Scroll back up to the top of the page quickly
                    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

                except WebDriverException as e:
                    logging.error(f"Error while processing {url}: {str(e)}")
                    continue  # Move to the next URL
finally:
    # Close the browser when done
    driver.quit()
    logging.info("Selenium driver has been closed.")
