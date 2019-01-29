import os,sys
sys.stdout = open(r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/华山医院/1225数据整理需求/logging2.xls','w')
import re 
import numpy as np
import pandas as pd

def obtain_file_list():
    data_dir = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/华山医院/1227.merge'
    for boot,dirs,files in os.walk(data_dir):
        for fl in files:
            yield os.path.join(boot,fl)

def main():
    fl_list = list(obtain_file_list())
    data_sampleIDs = [os.path.split(i)[1].split('.')[0] for i in fl_list]
    header_df = pd.read_excel(r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/华山医院/1225数据整理需求/header5.xls',index_col='标本编号')
    sampleIDs = header_df.index.tolist()
    for sampleID in sampleIDs:
        results=header_df.loc[sampleID,'NGS病原体信息']
        if re.search('无致病菌',results):
            # print('无致病菌')
            continue
        if sampleID in data_sampleIDs:
            try:
                data_df = pd.read_table(fl_list[data_sampleIDs.index(sampleID)],engine='python',index_col='Species')
            except:
                print('{}\tempty file!'.format(sampleID))
                continue
            # 表头是齐全的情况
            if len(data_df.columns.tolist())==5:
                if len(results.split(';'))==1:
                    ptg = results.split(',')[1]
                    if ptg in data_df.index.tolist():
                        sdsmrn,reabu,sdsmrng=data_df.loc[ptg,['SDSMRN','Re_Abu','SDSMRNG']]
                    elif ptg in list(data_df['Genus']):
                        sdsmrn,reabu,sdsmrng=data_df.loc[data_df.index.tolist()[list(data_df['Genus']).index(ptg)],['SDSMRN','Re_Abu','SDSMRNG']]
                    else:
                        print('{}\t Not found {} in genus or Species'.format(sampleID,ptg))
                        continue
                    try:
                        ls_sdsmrng=list(map(lambda x:int(x), filter(lambda x:str(x)!='nan',filter(lambda x: x!='-',list(set(list(data_df['SDSMRNG'])))))))
                        x = np.array(ls_sdsmrng)
                        rank=list(x[np.argsort(-x)]).index(int(sdsmrng))+1  
                    except:
                        rank = np.nan    
                    # print('Normal')
                    header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
                else:
                    try:
                        ptgs = [i.split(',')[1] for i in results.split(';')]
                    except:
                        ptg='_'.join(results.split(';'))
                        # sdsmrn,reabu,rank=sdsmrn_reabu_rank(ptg,data_df)
                        # print('Normal')
                        header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
                    sdsmrns,reabus,ranks=[],[],[]
                    for ptg in ptgs:
                        if ptg in data_df.index.tolist():
                            sdsmrn,reabu,sdsmrng=data_df.loc[ptg,['SDSMRN','Re_Abu','SDSMRNG']]
                        elif ptg in list(data_df['Genus']):
                            sdsmrn,reabu,sdsmrng=data_df.loc[data_df.index.tolist()[list(data_df['Genus']).index(ptg)],['SDSMRN','Re_Abu','SDSMRNG']]
                        else:
                            print('{}\t{}'.format(sampleID,ptg))
                            continue
                        ls_sdsmrng=list(map(lambda x:int(x), filter(lambda x:str(x)!='nan',filter(lambda x: x!='-',list(set(list(data_df['SDSMRNG'])))))))
                        x = np.array(ls_sdsmrng)
                        try:
                            rank=list(x[np.argsort(-x)]).index(int(sdsmrng))+1    
                        except:
                            print('{}'.format(sampleID))
                            continue   
                        sdsmrns.append(sdsmrn)
                        reabus.append(reabu)
                        ranks.append(rank)
                    sdsmrn,reabu,rank = ','.join(map(str,sdsmrns)),','.join(map(str,reabus)),','.join(map(str,ranks))
                    # print('Normal')
                    header_df.loc[sampleID,['致病病原体SDSMRN','致病病原体丰度','致病病原体排序（病原体所在属sdsmrng在总谱中（细菌+真菌+寄生虫+病毒）的排位）']]=[sdsmrn,reabu,rank]
            # 缺少丰度和SDSMRNG,只找SDSMRN
            else:
                if len(results.split(';'))==1:
                    ptg = results.split(',')[1]
                    if ptg in data_df.index.tolist():
                        sdsmrn=data_df.loc[ptg,'SDSMRN']
                    else:
                        print('{}\t{}'.format(sampleID,ptg))
                        continue
                    # print('Normal')
                    try:
                        header_df.loc[sampleID,'致病病原体SDSMRN']=sdsmrn
                    except:
                        print(header_df.loc[sampleID,'致病病原体SDSMRN'],sampleID,'marker')
                else:
                    ptgs = [i.split(',')[1] for i in results.split(';')]
                    for ptg in ptgs:
                        if ptg in data_df.index.tolist():
                            sdsmrn=data_df.loc[ptg,'SDSMRN']
                        else:
                            print('{}\t{}'.format(sampleID,ptg))
                            continue
                        sdsmrns.append(sdsmrn)
                    sdsmrn = ','.join(map(str,sdsmrns))
                    # print('Normal')
                    header_df.loc[sampleID,'致病病原体SDSMRN']=sdsmrn
        else:
            print('{}\t Lack data file'.format(sampleID))
    header_df.to_excel(r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/华山医院/1225数据整理需求/header6.xls')

main()