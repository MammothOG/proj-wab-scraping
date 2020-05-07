import json
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

import mother


class MainWindow(tk.Frame):
    """The main and unique window that display curve."""

    CASE_NAME = "case_name.json"

    def __init__(self, master):
        tk.Frame.__init__(self, master, background="blue")
        self.master = master

        # initialize tkinter layout
        self.pack(fill=tk.Y, side=tk.LEFT)

        self.button = tk.Button(
            master=self, text="Display", command=self.on_display)
        self.button.pack(side=tk.BOTTOM)

        # initialize of the Listbox
        self.cases = []
        self.listbox_items = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox_items.pack(fill=tk.BOTH, side=tk.LEFT)
        self.load_items()

        # initialize figure
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([], [])

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

    def on_display(self):
        """Call then a user click on display

        Send to the mother thread the list of case selected by the user in the list box.
        
        """
        self.items_selected = [
            self.cases[int(index)] for index in self.listbox_items.curselection()]

        print("item selected = ", self.items_selected)

        self.mother.set_items_selected(self.items_selected)

    def close_window(self):
        self.mother.stop()
        self.mother.join()

    def refresh_graph(self):

        print("refresh")
        time, price, quantity = self.mother.update_plot()
        self.ax.lines.pop(0)
        self.ax.plot(time, price)

        self.graph.draw()
        
        self.master.after(2000, self.refresh_graph)


if __name__ == "__main__":
    root = tk.Tk()

    app = MainWindow(master=root)

    def on_closing():
        print("window closed")
        app.close_window()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app.refresh_graph()
    app.mainloop()
