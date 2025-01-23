import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up ChromeDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=options)

driver.get('https://www.math.nsysu.edu.tw/~problem/')

print(driver.page_source)

time.sleep(5)

driver.quit()