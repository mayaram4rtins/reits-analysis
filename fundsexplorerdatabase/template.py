from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO 

url = "https://www.fundsexplorer.com.br/ranking"

# Initialize a Selenium WebDriver (make sure to have the appropriate driver installed, e.g., chromedriver)
driver = webdriver.Chrome()  # You can use other drivers like Firefox, etc.

# Fetch the URL using Selenium
driver.get(url)

# Wait for the page to load completely (You may need to adjust the wait time according to the page loading speed)
time.sleep(10)  # Wait for 10 seconds (adjust as needed)

# Scroll down using JavaScript
driver.execute_script("window.scrollBy(0, 500);")

# Wait for some time to let the page load
time.sleep(2)

# If the filtering mechanism involves interacting with HTML elements (e.g., buttons, dropdowns), locate those elements and interact with them to remove filters
# For example, if there's a dropdown for selecting a category and you want to select "All categories":
dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'colunas-ranking__select-button')))
dropdown.click()
all_categories_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.colunas-ranking__selectItem + .checkmark")))
all_categories_option.click()

# Wait for some time to let the page load
time.sleep(10)

# Get the page source after JavaScript has executed
html = driver.page_source

# Close the Selenium WebDriver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Finding the table by its HTML tag (e.g., <table>)
table = soup.find('table')

if table:
    # Extracting data from the table and converting it into a DataFrame
    df = pd.read_html(StringIO(str(table)))[0]  # [0] is used to select the first table if there are multiple tables
    
    # Displaying the DataFrame
    df.to_excel('fundsexplorerranking.xlsx', index=False)
else:
    print("No table found on the webpage.")