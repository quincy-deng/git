import os
import pandas as pd
import numpy as np
path  =r'F:\BGI100_MGI200\BGI100_MGI200.data'

#合并指定表格
def MergeBac_fungi_parasite(path):
    df = []
    for boot,flnames,files in os.walk(path):
        flnames #no use
        for fl in files:
            if fl.split('_')[0] != 'species' or len(fl.split('_')) != 4 :
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

### 第一步,合并表格并输出到三个平台目录下
def merge_platform(path):
    for i in ['BGI100','MGI200_2557','MGI200_2615']:
        os.chdir(os.path.join(path,i))
        df = MergeBac_fungi_parasite(os.path.join(path,i))
        df = strin_cols(df)
        df = SampleTop10(df)
        df['Group'] = i
        df.to_csv('species.merge.TOP10.txt',sep='\t',index=False)
# merge_platform(path)

### 第二步,合并三个文件用于画PCA
# 生成矩阵文件
def merge_to_matrix(path):
    df = []
    for i in ['BGI100','MGI200_2557','MGI200_2615']:
        os.chdir(os.path.join(path,i))
        df.append(pd.read_csv('species.merge.TOP10.txt',sep='\t',engine='python'))
    df1 =pd.concat(df[0:2])
    df2 = pd.concat([df[0],df[2]])
    df3 = pd.concat(df[1:3])
    os.chdir(path)
    df1.to_csv('bgi100_mgi200_2557.species.merge.TOP10.txt',sep='\t',index=False)
    df2.to_csv('bgi100_mgi200_2615.species.merge.TOP10.txt',sep='\t',index=False)
    df3.to_csv('mgi200_2557_mgi200_2615.species.merge.TOP10.txt',sep='\t',index=False)

merge_to_matrix(path)