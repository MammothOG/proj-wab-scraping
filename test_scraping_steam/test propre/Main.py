# -*- coding: utf-8 -*-
"""
Created on Sun May  3 20:42:56 2020

@author: Yohan Arnoux
"""


import time
import urllib.parse
from threading import Thread, Lock
import pandas as pd
from selenium import webdriver
import fenetre 
import poller 
import tkinter as tk
from threading import Thread

def start_scrapping(e):
    poller.scrapping_start(app.liste_choix)
        

        
        
root = tk.Tk()
app = fenetre.MainWindow(master=root)   

recup_case = fenetre.RecupCase()
liste_choix=app.liste_choix
name_case = recup_case.recup()



app.valide.bind('<Button-1>', start_scrapping)
app.leave.bind('<Button-1>', root.destroy)
app.mainloop()





