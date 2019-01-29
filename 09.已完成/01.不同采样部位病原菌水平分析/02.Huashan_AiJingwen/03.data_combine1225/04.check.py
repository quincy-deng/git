import os,re
import pandas as pd
import numpy as np
import math

def check():
    header4=r'D:\华山医院\1225数据整理需求\header5.xls'
    df = pd.read_excel(header4,index_col='标本编号')
    for index,col in df.iterrows():
        if not re.search('无致病菌',list(col)[3]):
            # print(list(col)[-3])
            
            if isinstance(list(col)[-3],str):
                # print(list(col)[-3])
                continue
            if list(col)[-3]>0:
                continue
            yield index

samples = list(check())
print(len(samples))