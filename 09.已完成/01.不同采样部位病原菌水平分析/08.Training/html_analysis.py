import os
import re 
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser,self).__init__()
        self.__parsedata='' #设置一个空状态
    def handle_starttag(self, tag, attrs):
        if ('class','gs_rt') in attrs:
            # print(attrs)
            self.__parsedata = 'name'
        if ('class', 'gs_fl') in attrs:
            # print(attrs)
            self.__parsedata = 'cite'
    def handle_endtag(self, tag):
        if tag =='h3' or tag == 'div':
            self.__parsedata = ''
    def handle_data(self, data):
        if self.__parsedata =='name':
            if data =='\n' or data =='[HTML]':
                pass
            else:
                # pass
                print('文献名称:%s'%data.rstrip())
        if self.__parsedata =='cite':
            if re.search('被引用次数',data):
                print(data)
parser = MyHTMLParser()





html_path = r'C:\Users\邓秋洋\Documents\WeChat Files\huanghujian1990\Files\get'
for html in [os.path.join(html_path, i) for i in os.listdir(html_path)]:
    f = open(html,'rb')
    data = f.read()
    parser.feed(data.decode('utf-8'))
    exit()