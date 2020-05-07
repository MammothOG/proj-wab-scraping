# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:19:50 2020

@author: Yohan Arnoux
"""
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests as rq
import time
import json
from threading import Thread


class MainWindow(tk.Frame):

    def __init__(self, master=None):
        
        super().__init__(master)
        
        # ?????????????
        import poller
        
       
        self.liste_choix=[]
        self.name_choose=""
        self.master = master
        self.master.geometry("1600x900")
        self.master.resizable(width=False, height=False)
        self.grid()
        
        """self.COUNTER=1
        self.df = poller.scrapping_start(self.liste_choix)
        self.df = self.df.sort_values('time')
        self.df = self.df.reset_index(drop=True)
        self.column_list = list(df.columns)
        self.column_list.remove('quantity')"""
    
        self.fig = plt.figure(figsize=(15, 5))
        self.subplot_1 = self.fig.add_subplot(1,1,1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(row=1, column=5)

        self.scrollbar_choice = tk.Scrollbar(self)
        #self.scrollbar_choice.pack(expand=True, side="left")
        self.scrollbar_choice.grid(row=1, column=1)

        self.scrollbar_choosen = tk.Scrollbar(self)
        #self.scrollbar_choosen.pack(expand=True, side="right", )
        self.scrollbar_choosen.grid(row=3, column=1)

        self.listbox_choosen = tk.Listbox(self, yscrollcommand=self.scrollbar_choosen.set)
        self.listbox_choosen.bind('<Double-Button-1>',self.unload_scrollbar_choosen)
        #self.listbox_choosen.pack(side="right")
        self.listbox_choosen.grid(row=3, column=2)
        
        self.listbox_choice = tk.Listbox(self,width=30, height=25, yscrollcommand=self.scrollbar_choice.set)
        self.listbox_choice.bind('<Double-Button-1>',self.clic)
        #self.listbox_choice.pack(side="left")
        self.listbox_choice.grid(row=1, column=2)

        self.scrollbar_choice.config(command=self.listbox_choice.yview)
        self.load_scrollbar_choice("Case_name.json")
        
        self.scrollbar_choosen.config(command=self.listbox_choosen.yview)
        self.load_scrollbar_choosen()

        self.valide = tk.Button(self, text='valider', width=15, height=2)
        #self.valide.pack(side="bottom", fill="both")
        self.valide.grid(row=2, column =3)

        self.leave = tk.Button(self, text='Quitter', width=15, height=2, command=self.master.destroy)
        #self.leave.pack(side="bottom", fill="both")
        self.leave.grid(row=4, column = 2)
        
    def load_scrollbar_choice(self, file_name):
    
        with open(str(file_name)) as json_data:
                cases = json.load(json_data)
        
        for case in cases:
            self.listbox_choice.insert("end", case)
        
          ## on associe l'évènement "relachement du bouton gauche la souris" à la listbox
        
    def load_scrollbar_choosen(self):
       
        if self.name_choose !="" and self.name_choose not in self.liste_choix:
            self.listbox_choosen.insert("end", self.name_choose)
            self.liste_choix.append(self.name_choose)
        

    ## on associe l'évènement "relachement du bouton gauche la souris" à la listbox    
    def clic(self,e):
        i=self.listbox_choice.curselection()  ## Récupération de l'index de l'élément sélectionné
        self.name_choose = self.listbox_choice.get(i)  ## On retourne l'élément (un string) sélectionné
        self.load_scrollbar_choosen()
        
        
    def unload_scrollbar_choosen(self,e):
        unload_case=self.listbox_choosen.curselection()
        delete = self.listbox_choosen.get(unload_case)
        self.listbox_choosen.delete(unload_case, tk.END)
        self.liste_choix.remove(delete)
        
    """def update_plot(self):
       
        #print(self.fig.get_axes())
        self.fig.delaxes(self.fig.get_axes()[0])
        #print(self.fig.get_axes())
        self.subplot_1 = self.fig.add_subplot(1,1,1)
        date_list = self.df['time'][:COUNTER].to_list()

        for column in column:
            value_list = self.df[column][:COUNTER].to_list()
            line = self.subplot_1.plot_date([date_list],[value_list])
        self.canvas.draw()
        
    def refresh(self):

        

        #print("refresh")
        self.after(500, self.refresh)
        self.update_plot(COUNTER,dataframe,column)
        self.COUNTER+=1"""
        
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



