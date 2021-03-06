import time
import urllib.parse
from threading import Thread, Lock
import pandas as pd
from selenium import webdriver
import datetime
import re
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import tkinter as tk


class Scraper(Thread):
    """The data scrapper"""

    TIME = 0
    QUANTITY = 1
    PRICE = 2

    def __init__(self, name, timer=0, refresh_rate=1):
        """Initialize and setup the scraper

        :param name: exact item name the item in english
        :type name: str
        :param timer: thread execution time in second if 0 then the threa run indefinitely, default to 0
        :type timer: int
        :param refresh_rate: the time interval between scraping, default to 1
        :type refresh_rate: float

        """

        Thread.__init__(self)
        self.lock = Lock()
        self.running = False

        self.game_id = 730 # id de cs go (url)
        self.item_name = name # idem

        self.start_time = 0 # cb de temps le programme doit tourner
        self.timer = timer
        self.refresh_rate = refresh_rate # temps de rafraichissement de scraping

        url_name = "{}".format(self.item_name)
        parsed_name = urllib.parse.quote(url_name) # convertir le nom en nom pour url
        self.adresse = "https://steamcommunity.com/market/listings/{game_id}/{item_name}" \
                .format(game_id=self.game_id, item_name=parsed_name)

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(self.adresse)

        self.reset_buffer()

        self.quantity = 0
        self.price = 0.0

    timer_check = lambda self: time.time() - self.start_time > self.timer and self.timer > 0

    def run(self):
        print("[{}] Starting scraper".format(self.item_name))

        self.running = True
        self.start_time = time.time()

        while True:
            time_start_processing = time.time()

            if not self.running or self.timer_check():
                break

            with self.lock:
                self.scrap_data()

            processing_duration = time.time() - time_start_processing

            assert self.refresh_rate > processing_duration, "PC slow up the refresh rate"

            time.sleep(self.refresh_rate - processing_duration)
        print("[{}] Closing Chrome".format(self.item_name))
        self.driver.close()

    def stop(self):
        with self.lock:
            self.running = False
            print("[{}] Stopping scraper".format(self.item_name))

    def is_running(self):
        with self.lock:
            return self.running

    def scrap_data(self):
        """Starting to scrap data of the selected item on the steam market """

        # building link to locate price and quantity of  items
        sale = "market_commodity_forsale_table"
        xpath_price = "//div[@id='{}']/table/tbody/tr/td[1]".format(sale)
        xpath_quantity = "//div[@id='{}']/table/tbody/tr/td[2]".format(sale)


        # get element
        try:

            quantity_element = self.driver.find_element_by_xpath(xpath_quantity)
            price_element = self.driver.find_element_by_xpath(xpath_price)

            # clean element
            self.quantity = int(quantity_element.text)
            self.price = float(re.findall('\d*\.?\d+', price_element.text)[0])

        except StaleElementReferenceException as e:
            print("[{}] Warning : {}".format(self.item_name, e))

        now = datetime.datetime.now()
        time_stamp = now.strftime('%H:%M:%S:%f')
        # print("[{}] {} => {}".format(time_stamp, self.quantity, self.price))

        self.buf[self.TIME].append(time_stamp)
        self.buf[self.QUANTITY].append(self.quantity)
        self.buf[self.PRICE].append(self.price)

    def get_data(self): #remplir la dataframe avec le buf puis le vider
        with self.lock:
            buf = list(self.buf)
            self.reset_buffer()
            return buf

    def reset_buffer(self):
        self.buf = [[], [], []]

class element_has_xpaht(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class

    """
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        element = driver.find_element(*self.locator)   # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False

if __name__ == "__main__":

    # scraper = Scraper("Sticker | Skadoodle (Gold) | Krakow 2017", timer=10)
    scraper = Scraper("Sticker | AdreN (Gold) | Krakow 2017", timer=0)
    scraper.start()

    scraper.join()
