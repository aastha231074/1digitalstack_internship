import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup

# Configure Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')  # Run headless if desired
driver = webdriver.Chrome(options=options)

def get_product_info(driver, url):
    asin = url.split('/dp/')[1].split('/')[0]
    print(asin)

    try:
        title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        ).text.strip()
    except (TimeoutException, NoSuchElementException):
        title = ""

    try:
        rating_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'acrCustomerReviewText'))
        )
        rating = rating_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        rating = ""

    try:
        rating_value_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-hook="rating-out-of-text"]'))
        )
        rating_value = rating_value_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        rating_value = ""

    try:
        five_star_percent_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'percent of reviews have 5 stars')]"))
        )
        five_star_percent = five_star_percent_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        five_star_percent = ""

    try:
        four_star_percent_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'percent of reviews have 4 stars')]"))
        )
        four_star_percent = four_star_percent_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        four_star_percent = ""

    try:
        three_star_percent_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'percent of reviews have 3 stars')]"))
        )
        three_star_percent = three_star_percent_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        three_star_percent = ""

    try:
        two_star_percent_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'percent of reviews have 2 stars')]"))
        )
        two_star_percent = two_star_percent_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        two_star_percent = ""

    try:
        one_star_percent_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'percent of reviews have 1 stars')]"))
        )
        one_star_percent = one_star_percent_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        one_star_percent = ""

    try:
        bought_in_past_month_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'social-proofing-faceout-title-tk_bought'))
        )
        bought_in_past_month = bought_in_past_month_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        bought_in_past_month = ""

    try:
        discounted_price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.a-price span.a-price-whole'))
        )
        discounted_price = discounted_price_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        discounted_price = ""

    try:
        positive_ratings_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brand-snapshot-flex-row') and contains(., 'positive ratings')]"))
        )
        positive_ratings = positive_ratings_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        positive_ratings = ""

    try:
        recent_orders_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brand-snapshot-flex-row') and contains(., 'recent orders')]"))
        )
        recent_orders = recent_orders_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        recent_orders = ""

    try:
        years_on_amazon_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'brand-snapshot-flex-row') and contains(., 'years on Amazon')]"))
        )
        years_on_amazon = years_on_amazon_element.text.strip()
    except (TimeoutException, NoSuchElementException):
        years_on_amazon = ""

    return (asin, title, rating_value, rating, five_star_percent, four_star_percent,
            three_star_percent, two_star_percent, one_star_percent, bought_in_past_month,
            discounted_price, positive_ratings, recent_orders, years_on_amazon)

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def fetch_product_page(driver, url):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            return True
        except WebDriverException as e:
            print(f"Error fetching {url}: {e}. Retrying ({retries+1}/{max_retries})...")
            retries += 1
            time.sleep(2 + retries * 2)  # Exponential backoff
    return False

URL = "https://www.amazon.in/gp/bestsellers/beauty"
# URL = "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_pg_2_beauty?ie=UTF8&pg=2"

driver.get(URL)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='a-link-normal']"))
)

scroll_to_bottom(driver)
soup = BeautifulSoup(driver.page_source, "html.parser")
links = soup.find_all("a", class_='a-link-normal', href=True)

data = []
base_url = "https://www.amazon.in"

for link in links:
    if "/dp/" in link['href']:
        product_url = base_url + link['href']
        if fetch_product_page(driver, product_url):
            (asin, title, rating_value, rating, five_star_percent, four_star_percent,
             three_star_percent, two_star_percent, one_star_percent, bought_in_past_month,
              discounted_price, positive_ratings, recent_orders, years_on_amazon
             ) = get_product_info(driver, product_url)
            if title:  # Only append if title is not empty
                html_content = driver.page_source
                data.append({
                    'ASIN': asin,
                    'Title': title,
                    'Rating Value': rating_value,
                    'Rating': rating,
                    '5 Star Reviews': five_star_percent,
                    '4 Star Reviews': four_star_percent,
                    '3 Star Reviews': three_star_percent,
                    '2 Star Reviews': two_star_percent,
                    '1 Star Reviews': one_star_percent,
                    'Bought in Past Month': bought_in_past_month,
                    'Discounted Price': discounted_price,
                    'Positive Ratings': positive_ratings,
                    'Recent Orders': recent_orders,
                    'Years on Amazon': years_on_amazon,
                })
            time.sleep(random.uniform(1, 3))  # Random delay to mimic human browsing

# Create an empty dataframe
df = pd.DataFrame(columns=['ASIN', 'Title', 'Rating Value', 'Rating', '5 Star Reviews',
                           '4 Star Reviews', '3 Star Reviews', '2 Star Reviews',
                           '1 Star Reviews', 'Bought in Past Month', 'Discounted Price',
                           'Positive Ratings', 'Recent Orders', 'Years on Amazon'])
for product in data:
    df = df.append(product, ignore_index=True)
df.to_csv('amazon_products.csv', index=False)

# Process the data as needed (e.g., save to a dataframe or a file)
for product in data:
    print("ASIN:", product['ASIN'])
    print("Title:", product['Title'])
    print("Rating Value:", product['Rating Value'])
    print("Rating:", product['Rating'])
    print("4 Star Reviews:", product['4 Star Reviews'])
    print("3 Star Reviews:", product['3 Star Reviews'])
    print("2 Star Reviews:", product['2 Star Reviews'])
    print("1 Star Reviews:", product['1 Star Reviews'])
    print("Bought in Past Month:", product['Bought in Past Month'])
    print("Discounted Price:", product['Discounted Price'])
    print("Positive Ratings:", product['Positive Ratings'])
    print("Recent Orders:", product['Recent Orders'])
    print("Years on Amazon:", product['Years on Amazon'])
    print("\n" + "-"*50 + "\n")

