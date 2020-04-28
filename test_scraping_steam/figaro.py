#!/usr/bin/env python
# coding: utf-8

import time
from pandas import DataFrame
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def steam_market_url(page):
    """Generate url of the steam community market"""

    parameter = {
        "itemset": "any",
        "proplayer": "any",
        "stickercapsule": "any",
        "tournamentteam": "any",
        "weapon": "tag_weapon_awp",
        "exterior": "tag_WearCategory0",
        "quality": "tag_normal",
        "appid": "730", # cs go id
        "page": page, # page number 
        "sorted": "name", # sorted by, option : quantity, popular
        "order": "asc", # ascendant or descendant, option : desc
    }
    
    steam_market = "https://steamcommunity.com/market/search"\
            "?q=&category_{appid}_ItemSet%5B%5D={itemset}"\
            "&category_{appid}_ProPlayer%5B%5D={proplayer}"\
            "&category_{appid}_StickerCapsule%5B%5D={stickercapsule}"\
            "&category_{appid}_TournamentTeam%5B%5D={tournamentteam}"\
            "&category_{appid}_Weapon%5B%5D={weapon}"\
            "&category_{appid}_Exterior%5B%5D={exterior}"\
            "&category_{appid}_Quality%5B%5D={quality}"\
            "&appid={appid}"\
            "#p{page}_{sorted}_{order}".format(**parameter)

    return steam_market

def steam_market_data():
    """return items from the Steam community market in dataframe format"""

    col = ["type", "name", "condition", "price", "currency"]

    page_item = []
    page_index = 0
    
    ended = False
    while not ended:

        page_index += 1


        # print("get page")
        page = requests.get(steam_market_url(page_index))
    
        # print("Response : ", page)
        assert page.status_code == 200
        
        soup = BeautifulSoup(page.content, 'lxml')
        
        # get number of items
        element = soup.find('span', id="searchResults_total")
        # print("Number of items", element.get_text())
        
        
        # find item and price in the page
        soup_items = soup.find_all('span', {"class": "market_listing_item_name"})
        soup_prices = soup.find_all('span', {"class": "sale_price"})
        # print(soup_items)
        
        assert len(soup_prices) == len(soup_items)
        
        nb_item = len(page_item)
        for item, price in zip(soup_items, soup_prices):
            formatted_item = re.split("\s\|\s|\s\(|\)", item.get_text())[:3] # TODO improve regex
            formatted_price = price.get_text().replace("$","").split(" ")
            print(formatted_item + formatted_price)
            
            page_item.append(formatted_item + formatted_price)
        
        
        if len(page_item) == nb_item:
            ended = True
        else:
            print("get page = ", page_index) 
            time.sleep(60)
    

    df = pd.DataFrame(page_item, columns=col)
    # converting price in float value
    df["price"] = pd.to_numeric(df["price"])

    # print(df.dtypes)
    return df
    
print(steam_market_data().sort_values(by=['name']))
