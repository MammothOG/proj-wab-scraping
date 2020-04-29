from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


refresh_time = 10

driver = webdriver.Chrome()
driver.get("https://steamcommunity.com/market/listings/730/Shattered%20Web%20Case")

assert "Marché de la communauté Steam :: Offres pour Shattered Web Case" in driver.title

i = 0

try:
    wait  = WebDriverWait(driver, refresh_time)
    for i in range(10):
        time.sleep(10)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                    "market_commodity_orders_header_promote"))
        )
        print(element.text)
finally:

    assert "No results found." not in driver.page_source
    driver.close()


