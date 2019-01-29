import pandas as pd
import numpy as np

def export_df():
    sampleID = r'D:\华山医院\1225数据整理需求\总表修改.xlsx'
    header_file = r'D:\华山医院\1225数据整理需求\header2.xls'
    df_sampleid = pd.read_excel(sampleID,use_col=['标本编号'])
    sampleIDs = [i[:10] for i in list(df_sampleid['标本编号']) if not isinstance(i,float)]
    df_header = pd.read_excel(header_file,index_col='标本编号')
    header = ['标本编号']+df_header.columns.tolist()
    print(df_header.shape)
    df_sample,df_miss = [],[]
    for sample in sampleIDs:
        try:
            df_sample.append([sample]+list(df_header.loc[sample,:]))
        except:
            df_miss.append([sample]+[np.nan for i in range(11)])
    df = df_miss+df_sample
    merge_df=pd.core.frame.DataFrame(df,columns=header)
    # merge_df.to_excel(r'D:\华山医院\1225数据整理需求\表头修改.xlsx',index=False)

def test():
    data = r'D:\华山医院\1225数据整理需求\总表修改.xlsx'
    header = r'D:\华山医院\1225数据整理需求\表头修改.xlsx'
    df1=pd.read_excel(data,index_col='标本编号')
    print(df1.columns.tolist())
    df2=pd.read_excel(header)
    for i in range(24):
        df2.loc[i,'患者姓名'] = df1.loc[df2.loc[i,'标本编号'],'患者姓名']
        df2.loc[i,'标本类型'] = df1.loc[df2.loc[i,'标本编号'],'标本类型']
    df2.to_excel(r'D:\华山医院\1225数据整理需求\表头修改2.xlsx',index=False)
test()