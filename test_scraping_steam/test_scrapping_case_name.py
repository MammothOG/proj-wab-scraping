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
    """This is the main window of our programm"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
    
        self.master.title("Mon programme de bourse")
    
        
class Plot(FigureCanvasTkAgg):

    def __init__(self,name_case, master=None):
      
        self.window = tk.Tk()
        self.window.geometry('1920x1080')
        self.window.resizable(0,0)
        self.case=name_case

        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.window, yscrollcommand=self.scrollbar.set)
        for i in self.case:
            self.listbox.insert("end", i)
        self.listbox.pack(side="left", fill="both")

        self.scrollbar.config(command=self.listbox.yview)

        self.window.mainloop()
        
        
        """self.figure = plt.Figure(figsize=(6,5), dpi=100)

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
    

class recup_case():
    def __init__(self,master=None):
        self.urlbase="https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730&q=case#p"
        self.table_case=[]
        self.page=25
        
        for i in range(1,self.page+1):
            time.sleep(10)
            
            url='https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730&q=case#p{page}_default'.format(page=str(i))
            print(url)
            page = rq.get(url)
            print(page)
            soup = BeautifulSoup(page.text, 'lxml')
            
            element = soup.find_all('span',class_="market_listing_item_name" )
            for k in element:
                self.table_case.append(k.text)
            element.attrs = {}
        print(self.table_case)




name_case=recup_case()
#app = Plot(name_case)

#root.mainloop()