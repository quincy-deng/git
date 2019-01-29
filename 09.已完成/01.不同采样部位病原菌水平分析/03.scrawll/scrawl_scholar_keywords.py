# -- coding: utf-8 --

# from docopt import docopt
import os
from time import sleep
import random

number_of_results = int(10)#(args['--results']) # number of results to look for on Google Scholar
save_database = 'false' # choose if you would like to save the database to .csv (recommended to correctly visualize the URLs)

path = r'D:\ngs_pathogen_detection_clinical2.csv'

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import chardet
import sys

def get_citations(content):
    out = 0
    if str(content[1]).find('次数') != -1:
        temp = str(content[1]).index('次数') 
        # print(temp,str(content[1])[temp+4])
        for char in range(len(str(content[1])[temp+4:])):
            # print(str(content[1])[temp+4+char])
            if str(content[1])[temp+4+char] =='<':
                out = str(content[1])[temp+3:temp+4+char]
                break
    print(out)
    return int(out)

def get_year(content):
    out = 0
    for char in range(0,len(content)):
        if content[char] == '-':
            out = content[char-5:char-1]
            if not out.isdigit():
                out = 0
    return int(out)

def get_author(content):
    out = 'NoAuthor'
    for char in range(0,len(content)):
        if content[char] == '-':
            out = content[:char-4]
            break
    return out

def get_publication(content):
    out = 'NoJournal'
    for char in range(0,len(content)):
        temp = content.split("-")
        try:
            out = temp[2]
        except: # catch *all* exceptions
            out = "Couldn't retrieve publication"
    return out

def main():
    # Start new session
    # session = requests.Session()

    # Variables
    links = list()
    title = list()
    citations = list()
    year = list()
    rank = list()
    author = list()
    rank.append(0) # initialization necessary for incremental purposes
    publication = list()
    abstract = list()
    # Get content
    compeat = 0
    for n in range(0, number_of_results, 10):
        url = 'https://c.beijingbang.top/scholar?start='+str(n)+'&q='+'ngs pathogen patient -mutations -variants -mutation -variant'.replace(' ','+')
        page = requests.get(url)
        c = page.text 
        c = c.encode('GB18030')
        # c = unicode(c,errors = 'replace')
        # page = page.decode('utf-8')
        #= ('gb2312')
        # exit()
        # print(page.encoding)
        #.decode(page.apparent_encoding,'replace').encode('utf-8')
    
        # #print(text
        # Create parser
        soup = BeautifulSoup(c, 'html.parser') #'html.parser'

        # Get stuff
        mydivs = soup.findAll("div", { "class" : "gs_r" })
        for div in mydivs:
            try:
                links.append(div.find('h3').find('a').get('href'))
            except: # catch *all* exceptions
                links.append('NO LINKS')

            try:
                title.append(div.find('h3').find('a').text)
            except:
                title.append('Could not catch title')

            try:
                abstract.append(div.find('div',{'class' : 'gs_rs'}).text)
            except:
                abstract.append('Could not catch abstract')
            try:
                citations.append(get_citations(div.findAll('div',{'class' : 'gs_fl'})))
            except:
                citations.append('No citation')
            year.append(get_year(div.find('div',{'class' : 'gs_a'}).text))
            author.append(get_author(div.find('div',{'class' : 'gs_a'}).text))
            rank.append(rank[-1]+1)
            publication.append(get_publication(div.find('div',{'class' : 'gs_a'}).text))
            sleep(random.random()*3)
            compeat += 1
            print(compeat)
    print(year)
    data = (title,author,year,publication,citations,links,abstract)

    o = open(path,'w',encoding = 'utf-8')
    headers = ['Title','Author','Year','Journal','Citation','Link','Abstact']
    o.write(headers[0])
    for header in headers[1:]:
        o.write(','+header)
    o.write('\n')
    for i in range(len(year)):
        for df in data[:-1]:
            o.write(str(df[i])+',')
        o.write(data[-1][i])
        o.write('\n')

    # save_database=True
    # # Create a dataset and sort by the number of citations
    # data = pd.DataFrame(list(zip(author, title, citations, year, links,publication, abstract)), index = rank[1:], columns=['Author', 'Title', 'Citations', 'Year', 'Source', 'Publication', 'Abstract'])
    # data = data.rename_axis('Rank', axis="columns")

    # data_ranked = data.sort_values('Citations', ascending=False)

    # # Save results
    # if save_database:
    #     data_ranked.to_csv(path, encoding='utf-8')

    print('Done!')
if __name__ =='__main__':
    main()
