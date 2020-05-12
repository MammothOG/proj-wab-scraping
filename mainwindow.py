import json
import tkinter as tk

import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import mother
import random as rd

import numpy as np


class MainWindow(tk.Frame):
    """The main and unique window that display curve."""

    QUANTITY = 0
    PRICE = 1
    COLOR = 2

    CASE_NAME = "case_name.json"

    UPMS = 1000 # Update per milliseconds

    chunk_per_graph = 41

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.configure(bg='#2B2E3A')
        # initialize tkinter layout
        self.pack(fill=tk.BOTH, expand=True)

        self.frame_button = tk.Frame(self)
        self.frame_button.configure(bg='#2B2E3A')
        self.frame_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.button_display = tk.Button(
                master=self.frame_button, text="Display", command=self.on_display)
        self.button_display.pack(side=tk.LEFT)

        self.button_save = tk.Button(
                master=self.frame_button, text="Save Data", command=self.save_data_csv)
        self.button_save.pack(side=tk.TOP)

        # initialize of the Listbox
        self.cases = []
        self.listbox_items = tk.Listbox(self, selectmode=tk.MULTIPLE, bg="#2B2E3A", fg ="#C3C4C6", selectbackground ='#3C3D40')
        self.listbox_items.pack(fill=tk.BOTH, side=tk.LEFT)
        self.load_items()

        # initialize figure
        self.figure = plt.Figure(dpi=100, facecolor ='#2B2E3A')

        # self.ax_quantity.patch.set_facecolor('#575A63')
        # self.ax_quantity.yaxis.set_ticks(np.arange(0, 1, 1))
        # self.ax_quantity.xaxis.set_ticks(np.arange(0, 1, 1))

        # create the graph
        self.graphics = {}
        self.graph = FigureCanvasTkAgg(self.figure, master=self)
        self.tk_graph = self.graph.get_tk_widget()
        self.tk_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # starting mother thread
        self.mother = mother.Mother(master=self, timer=1)
        self.mother.start()

    def draw_graph(self):
        """Define the list of graphics displayed and give them a color"""

        self.figure.clf()
        for graph_index, item in enumerate(self.items_selected):

            # self.figure.cla()
            ax_quantity = self.figure.add_subplot(len(self.items_selected), 1, graph_index+1)
            ax_quantity.set_ylabel('Quantité', color='#C3C4C6')
            ax_quantity.set_xlabel('Dates', color='#C3C4C6')
            ax_quantity.plot([], [])
            ax_price = ax_quantity.twinx()
            ax_price.set_ylabel('Prix', color='#C3C4C6')

            color = (rd.uniform(0, 1), rd.uniform(0, 1), rd.uniform(0, 1))

            self.graphics[item] = (ax_quantity, ax_price, color)

    def load_items(self):
        """Load a case list in json file and insert case name in the list box."""
        with open(str(self.CASE_NAME)) as json_data:
            self.cases = json.load(json_data)

        for case in self.cases:
            self.listbox_items.insert(tk.END, case)

    def on_display(self):
        """Call then a user click on display

        Send to the mother thread the list of case selected by the user in the list box.
        """


        self.items_selected = [
                self.cases[int(index)] for index in self.listbox_items.curselection()]

        self.draw_graph()

        print("[Main Window] item selected = {}".format(self.items_selected))

        self.mother.set_items_selected(self.items_selected)

    def close_window(self):
        self.mother.stop()
        self.mother.join()

    def refresh_graph(self):
        """Plot The graph with the new data send by the poller.py"""

        self.master.after(self.UPMS, self.refresh_graph)

        datas = self.mother.get_data()

        if len(datas) == len(self.graphics) > 0:
            for item, ax in self.graphics.items():
                # get datas 
                times = datas[item][self.mother.TIME]
                quantities = datas[item][self.mother.QUANTITY]
                prices = datas[item][self.mother.PRICE]

                if len(times) == 0:
                    return

                if len(times) > self.chunk_per_graph:
                    times = times[-self.chunk_per_graph:]
                    quantities = quantities[-self.chunk_per_graph:]
                    prices = prices[-self.chunk_per_graph:]

                # print(times, quantities, prices)

                ax[self.QUANTITY].cla()
                ax[self.PRICE].cla()

                # plot quantity
                ax[self.PRICE].plot(times,
                        prices,
                        color=ax[self.COLOR],
                        label=item+" (quantity = {}, price = {})".format(quantities[-1], prices[-1])
                        )

                # plot price
                ax[self.QUANTITY].bar(times,
                        quantities,
                        color=ax[self.COLOR],
                        alpha=0.3,
                        label=item
                        )


                ax[self.QUANTITY].yaxis.set_ticks(np.arange(0, max(quantities)*5, max(quantities)))
                # TODO marche pas quand *2
                arange_de_merde = np.arange(0, max(prices)*3, max(prices))
                ax[self.PRICE].yaxis.set_ticks(arange_de_merde)

                times_with_step = [t for i, t in enumerate(times) if i%5 ==0]
                ax[self.QUANTITY].xaxis.set_ticks(times_with_step)

                ax[self.PRICE].legend()

            self.graph.draw()

    def save_data_csv(self):
        """Save all data scraped in csv files"""

        print("[Main Window] Data saved")
        datas_to_save = self.mother.get_data()

        for key in datas_to_save:
            date = datas_to_save[key][self.mother.TIME]
            quantity = datas_to_save[key][self.mother.QUANTITY]
            price = datas_to_save[key][self.mother.PRICE]
            df = DataFrame({'Date':date, 'Quantite': quantity, 'Prix': price})

            now = datetime.datetime.now()
            date = now.strftime("%d-%m-%Y_%f")
            df.to_csv("{nom}_{date}.csv".format(nom=key.replace(" ", "-"), date=date))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(master=root)

    def on_closing():
        print("[Main Window] closed")
        app.close_window()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    app.refresh_graph()
    app.mainloop()
