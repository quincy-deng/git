import os
import pandas as pd
import numpy as np
path1=r'D:\华山医院\b.NGS结果.组织分类'
path2=r'D:\华山医院\03.matrix(各组织和合并)\各组织matrix'
for i in os.listdir(path1):
    # 处理一个组织
    organ =dict()
    os.chdir(path1)
    df = pd.read_table(i,engine='python',header=None)
    df.columns=['sampleid','ngs_result']
    # 以species作为键,sampleid为值,没有阳性species的跳过
    for _,row in df.iterrows():
        if str(row[1]).startswith('(') or str(row[1]).startswith('无'):
            # organ.setdefault('NA',[]).append(row[0])
            continue
        for ptg in row[1].split(';'):
            try:
                ptg.split(',')[1]
            except:
                continue
            if ptg.split(',')[1].startswith('Mycobacterium'):
                organ.setdefault('Mycobacterium_tuberculosis_complex_group',[]).append(row[0])
                continue
            organ.setdefault(ptg.split(',')[1],[]).append(row[0])

    os.chdir(path2)
    for fl in os.listdir():
        if fl.startswith(i.split('.')[0]):
            matrix_df=pd.read_table(fl,engine='python',index_col='#Sample')
    print(matrix_df.shape)
    # 合并结核分枝杆菌
    merge_col=list()
    for col in matrix_df.columns.tolist():
        if col.startswith('Mycobacterium'):
            merge_col.append(col)
    matrix_df['Mycobacterium_tuberculosis_complex_group']=sum(matrix_df[i] for i in merge_col)
    matrix_df.drop(merge_col,axis=1,inplace=True)

    # 创建df
    out_df=pd.DataFrame(columns=['sampleid','positive','negative'])
    out_df['sampleid']=organ.keys()
    # print(organ.keys())
    out_df.set_index('sampleid',inplace=True)
    
    for col in matrix_df.columns.tolist():
        # 输出一行ptg,阳性,阴性
        if col in out_df.index.tolist():
            for sampleid,SDSMRN in zip(matrix_df.index.tolist(),matrix_df[col]):
                if SDSMRN==0 or int(SDSMRN)==0:
                    continue
                elif sampleid in organ[col]:
                    if isinstance(out_df.loc[col,'positive'],float):
                        out_df.loc[col,'positive'] =str(int(SDSMRN))
                    else:
                        out_df.loc[col,'positive'] += ','+str(int(SDSMRN))
                else:
                    if isinstance(out_df.loc[col,'negative'],float):
                        out_df.loc[col,'negative'] =str(int(SDSMRN))
                    else:
                        out_df.loc[col,'negative'] += ','+str(int(SDSMRN))
    out_df.dropna(axis=0,how='all',inplace=True)
    out_df.to_csv(r'D:\华山医院\0109.组织SDMSRN(阳性阴性)\pos_negative.{}.xls'.format(i.split('.')[0]),sep='\t')
