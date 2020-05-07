import time
from threading import Lock, Thread

from poller import DataPoller


class Mother(Thread):

    def __init__(self, timer=10):
        Thread.__init__(self)

        self.running  = False
        self.lock = Lock()

        self.items_selected = []
        self.items_running = {}

        self.items_scraper = []
        self.timer = timer

    def run(self):
        print("lauch thread")
        self.running = True
        
        i = 0
        while True:
            time.sleep(self.timer)

            i += 1

            print(i)

            if i == 6:
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
                    self.items_running[scraper.item_name].extend(data)

    def stop(self):
        with self.lock:
            for scraper in self.items_scraper:
                scraper.stop()

                self.running = False

    def set_items_selected(self, items_selected):
        with self.lock:
            self.items_selected = items_selected

if __name__ == "__main__":
    mother = Mother()
    mother.start()
    mother.set_items_selected(["Glove Case","Gamma Case","Spectrum Case", "Clutch Case", "Horizon Case", "Prisma Case", "Chroma Case"])

    mother.join()