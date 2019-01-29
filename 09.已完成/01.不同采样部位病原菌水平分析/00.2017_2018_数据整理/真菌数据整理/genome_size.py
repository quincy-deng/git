from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

html = urlopen(
    "https://morvanzhou.github.io/static/scraping/table.html" # 1, https://morvanzhou.github.io/static/scraping/basic-structure.html2, https://morvanzhou.github.io/static/scraping/list.html
).read().decode('utf-8')
# res = re.findall(r'href="(.*?)"', html)#, flags = re.DOTALL)
# print(res)
soup = BeautifulSoup(html, features='lxml')
# print('\n',soup.p)
# all_href = soup.find_all('a')
# # print(all_href)
# all_href = [i['href'] for i in all_href]
# print('\n',all_href)

#use class to narrow search
# month = soup.find_all('li',{"class":"month"})
# # print(month)
# # [print(m.get_text()) for m in month]

# jan = soup.find('ul',{"class":"jan"})
# d_jan = jan.find_all('li')
# [print(m.get_text()) for m in d_jan]
img_links = soup.find_all("img", {"src":re.compile('.*?\.jpg')})
[print(link['src']) for link in img_links]