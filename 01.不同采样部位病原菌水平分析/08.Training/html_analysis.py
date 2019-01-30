import os,shutil
import xlrd
import pandas as pd
from collections import defaultdict,Counter
import numpy as np
# >> Read table <<
table=r'D:\0125\08.resultdata\a.华山医院给出NGS结果\12.5重新整理中英文.xlsx'
sheets=xlrd.open_workbook(table).sheet_names()
# row[0][:10]:{i.split(',')[1]:i.split(',')[0] for i in row[1].split(';')} 
patientsID={row[0][:10]:{i.split(',')[1]:i.split(',')[0] for i in row[1].split(';') if len(i.split(','))>1} for sheet in sheets[:-1] for index,row in pd.read_excel(table,sheet_name=sheet)[['标本编号','new_NGS_result']].iterrows() if not row[1].startswith('无')}
os.chdir(r'D:\0125\华山医院整理后病人数据2.rankheader')
dataids = {i.split('_')[1]:i for i in os.listdir()}
for idt,ptgs in patientsID.items():
    if idt in dataids:
        os.chdir(dataids[idt])
        fls = os.listdir()
        for ptg,typ in ptgs.items():
            # 病原文件类型
            fl = [i for i in fls if not i.endswith('xlsx') if i.split('.')[1]==typ]
            if any(fl):
                df = pd.read_table(fl[0],engine='python',encoding='gbk')
                # species 类型
                spe = [i for i in df['Species'] if i==ptg]
                genus = [i for i in df['Species'] if i.split('_')[0]==ptg.split('_')[0]]
                if any(spe):
                    index,x = list(df['Species']).index(spe[0]),list(df['SDSMRN'])
                    sdsmrn = x[index]
                    rank = np.array(x)[np.argsort(-np.array(x))].index(int(sdsmrn))+1
                elif any(genus):
                    x,y = list(df['Species']),list(df['SDSMRN'])
                    index = [x.index(i) for i in genus]
                    sdsmrn = sum([x[i] for i in index])
                    new_list = y+[sdsmrn]
                    rank = np.array(new_list)[np.argsort(-np.array(new_list))].index(int(sdsmrn))+1
                else:
                    print(ptg,idt)
    else:
        print('lack {} sample file!'.format(idt))