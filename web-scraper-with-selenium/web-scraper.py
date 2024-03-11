from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("https://www.amazon.com/Dyson-V10-Allergy-Cordless-Cleaner/dp/B095LD5SWQ/")

title = driver.find_element(by=By.XPATH, value='//span[@id="productTitle"]')
current_price = driver.find_element(by=By.XPATH, value='//div[@id="corePrice_feature_div"]//span[@data-a-color="price"]/span[1]')
image = driver.find_element(by=By.XPATH, value='//div[@id="imgTagWrapperId"]/img')

product_data = {
'title': title.text,
'current_price': current_price.get_attribute('innerHTML'),
'image_url': image.get_attribute('src')
}

print(product_data)
driver.quit()