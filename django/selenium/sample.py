import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By

# x. ブラウザの新規ウィンドウを開く
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get('https://www.4gamer.net/')
time.sleep(6)
print(driver.current_url)

driver.find_element(by=By.LINK_TEXT, value='PC').click()
time.sleep(6)
print(driver.current_url)
