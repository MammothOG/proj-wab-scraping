import json
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import mother
import random as rd

import numpy as np


class MainWindow(tk.Frame):
    """The main and unique window that display curve."""
    

    CASE_NAME = "case_name.json"

    UPMS = 1000 # Update per milliseconds

    chunk_per_graph = 25

    def __init__(self, master):
        tk.Frame.__init__(self, master, background="blue")
        self.master = master
        self.configure(bg='#2B2E3A')
        # initialize tkinter layout
        self.pack(fill=tk.BOTH, side=tk.TOP)

        self.button = tk.Button(
        master=self, text="Display", command=self.on_display)
        self.button.pack(side=tk.BOTTOM)

        # initialize of the Listbox
        self.cases = []
        self.listbox_items = tk.Listbox(self, selectmode=tk.MULTIPLE, bg="#2B2E3A", fg ="#C3C4C6", selectbackground ='#3C3D40')
        self.listbox_items.pack(fill=tk.BOTH, side=tk.LEFT)
        self.load_items()

        # initialize figure
        self.figure = plt.Figure(figsize=(10, 9), dpi=100, facecolor ='#2B2E3A')
        self.ax_quantity = self.figure.add_subplot(111)
        self.ax_quantity.set_ylabel('Quantité', color='#C3C4C6')
        self.ax_quantity.set_xlabel('Dates', color='#C3C4C6')
        self.ax_quantity.patch.set_facecolor('#575A63')
        self.ax_quantity.plot([], [])
        self.ax_price = self.ax_quantity.twinx()
        self.ax_price.set_ylabel('Prix', color='#C3C4C6')
        # self.ax_quantity.yaxis.set_ticks(np.arange(0, 1, 1))
        # self.ax_quantity.xaxis.set_ticks(np.arange(0, 1, 1))

        # create the graph
        self.graph = FigureCanvasTkAgg(self.figure, master=self)
        self.tk_graph = self.graph.get_tk_widget()
        self.tk_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # starting mother thread
        self.mother = mother.Mother(master=self, timer=1)
        self.mother.start()

    def load_items(self):
        """Load a case list in json file and insert case name in the list box."""
        with open(str(self.CASE_NAME)) as json_data:
            self.cases = json.load(json_data)

        for case in self.cases:
            self.listbox_items.insert(tk.END, case)

        self.link_item_to_color()

    def on_display(self):
        """Call then a user click on display

        Send to the mother thread the list of case selected by the user in the list box.
        
        """
        self.items_selected = [
            self.cases[int(index)] for index in self.listbox_items.curselection()]

        print("[Main Window] item selected = {}".format(self.items_selected))

        self.mother.set_items_selected(self.items_selected)

    def close_window(self):
        self.mother.stop()
        self.mother.join()

    def refresh_graph(self):
        """Plot The graph with the new data send by the poller.py"""

        datas = self.mother.get_data()

        self.ax_quantity.lines = []

        # self.ax_price.cla()
        # self.ax_quantity.cla()

        max_price = 1
        max_quantity = 1
        min_time = 0
        max_time = 1
        for item, data in datas.items():
            time_list = []
            price_list = []
            quantity_list = []

            for plot in data:
                time_list.append(plot[self.mother.TIME])
                price_list.append(plot[self.mother.PRICE])
                quantity_list.append(plot[self.mother.QUANTITY])

            self.ax_quantity.plot(time_list,
                    quantity_list,
                    color=self.items_colors[item],
                    alpha=0.3,
                    label=item)
            
            self.ax_price.scatter(time_list,
                    price_list,
                    color=self.items_colors[item], marker = '+', label=item +" price")

            self.ax_quantity.tick_params(axis='x',labelrotation=30,
                            labelsize=7)
            
            self.ax_quantity.legend()

            if len(quantity_list) > 0 and max(quantity_list) > max_quantity:
                max_quantity = max(quantity_list)
            if len(price_list) > 0 and max(price_list) > max_price:
                max_price = max(price_list)
            if len(time_list) > self.chunk_per_graph :
                min_time = time_list[-self.chunk_per_graph]    
                max_time = time_list[-1]
        
        self.ax_quantity.xaxis.set_ticks(np.arange(min_time, max_time, 2))
        self.ax_quantity.yaxis.set_ticks(np.arange(0, max_quantity*3, max_quantity/20))
        self.ax_price.yaxis.set_ticks(np.arange(0, max_price*1.5, max_price/20))

        self.graph.draw()
        
        self.master.after(self.UPMS, self.refresh_graph)

    def link_item_to_color(self):
        self.items_colors = {}
        for case in self.cases:
            self.items_colors[case] = (rd.uniform(0, 1), rd.uniform(0, 1),
                    rd.uniform(0, 1))


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
