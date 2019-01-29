import requests
from bs4 import BeautifulSoup

accession = ['sss','ssss']
page = requests.get('https://www.zhihu.com/search?type=content&q=sss')
c = page.text
print(c)
soup = BeautifulSoup(c,'html.parser')
div = soup.find_all('h2',{'class':'ContentItem-title'})
print(div)
ass = [i.find('a').get('href') for i in div]
print(ass)

# for part in div:
#     links = part.find_all(href = )
# <div class="detail-navlist-title"><a href="http://wiki.jikexueyuan.com/proje
# for accessionid in accession:
#     url = 'https://www.zhihu.com/search?type=content&q='+accessionid
#     page = requests.get(url)
#     c = page.text
#     print(c)
#     soup = BeautifulSoup(c, 'html.parser')
#     print(soup)
#     mydiv = soup.find_all('a')
#     print(mydiv)
#     # for div in mydiv:
#     #     part = soup.find_all('pre',{'classs':'genbank'})
#     #     print(part)
#     exit()