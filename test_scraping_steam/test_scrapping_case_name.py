# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:19:50 2020

@author: Yohan Arnoux
"""


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests as rq
import time
import json



    
        
class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1600x900")
        self.master.resizable(width=False, height=False)
        self.pack()

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="left", fill='y')
        self.load_scrollbar("Case_name.json")
        self.scrollbar.config(command=self.listbox.yview)
        self.leave = tk.Button(self, text='valider')
        self.leave.bind('<ButtonRelease-1>',self.clic)
        self.leave.pack(side="bottom", fill="both")
        self.name_choose=""
 

    def load_scrollbar(self, file_name):
    
        with open(str(file_name)) as json_data:
                cases = json.load(json_data)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        for case in cases:
            self.listbox.insert("end", case)
        #self.listbox.bind('<ButtonRelease-1>',self.clic)
        self.listbox.pack(side="left")
          ## on associe l'évènement "relachement du bouton gauche la souris" à la listbox
    def clic(self,e):
        i=self.listbox.curselection()  ## Récupération de l'index de l'élément sélectionné
        
        self.name_choose = self.listbox.get(i)  ## On retourne l'élément (un string) sélectionné
        

    

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
        page = rq.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
            
        element = soup.find_all('span', class_="market_listing_item_name" )
        for k in element:
            table_case.append(k.text)
        with open('Case_name.json', 'w') as fp:
                json.dump(table_case, fp)
        return table_case



"""recup_case = RecupCase()
name_case = recup_case.recup()

root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()

name_choose=app.name_choose"""
