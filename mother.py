import time
from threading import Lock, Thread

from scraper import Scraper


class Mother(Thread):
    """This thread manage the list of scrapers threads

    This thread run while the main window.

    """
    TIME = 0
    QUANTITY = 1
    PRICE = 2

    def __init__(self, master=None, timer=1):
        """Initialize the mother thread

        :param timer: time the refresh time of the thread, defaults to 10
        :type timer: int

        """
        Thread.__init__(self)
        self.master = master

        self.running  = False
        self.lock = Lock()

        self.items_selected = []
        self.items_running = {}

        self.scrapers = []
        self.timer = timer


    def run(self):
        """On update compare the user selected list and the list of scraper and stop or start new scraper"""
        self.running = True
        print("[MOTHER] Starting")

        while True:
            time.sleep(self.timer)

            if not self.running:
                print("[MOTHER] Stopping")
                self.stop()
                break

            items_to_run = list(set(self.items_selected) - set(self.items_running.keys()))
            # create all added scrapers 
            new_scrapers = []
            for item_to_run in items_to_run:
                new_scraper = Scraper(item_to_run)

                new_scrapers.append(new_scraper)

            # starting all new scrapers 
            for new_scraper in new_scrapers:
                new_scraper.start()

                self.scrapers.append(new_scraper)

                self.items_running[new_scraper.item_name] = [[], [], []]


            items_to_stop = list(set(self.items_running.keys()) - set(self.items_selected))
            for scraper in self.scrapers:
                # get_data
                if scraper.item_name in items_to_stop:
                    scraper.stop()
                    del self.items_running[scraper.item_name]
                else:
                    data = scraper.get_data()
                    self.items_running[scraper.item_name][self.TIME] += data[self.TIME]
                    self.items_running[scraper.item_name][self.QUANTITY] += data[self.QUANTITY]
                    self.items_running[scraper.item_name][self.PRICE] += data[self.PRICE]

    def stop(self):
        with self.lock:
            for scraper in self.scrapers:
                scraper.stop()
                scraper.join()

            self.running = False

    def set_items_selected(self, items_selected):
        """Use to set the new active item scraper.

        :param item_selected: list of item selected by the user
        :param item_selected: list of string

        """
        with self.lock:
            self.items_selected = items_selected

    def get_data(self):
        """Update plot line with current value"""
        with self.lock:
            return self.items_running

if __name__ == "__main__":
    mother = Mother()
    mother.start()
    mother.set_items_selected(["Glove Case",
        "Gamma Case",
        "Spectrum Case",
        "Clutch Case",
        "Horizon Case",
        "Prisma Case",
        "Chroma Case"])

    mother.join()
