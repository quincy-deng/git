import pandas as pd
import os
import numpy as np
def read_data():
    header_file = r'D:\华山医院\1225数据整理需求\ajw12.27表头修改2.xlsx'
    data_stat_file = r'D:\华山医院\test_merge_data.stat.xls'
    data_stat_file2 = r'D:\华山医院\merge_data.stat.xls'
    df1 = pd.read_excel(header_file)
    df1['标本编号']=df1['标本编号'].str.slice(0,10)
    df1.drop_duplicates('标本编号','first',inplace=True)
    df2 = pd.read_table(data_stat_file,engine='python')
    df3 = pd.read_table(data_stat_file2,engine='python')
    df4 = pd.concat([df2,df3])
    df4.drop_duplicates('#SampleID','first',inplace=True)
    return df1,df4
def analysis_df():
    df1,df2 = read_data()
    sampleIDs = list(df1['标本编号'])
    Raw_reads,Filter_rate,Clean_reads,Hg19_rate = [],[],[],[]
    data_sampleIDS = list(df2['#SampleID'])
    for sampleID in sampleIDs:
        if sampleID in data_sampleIDS:
            index = data_sampleIDS.index(sampleID)
            a,b,c,d = list(df2.iloc[index,1:5])
            Raw_reads.append(a)
            Filter_rate.append(b)
            Clean_reads.append(c)
            Hg19_rate.append(d)
        else:
            Raw_reads.append(np.nan)
            Filter_rate.append(np.nan)
            Clean_reads.append(np.nan)
            Hg19_rate.append(np.nan)
            yield sampleID
            # print(sampleID)
    df1['Raw reads']=np.array(Raw_reads)
    df1['Filter rate']=np.array(Filter_rate)
    df1['Clean reads']=np.array(Clean_reads)
    df1['Hg19 rate'] = np.array(Hg19_rate)
    df1.to_excel(r'D:\华山医院\1225数据整理需求\header3.xls',index=False)
print(list(analysis_df()))