# import requests,re,collections
# from bs4 import BeautifulSoup
# import pandas as pd
# from scipy.misc import imread
# from time import sleep
# # choose your demand
# Max_page = 45
# key = 'ngs+pathogen+detection+clinical'
# start = '2000'
# final = '2018'
# text_title = 'GStitle.txt'
# text_keyword = 'GSkw.txt'
# path = 'ngs_pathogen_detection_clinical.csv'
# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

# def get_citations(content):
#     out = 0
#     for char in range(0,len(content)):
#         if content[char:char+9] == 'Cited by ':
#             init = char+9
#             for end in range(init+1,init+6):
#                 if content[end] == '<':
#                     break
#             out = content[init:end]
#     return int(out)

# def get_year(content):
#     for char in range(0,len(content)):
#         if content[char] == '-':
#             out = content[char-5:char-1]
#             break
#     if not out.isdigit():
#         out = 0
#     return int(out)

# def get_author(content):
#     for char in range(0,len(content)):
#         if content[char] == '-':
#             out = content[2:char-1]
#             break
#     return out

# def get_publication(content):
#     for char in range(0,len(content)):
#         temp = content.split("-")
#         try:
#             out = temp[2]
#         except: # catch *all* exceptions
#             out = "Couldn't retrieve publication"
#     return out

# #virable
# links, titles, citations, years, ranks, authors, publications, abstracts = [],[],[],[],[],[],[],[]
# ranks.append(0) # initialization necessary for incremental purposes

# # grab titles
# for i in range(Max_page):
#     url = 'https://c.beijingbang.top/scholar?start='+str(i*10)+'&q='+key+'&as_ylo='+start+'&as_yhi='+final
#     start_html = requests.get(url,  headers=headers)
#     Soup = BeautifulSoup(start_html.text, 'lxml')
#     # all_title = Soup.find_all('h3', class_="gs_rt")
#     # all_year = Soup.find_all('div', class_="gs_a")
#     # all_sited = Soup.find_all('div', class_="gs_fl")
    
#     # for a in all_title:
#     #     ranks.append(ranks[-1]+1)
#     #     title = a.get_text()
#     #     titles.append(title)
#     # for a in all_year:
#     #     year = a.get_text()
#     #     years.append(year)
#     # for a in all_sited:
#     #     cite = a.get_text()
#     #     if re.search('被',cite):
#     #         citations.append(cite)
#     # sleep(0.5)
#     mydivs = Soup.find_all('h3', class_="gs_rt")
#     # print(mydivs)
#     for div in mydivs:
#         try:
#             links.append(div.find('h3').find('a').get('href'))
#         except:
#             links.append('https://c.beijingbang.top/scholar?start='+str(i*10)+'&q='+key+'&as_ylo='+start+'&as_yhi='+final)
#         # all_year = div.find_all('div', class_="gs_a")
#         # print(all_year)
#         # exit()
#         citations.append(get_citations(str(div.find_all('div', class_="gs_fl"))))
#         years.append(get_year(div.find('div',class_="gs_a")))
#         authors.append(get_author(div.find_all('div',class_="gs_a")))
#         publications.append(get_publication(div.find('div', class_="gs_a")))
#         ranks.append(ranks[-1]+1)
# print(citations,authors)
# exit()
# save_database=True
# # Create a dataset and sort by the number of citations
# print(titles)
# data = pd.DataFrame(list(zip(titles, citations, years,)), index = ranks[1:], columns=['Title', 'Citations', 'Year'])
# data = data.rename_axis('Rank', axis="columns")

# data_ranked = data.sort_values('Citations', ascending=False)

# # Save results
# if save_database:
#     data_ranked.to_csv(path, encoding='utf-8')

# print('Done!')
f = open(r'E:\2017-20180814病原下机&报告数据\3.正式报告2018年\201808\20180814\N100005326.result.v3.2.2\data.stat.xls')
print(f.readline().split())