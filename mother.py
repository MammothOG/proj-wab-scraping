import time
from threading import Lock, Thread

from poller import DataPoller


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

        self.items_scraper = []
        self.timer = timer

    def run(self):
        """On update compare the user selected list and the list of scraper and stop or start new scraper"""
        self.running = True
        
        while True:
            time.sleep(self.timer)

            if not self.running:
                print("stop mothead")
                self.stop()
                break
            
            print(self.items_running, self.items_selected)

            items_to_run = list(set(self.items_selected) - set(self.items_running.keys()))
            for item_to_run in items_to_run:
                # lauch titem_to_run
                data_poller = DataPoller(item_to_run)
                data_poller.start()

                self.items_scraper.append(data_poller)

                self.items_running[item_to_run] = []

            items_to_stop = list(set(self.items_running.keys()) - set(self.items_selected))
            for scraper in self.items_scraper:
                # get_data
                if scraper.name in items_to_stop:
                    scraper.stop()
                    del self.items_running[scraper.name]
                else:
                    data = scraper.get_data()
                    self.items_running[scraper.item_name] += data

            with self.lock:
                self.update_plot()

    def stop(self):
        with self.lock:
            for scraper in self.items_scraper:
                scraper.stop()

            self.running = False

    def set_items_selected(self, items_selected):
        """Use to set the new active item scraper.

        :param item_selected: list of item selected by the user
        :param item_selected: list of string

        """
        with self.lock:
            self.items_selected = items_selected

    def update_plot(self):
        """Update plot line with current value"""
        
        items_data= {}
        time_list = []
        price_list = []
        quantity_list = []

        for items, data in self.items_running.items():
            for plot in data:
                time_list.append(plot[self.TIME])
                price_list.append(plot[self.PRICE])
                quantity_list.append(plot[self.QUANTITY])
                
                items_data[items]=([plot[self.TIME], plot[self.PRICE], plot[self.QUANTITY]])
              

        return items_data
# if __name__ == "__main__":
#     mother = Mother()
#     mother.start()
#     mother.set_items_selected(["Glove Case","Gamma Case","Spectrum Case", "Clutch Case", "Horizon Case", "Prisma Case", "Chroma Case"])

#     mother.join()