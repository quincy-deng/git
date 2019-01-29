# libraries
from matplotlib.cbook import flatten
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os

dpath = r'F:\BGI100_MGI200\BGI100_MGI200.data\种交集与排名结果'
os.chdir(dpath)
suffix = {}
for fl in os.listdir():
    suf  = fl.split('_')[-1].split('.')[0]
    suffix.setdefault(suf,[]).append((fl.split('_')[-2],fl))


for k,v in suffix.items():
    data = []
    for bm,fl in v:
        df = pd.read_table(fl)
        cols = df.columns.tolist()
        data.append([list(df[i]) for i in cols])
    x_pos = max(map(lambda x:len(x[0]),data))+1
    figure, axes = plt.subplots(3, 1)
    for a,d in zip(flatten(axes),data):
        # set color 
        color_bar = {'a':'#75D701','b':'#EFDC05','c':'#E53A40','ab':'#090707','ac':'#379392','bc':'#4FB0C6','abc':'#6C49B8'}
        # Choose the height of the bars
        bars,colors=d
        print(colors)
        height = range(len(bars)+1)[::-1][:-1]
        y_pos = np.arange(len(bars))+1
        
        # Create bars
        a.bar(y_pos,height,width=0.5,color = [color_bar[i] for i in colors])
        a.set_xlim(left=0.0,right=x_pos)
        # Rotation of the bars names
        # a.set_xticks(y_pos)
        # a.set_xticklabels(bars,fontsize='8',rotation=90)
        
    figure.suptitle(k)
    plt.show()
    exit()
