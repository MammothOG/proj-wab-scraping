import time
import urllib.parse
from threading import Thread, Lock

import pandas as pd
from selenium import webdriver

class DataPoller(Thread):
    def __init__(self, name, condition=None, timer=0, refresh=10):
        Thread.__init__(self)
        self.lock = Lock()
        self.running = False

        self.game_id = 730
        self.item_name = name
        self.condition = condition

        self.start_time = 0
        self.timer = timer
        self.refresh = refresh

        # url_name = "{} ({})".format(self.item_name, self.condition)
        url_name = "{}".format(self.item_name)
        parsed_name = urllib.parse.quote(url_name)
        self.adresse = "https://steamcommunity.com/market/listings/{game_id}/{item_name}" \
                        .format(game_id=self.game_id, item_name=parsed_name)
        
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(self.adresse)

        self.buf = []


    timer_check = lambda self: time.time() - self.start_time > self.timer

    def run(self):
        counter = 0
        self.running = True
        self.start_time = time.time()
        try:
            while True:
                if not self.running or self.timer_check():
                    self.stop()
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
            print("stop thread")

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

        self.buf.append([time_stamp, quantity, price])

    def get_data_frame(self):
        with self.lock:
            print("get data")
            col = ["time", "quantity", "price"]
            data_frame = pd.DataFrame(data=self.buf, columns=col)

            self.buf = []
            
            return data_frame



if __name__ == "__main__":
    poller_prisma = DataPoller("Prisma 2 Case", timer=1200)
    poller_phoenix = DataPoller("Operation Phoenix Weapon Case", timer=1200)

    poller_prisma.start()
    poller_phoenix.start()

    while poller_prisma.is_running() and poller_phoenix.is_running():
        time.sleep(10)

    df_prisma = poller_prisma.get_data_frame()
    df_phoenix = poller_phoenix.get_data_frame()
    
    df_prisma.to_csv("prisma.csv")
    df_phoenix.to_csv("phoenix.csv")
