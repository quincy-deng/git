#!python
# coding:utf-8
import os
import sys
import re
import urllib.request 
import time
import json
import pandas as pd 
from bs4 import BeautifulSoup
import requests

# def get_id():
#     id =pd.read_excel(r"C:\Users\邓秋洋\Documents\K.xlsx")
#     return id["BioSample"]

def get_data():
    header = {"Referer":"https://www.ncbi.nlm.nih.gov/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
            }
    req = urllib.request.Request(url='https://morvanzhou.github.io/static/scraping/basic-structure.html',headers=header)  
    session = requests.Session()
    url = 'https://scholar.google.com/scholar?start=1&q='+'ngs+pathogen+detection+clinical'
    page = session.get(url)
    c = page.content
    print(c)
    #'https://scholar.google.com/scholar?start=20&hl=en&q={}'.format(id)
    f = urllib.request.urlopen(url).read().decode('utf-8') 
    print(f)
    exit()
    soup = BeautifulSoup(f, 'html5lib')
    biosample = soup.find_all('div', attrs={"class": "gs_rs"}).get_text()
    dicta = {"biosample":biosample}
    attributes = soup.find(name='table', attrs={"class": "docsum"})
    for each in attributes.find_all('tr'):
        if each is not None:
            print(each.th, each.td)
            dicta[each.th.get_text()]=each.td.get_text()
        else:
            pass
    return dicta

if __name__ == "__main__":
    id = 'ngs & pathogen & detection & clinical'
    time.sleep(1)
    try:
        info = get_data()
    except:
        info=None
    print(info, end='\n')
    