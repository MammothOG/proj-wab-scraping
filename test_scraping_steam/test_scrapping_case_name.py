# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:22:21 2020

@author: Yohan Arnoux
"""


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import test_selenium
from bs4 import BeautifulSoup
import requests as rq
import time



    
        
class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")
        self.load_scrollbar("file_name.json")
        self.scrollbar.config(command=self.listbox.yview)
        self.leave = tk.Button(self, text='Quitter', command=self.master.destroy)
        self.leave.pack(side="bottom", fill="both")

    def load_scrollbar(self, file_name):
        """refresh scroll bar"""
        cases = [] # load json 
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        for case in cases:
            self.listbox.insert("end", case)
        self.listbox.pack(side="left", fill="both")

class Figure(FigureCanvasTkAgg):

    def __init__(self, master=None):
        
        """self.figure = plt.Figure(figsize=(6,5) dpi=100)

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
        # self.ax.set_title("The title for yor chart")"""
    

class RecupCase():
    def __init__(self, master=None):
        self.urlbase="https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730&q=case#p1_default"
        self.table_case = []
        self.page = 25
        
    def recup(self):
        
        table_case = self.table_case
        url = self.urlbase
        """for i in range(1,26):
            time.sleep(6)"""
            
        print(url)
        page = rq.get(url)
        print(page)
        soup = BeautifulSoup(page.text, 'lxml')
            
        element = soup.find_all('span', class_="market_listing_item_name" )
        for k in element:
            table_case.append(k.text)
    
        return table_case



# recup_case = RecupCase()
# name_case = recup_case.recup()
# print(name_case)

root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
