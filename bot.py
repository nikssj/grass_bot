from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.common.exceptions import WebDriverException

csv_file = "pags.csv"

# Initialize the browser
driver = webdriver.Chrome()

try:
    while True:  # Infinite loop to keep cycling through the URLs
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                try:
                    # Visit the URL
                    driver.get(url)
                    print("Visiting:", url)
                    
                    # Wait for the page to load completely
                    time.sleep(2)
                    
                    # Gradually scroll down to the bottom of the page
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    for i in range(0, total_height, 50):  # Increment by 50 pixels
                        driver.execute_script(f"window.scrollTo(0, {i});")
                        time.sleep(0.05)  # Sleep time between scrolls

                    # Scroll back up to the top of the page
                    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
                    
                    # Wait a few seconds before moving to the next URL
                    time.sleep(4)
                    
                except WebDriverException as e:
                    print(f"Could not load URL {url}: {str(e)}")
                    continue  # Move to the next URL
finally:
    # Close the browser when done
    driver.quit()
