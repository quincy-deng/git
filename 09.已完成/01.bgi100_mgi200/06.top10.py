import os
import pandas as pd
import numpy as np
path  =r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试'

#合并指定表格
def MergeBac_fungi_parasite(path):
    df = []
    for boot,flnames,files in os.walk(path):
        flnames #no use
        for fl in files:
            if fl.split('_')[0] != 'genus' or len(fl.split('_')) != 4 or fl.split('_')[-1].split('.')[0]=='virus':
                continue
            print(fl)
            df.append(pd.read_csv(os.path.join(boot,fl),sep='\t',engine='python'))
    df2 = pd.concat(df,axis=1)
    df2 = df2.loc[:,~df2.columns.duplicated()] 
    return df2

#去掉df全为0的列
def strin_cols(df):
    for cols in df:
        try:
            if sum(list(df[cols]))==0:
                df.pop(cols)
        except:
            pass
    return df

# 选取每一行排名前十的列
def SampleTop10(df):
    col_index = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        arr = np.array(temp)
        col_index = col_index + list(arr.argsort()[-10:])
    col_index =list(set(col_index))
    new_df = df.iloc[:,col_index]
    return new_df
def merge_platform(path):
    for i in ['BGI100','MGI200_2557','MGI200_2615']:
        os.chdir(os.path.join(path,i))
        df = MergeBac_fungi_parasite(os.path.join(path,i))
        df = strin_cols(df)
        df = SampleTop10(df)
        df['Group'] = i
        df.to_csv('merge.TOP10.txt',sep='\t',index=False)

# 生成矩阵文件
def merge_to_matrix(path):
    df = []
    for i in ['BGI100','MGI200_2557','MGI200_2615']:
        os.chdir(os.path.join(path,i))
        df.append(pd.read_csv('merge.TOP10.txt',sep='\t',engine='python'))
    df =pd.concat(df)
    os.chdir(path)
    df.to_csv('merge.TOP10.txt',sep='\t',index=False)

merge_to_matrix(path)