# 合并包含data.stat的文件,提取'#SampleID','Total','Short'|'Frate','Clean','Hg19_rate'信息.
import pandas as pd
import os
import numpy as np
import re

def obtain_data_stat_paths():
    data_dir = r'D:\上机和病原组共享'
    for boot,dirs,files in os.walk(data_dir):
        for fl in files:
            if re.search('data.stat',fl) and fl[0]!='.':
                yield os.path.join(boot,fl)

def merge_data_stat():
    for fl in list(obtain_data_stat_paths()):
        try:
            df =pd.read_table(fl,engine='python',usecols=['#SampleID','Total','Frate','Clean','Hg19_rate'])
            df['Frate'] = np.array([float(i.rstrip('%'))/100 for i in list(df['Frate'])])
            df['Hg19_rate']= np.array([float(i.rstrip('%'))/100 for i in list(df['Hg19_rate'])])
            yield df
        except:
            try:
                df =pd.read_table(fl,engine='python',usecols=['#SampleID','Total','Short','Clean','Hg19_rate'])
                df['Short'] = np.array(['{:.4f}'.format(x/y) for x,y in zip(list(df['Short']),list(df['Total']))])
                df['Hg19_rate']= np.array([float(i.rstrip('%'))/100 for i in list(df['Hg19_rate'])])
                df.rename(columns={'Short':'Frate'},inplace=True)
                yield df
            except:
                try:
                    df =pd.read_csv(fl,engine='python',usecols=['#SampleID','Total','Frate','Clean','Hg19_rate'])
                    df['Frate'] = np.array([float(i.rstrip('%'))/100 for i in list(df['Frate'])])
                    df['Hg19_rate']= np.array([float(i.rstrip('%'))/100 for i in list(df['Hg19_rate'])])
                    yield df
                except:
                    print(fl)

def merge_df():
    df = pd.concat(list(merge_data_stat()))
    # 过滤长度小于10的ID
    df = df[df['#SampleID'].str.len()>9]
    # 取ID的前10位
    df['#SampleID'] = df['#SampleID'].str.slice(0,10)
    # 删除重复的ID
    df.drop_duplicates('#SampleID','first',inplace=True)
    df.to_csv(r'D:\华山医院\test_merge_data.stat.xls',sep='\t',index=False)

merge_df()
