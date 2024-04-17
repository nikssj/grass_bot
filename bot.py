from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import csv
import random  # Import the random module
import sys
import logging
import pyautogui

# Setup basic logging
logging.basicConfig(filename='app.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
# Handling unexpected exceptions to avoid script crashing
sys.excepthook = lambda type, value, traceback: print(value)

csv_file = "pags.csv"
extension_path = 'grass_extension.crx'  # Path to your .crx file

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_extension(extension_path)  # Add the extension
chrome_options.add_argument("--disable-features=SameSiteByDefaultCookies")  # Disable SameSite by default cookies
chrome_options.add_argument("--start-maximized")  # Start maximized
chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors

# Initialize the browser with the options
driver = webdriver.Chrome(options=chrome_options)



try:
    # Set the page load timeout to 5 seconds
    driver.set_page_load_timeout(5)

    # Open the first URL in a new tab and navigate to the second URL
    driver.execute_script("window.open('');")  # Open a new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
    driver.get("https://app.getgrass.io/")  # Navigate to the URL

    # Switch back to the first tab to continue processing the original URLs
    driver.switch_to.window(driver.window_handles[0])
    
    #To press 'Control + 2'
    pyautogui.hotkey('ctrl', '2')

    while True:  # Infinite loop to continuously process URLs
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
                for i in range(0, total_height, 20):  # Increment by 20 pixels
                    driver.execute_script(f"window.scrollTo(0, {i});")

                # Scroll back up to the top of the page quickly
                driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

            except TimeoutException:
                print(f"Timeout loading {url}: Skipping to next URL")
                continue  # Skip to the next URL if current URL times out
            except WebDriverException as e:
                print(f"Could not load URL {url}: {str(e)}")
                continue  # Handle other web driver exceptions and move to the next URL
finally:
    # Close the browser when done
    driver.quit()
