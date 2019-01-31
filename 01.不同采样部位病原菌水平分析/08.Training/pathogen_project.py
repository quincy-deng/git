# 部分病毒文件有两个header 删掉多余的header
import os
import pandas as pd
os.chdir(r'D:\0125\华山医院整理后病人数据3.rankheader')
fls = [os.path.join(boot,fl) for boot,dirs,fls in os.walk(r'D:\0125\华山医院整理后病人数据2.rankheader') for fl in fls if not fl.endswith('xlsx')]
for fl in fls:
    df = pd.read_table(fl,engine='python',encoding='gbk')
    for index,row in df.iterrows():
        if row[0].startswith('#Sample'):
            print(index,os.path.split(fl)[1])
            df = df.drop(index)
    dirname = os.path.split(os.path.split(fl)[0])[1]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    os.chdir(dirname)
    df.to_csv(os.path.split(fl)[1],encoding='gbk',sep='\t',index=False)
    os.chdir(os.pardir)