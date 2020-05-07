import time
import urllib.parse
from threading import Thread, Lock
import pandas as pd
from selenium import webdriver

import tkinter as tk
class DataPoller(Thread):
    def __init__(self, name, condition=None, timer=0, refresh=10):
        Thread.__init__(self)
        self.lock = Lock()
        self.running = False

        self.game_id = 730 #id de cs go (url)
        self.item_name = name #idem
        self.condition = condition #pour arme 

        self.start_time = 0 #cb de temps le programme doit tourner
        self.timer = timer
        self.refresh = refresh #temps de rafraichissement de scraping

        # url_name = "{} ({})".format(self.item_name, self.condition)
        url_name = "{}".format(self.item_name)
        parsed_name = urllib.parse.quote(url_name) #convertir le nom en nom pour url
        self.adresse = "https://steamcommunity.com/market/listings/{game_id}/{item_name}" \
                        .format(game_id=self.game_id, item_name=parsed_name)
        
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(self.adresse)

        self.buf = []


    timer_check = lambda self: time.time() - self.start_time > self.timer and self.timer > 0  #temps écouler depuis l'ouverture du programme (regard si supérieur au timer imposé)

    def run(self):
        self.running = True
        self.start_time = time.time()
        try:
            while True:
                if not self.running or self.timer_check():
                    # self.stop()
                    break
                
                with self.lock:
                    self.scrap_data()

                time.sleep(self.refresh)
            
        finally:
            self.driver.close()
            print("close driver")

    def stop(self):
        with self.lock:
            self.running = False
            print("stop ", self.item_name)

    def is_running(self):
        with self.lock:
            return self.running

    def scrap_data(self):

        # building link to locate price and quantity of  items
        sale = "market_commodity_buyrequests"
        xpath_quantity = "//div[@id='{}']/span[1]".format(sale)
        xpath_price = "//div[@id='{}']/span[2]".format(sale)

        # get element
        quantity_element = self.driver.find_element_by_xpath(xpath_quantity)
        price_element = self.driver.find_element_by_xpath(xpath_price)

        # clean element 
        time_stamp = int(time.time())
        quantity = int(quantity_element.text)
        price = float(price_element.text.replace("$", ""))

        self.buf.append([time_stamp, quantity, price])#time_stamp en seconde depuis le 1er janvier 1970
        # self.buf["time"].append([time_stamp, quantity, price])

    def get_data(self): #remplir la dataframe avec le buf puis le vider
        with self.lock:
            buf = list(self.buf)
            self.buf = []
            return buf