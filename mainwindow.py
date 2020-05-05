import json
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


class MainWindow(tk.Frame):

    CASE_NAME = "case_name.json"

    def __init__(self, master):
        tk.Frame.__init__(self, master, background="blue")
        self.master = master
        self.pack(fill=tk.Y, side=tk.LEFT)

        self.button = tk.Button(self, text="Display", command=self.on_display)
        self.button.pack(side=tk.BOTTOM)

        self.cases = []
        self.listbox_items = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox_items.pack(fill=tk.Y, side=tk.LEFT)
        self.load_items()


        # data sample
        data = {'Country': ['US','CA','GER','UK','FR'],
                    'GDP_Per_Capita': [45000,42000,52000,49000,47000]
                }
        df = DataFrame(data, columns=['Country','GDP_Per_Capita'])
        # create figure here 
        xAxis = [10,1,20] 
        yAxis = [2,3,3] 

        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.bar(xAxis,yAxis, color = 'lightsteelblue')

        self.graph = FigureCanvasTkAgg(self.figure, master)

        self.tk_graph = self.graph.get_tk_widget()

        self.tk_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_items(self):
        with open(str(self.CASE_NAME)) as json_data:
            self.cases = json.load(json_data)
        
        for case in self.cases:
            self.listbox_items.insert(tk.END, case)
    
    def on_display(self):
        print("CLICKED")

        self.items_selected = [self.cases[int(index)] for index in self.listbox_items.curselection()]
        print(self.items_selected)

if __name__ == "__main__":
    root = tk.Tk()

    app = MainWindow(master=root)

    app.mainloop()
