# -- coding: utf-8 --
import os
import random
import re
from time import sleep

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

import scrawl_scholar_keywords as test4

mendelay_file = r'C:\Users\邓秋洋\Documents\WeChat Files\huanghujian1990\Files\MyCollection.bib'
# Variables
DOIs, titles, years, authors, abstracts, journals = [],[],[],[],[],[]

def get_year(part):
        # print(part)
        year = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('year = ',line):
                        year = line[8:-1]
        return year

def get_DOI(part):
        doi = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('doi = ',line):
                        doi = line[7:-2]
        return doi

def get_title(part):
        title = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('title = ',line):
                        title = line[10:-2]
        return title

def get_author(part):
        author = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('author = ',line):
                        author = line[10:-2]
        return author

def get_abstract(part):
        abstract = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('abstract = ',line):
                        abstract =line[12:-2]
        return abstract

def get_journal(part):
        journal = 'NOT_FIND'
        for line in part.split('\n'):
                if re.search('journal = ',line):
                        journal = line[11:-2]
                elif re.search('booktitle = ',line):
                        journal = line[13:-2]
        return journal

f = open(mendelay_file,'r',encoding = 'utf-8')
all_artical = f.read().split('\n@')[1:]


for part in all_artical:
        DOIs.append(get_DOI(part))
        titles.append(get_title(part))
        years.append(get_year(part))
        authors.append(get_author(part))
        abstracts.append(get_abstract(part))
        journals.append(get_journal(part))
results = (titles,DOIs,journals,years,authors,abstracts)
print(DOIs)

#输出csv格式文件
file_path = r'C:\Users\邓秋洋\Documents\WeChat Files\huanghujian1990\Files\get\ngs_pathogen_detection_clinical1114.csv'
data = pd.DataFrame(list(zip(titles,journals,years,authors,abstracts)),columns=['Title', 'Journal', 'Year', 'Author','Abstract'])
data_ranked = data.sort_values('Year', ascending=False)
data_ranked.to_csv(file_path, encoding='utf-8')
# citations1 = [33, 122, 82, 11, 147, 4, 116, 5, 70, 42, 82, 30, 46,
#  84, 89, 161, 17, 0, 276, 76, 117, 279, 64, 251, 141, 1561, 165, 
#  535, 101, 152, 0, 136, 179, 25, 77, 60, 312, 44, 34, 232, 24, 215,
#   81, 132, 1065, 1, 58, 143, 1, 0, 118, 75]
# citations2 = [2, 50, 150, 208, 15, 0, 147, 209, 61, 107, 1, 98, 178,
#  8, 56, 84, 158, 73, 94, 76, 113, 18, 1780, 83, 249, 6, 459, 215, 37,
#   153, 39, 178, 128, 105, 244, 159, 207, 126, 60, 61, 58, 0, 18]
# citations3 = [18, 542, 63, 33, 189, 227, 1526, 68, 36, 53, 51, 52, 
# 224, 18, 151, 72, 94, 119, 60, 116, 79, 93, 82, 89, 77, 97, 1, 189,
#  79, 46, 325, 607, 55, 3, 43, 98, 156, 26, 68, 196, 62, 88, 23, 157, 64, 75]
# citations4 = [47, 70, 161, 154, 35, 189, 117, 36, 30, 48, 46, 58, 68, 
#  316, 5, 67, 44, 21, 34, 68, 23, 52, 42, 26, 113, 67, 50, 98, 44, 50, 31,
#   39, 101, 65, 78, 133, 226, 219, 46, 551, 94]
# citations = []
# for doi in DOIs[182:]:
#         if doi == 'NOT_FIND':
#                 citations.append(0)
#                 continue
#         url = 'https://c.beijingbang.top/scholar?start=0&q='+doi
#         page = requests.get(url)
#         page.encoding = 'gbk'
#         c = page.text
#         soup = BeautifulSoup(c, 'html.parser')
#         mydivs = soup.findAll("div", { "class" : "gs_r" })
#         if mydivs == []:
#                 continue
#         citations.append(test4.get_citations(mydivs[0].findAll('div',{'class' : 'gs_fl'})))
#         print(citations)
#         sleep(random.random()*3)
# print(citations)
