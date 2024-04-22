from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
from datetime import datetime
import pandas as pd

def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


data_list = []
# Initialize Chrome driver
driver = webdriver.Chrome()

# Navigate to the page
driver.get("https://www.amazon.in/gp/bestsellers/beauty")

# Define a function to scroll the page
def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# # Function to fetch data from a page
def fetch_data_from_page():
    for i in range(1, 55):
        item_data = {}
        try:
            name = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[{0}]/div/div/div[2]/div/a[2]/span/div'.format(i))
            item_data['name'] = name.text
        except:
            item_data['name'] = ""

        try:
            price = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[{0}]/div/div/div[2]/div/div[2]/div/div/a/div/span/span'.format(i))
            item_data['price'] = price.text
        except:
            item_data['price'] = ""

        try:
            num_of_ratings = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[{0}]/div/div/div[2]/div/div[1]/div/a/span'.format(i))
            item_data['num_of_ratings'] = num_of_ratings.text
        except:
            item_data['num_of_ratings'] = ""

        try:
            ranking = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[{0}]/div/div/div[1]/div[1]/span'.format(i))
            item_data['ranking'] = ranking.text
        except:
            item_data['ranking'] = ""

        try:
            rating = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[{0}]/div/div/div[2]/div/div[1]/div/a/i/span'.format(i))
            text = rating.get_attribute("innerHTML")
            parts = text.split()
            numeric_rating = parts[0]
            item_data['ratings out of 5'] = numeric_rating
        except:
            item_data['ratings out of 5'] = ""

        data_list.append(item_data)



# Initial page load
scroll_page()
# Loop through multiple pages
while True:
    try:
        fetch_data_from_page()
        # Find and click the "Next Page" button
        next_page_element = driver.find_element('xpath', '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/ul/li[last()]/a')
        next_page_element.click()
        # Wait for the next page to load
        for _ in range(5):  # You may need to adjust the number of scrolls based on the page
            scroll_page()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[54]/div/div/div[2]/div/a[2]/span/div')))
        scroll_page()  # Scroll to load more content
        # fetch_data_from_page()  # Fetch data from the next page
    except NoSuchElementException:
        # If there is no "Next Page" button, break the loop
        break

# Convert data_list to DataFrame
df = pd.DataFrame(data_list)
df.replace('', pd.NA, inplace=True)
df.dropna(inplace=True)
df.to_csv('amazon_beauty_data.csv', index=False)

print("CSV file saved successfully.")
