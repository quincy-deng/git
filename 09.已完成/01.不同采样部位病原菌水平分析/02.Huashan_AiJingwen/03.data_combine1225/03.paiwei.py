
# coding = utf-8
import os,sys
sys.stdout = open(r'D:\华山医院\1225数据整理需求\logging.xls','w')
import re 
import numpy as np
import pandas as pd
import logging
def obtain_file_list():
    data_dir = r'D:\华山医院\01.华山医院NGS测序报告\1227.merge'
    for boot,dirs,files in os.walk(data_dir):
        for fl in files:
            yield os.path.join(boot,fl)

# 表头齐全
def sdsmrn_reabu_rank(ptg,data_df):
    try:
        sdsmrn,reabu,sdsmrng=data_df.loc[ptg,['SDSMRN','Re_Abu','SDSMRNG']]
    # 找不到致病菌
    except:
        # 找属
        try:
            genuses = data_df['Genus']
            if ptg in genuses:
                index = genuses.index(ptg)
                new_ptg = data_df.index.tolist()[index]
                sdsmrn,reabu,sdsmrng = data_df.loc[new_ptg,['SDSMRN','Re_Abu','SDSMRNG']]
        # 属也找不着
        except:
            print('{}:No found {} in Species and Genus!'.format(list(data_df['#Sample'])[0],ptg))
            return 0,0,-1
    ls_sdsmrng=list(map(lambda x:int(x), filter(lambda x: x!='-',list(set(list(data_df['SDSMRNG']))))))
    x = np.array(ls_sdsmrng)
    rank=list(x[np.argsort(-x)]).index(int(sdsmrng))+1       
    return sdsmrn,reabu,str(rank)
def SDsmrn(ptg,data_df):
    sdsmrn=0
    try:
        sdsmrn==data_df.loc[ptg,['SDSMRN']]
    except:
        try:
            genuses = data_df['Genus']
            if ptg in genuses:
                index = genuses.index(ptg)
                new_ptg = data_df.index.tolist()[index]
                sdsmrn= data_df.loc[new_ptg,'SDSMRN']
        except:
            print('{}:No found {} in Species and Genus!'.format(list(data_df['#Sample'])[0],ptg))
            return -1
    return sdsmrn
def main():
    fl_list = list(obtain_file_list())
    data_sampleIDs = [os.path.split(i)[1].split('.')[0] for i in fl_list]
    header_file =r'D:\华山医院\1225数据整理需求\header3.xls'
    header_df = pd.read_excel(header_file,index_col='标本编号')
    sampleIDs = header_df.index.tolist()
    for sampleID in sampleIDs:
        results=header_df.loc[sampleID,'NGS病原体信息']
        if re.search('无致病菌',results):
            continue
        if sampleID in data_sampleIDs:
            try:
                data_df = pd.read_table(fl_list[data_sampleIDs.index(sampleID)],engine='python',index_col='Species')
            except:
                print('{}\tempty file!\n'.format(sampleID))
                continue
            # 表头是齐全的情况
            if len(data_df.columns.tolist())==5:
                if len(results.split(';'))==1:
                    ptg = results.split(',')[1]
                    sdsmrn,reabu,rank=sdsmrn_reabu_rank(ptg,data_df)
                    if rank ==0:
                        continue
                    header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
                else:
                    try:
                        ptgs = [i.split(',')[1] for i in results.split(';')]
                    except:
                        ptg='_'.join(results.split(';'))
                        sdsmrn,reabu,rank=sdsmrn_reabu_rank(ptg,data_df)
                        header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
                    sdsmrns,reabus,ranks=[],[],[]
                    if ranks ==0:
                        continue
                    for ptg in ptgs:
                        sdsmrn,reabu,rank = sdsmrn_reabu_rank(ptg,data_df)
                        sdsmrns.append(sdsmrn)
                        reabus.append(reabu)
                        ranks.append(rank)
                    sdsmrn,reabu,rank = ','.join(map(str,sdsmrns)),','.join(map(str,reabus)),','.join(map(str,ranks))
                    header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
            # 缺少丰度和SDSMRNG,只找SDSMRN
            else:
                if len(results.split(';'))==1:
                    ptg = results.split(',')[1]
                    sdsmrn = SDsmrn(ptg,data_df)
                    if sdsmrn ==-1:
                        continue
                    header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,0,0]  
        else:
            print('{}\t Lack data file\n'.format(sampleID))
    header_df.to_excel(r'D:\华山医院\1225数据整理需求\header5.xls')

main()
# print(len(daijiejue))

# o.write('\n'.join(daijiejue))
