from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from selenium.common.exceptions import WebDriverException, TimeoutException
import logging

# Configure logging
logging.basicConfig(filename='app_log.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')



csv_file = "pags.csv"
extension_path = 'grass_extension.crx'  # Path to your .crx file

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_extension(extension_path)  # Add the extension

# Initialize the browser with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Set the page load timeout to 5 seconds
    driver.set_page_load_timeout(5)

    while True:  # Infinite loop to keep cycling through the URLs
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                try:
                    # Attempt to visit the URL
                    driver.get(url)
                    logging.info(f"Visiting: {url}")
                    
                    # Gradually scroll down to the bottom of the page
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    for i in range(0, total_height, 15):  # Increment by 15 pixels
                        driver.execute_script(f"window.scrollTo(0, {i});")

                    # Scroll back up to the top of the page quickly
                    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

                except TimeoutException:
                    logging.warning(f"Loading timed out for {url}: Skipping to next URL")                   
                    continue  # Skip to the next URL if current URL times out
                except WebDriverException as e:
                    logging.error(f"Could not load URL {url}: {e}")
                    continue  # Handle other web driver exceptions and move to the next URL
finally:
    # Close the browser when done
    driver.quit()
    logging.info("Browser closed.")