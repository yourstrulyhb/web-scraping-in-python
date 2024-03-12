""" 
Python Web Scraper using selenium
by yourstrulyhb

Reference: https://www.scrapingbee.com/blog/practical-xpath-for-web-scraping/ 

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("https://www.postgresql.org/")


# Get web page details
title = driver.find_element(by=By.XPATH, value='//title')
name = driver.find_element(by=By.XPATH, value='//meta[@name="description"]')
# url = driver.find_element(by=By.XPATH, value='//meta[contains(@name, "url")]')


web_data = {
'title': title,
'name': name,
}

print(web_data)


driver.quit()
