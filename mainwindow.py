import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


class MainWindow(tk.Frame):
    """This is the main window of our programm"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack
    
        self.master.title("Mon programme de bourse")

class Plot(FigureCanvasTkAgg):

    def __init__(self, master=None):
        self.figure = plt.Figure(figsize=(6,5), dpi=100)

        super().__init__(self.figure, master)

        self.ax = self.figure.add_subplot(111)

        # data sample
        data = {'Country': ['US','CA','GER','UK','FR'],
                    'GDP_Per_Capita': [45000,42000,52000,49000,47000]
                }
        self.df = DataFrame(data, columns=['Country','GDP_Per_Capita'])

        # create figure here 
        xAxis = [10,1,20] 
        yAxis = [2,3,3] 
        self.ax.bar(xAxis,yAxis, color = 'lightsteelblue')

        self.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        # self.df.plot(kind="bar", legend=True, ax=self.ax)
        # self.ax.set_title("The title for yor chart")


root = tk.Tk()
app = Plot(master=root)
root.mainloop()
