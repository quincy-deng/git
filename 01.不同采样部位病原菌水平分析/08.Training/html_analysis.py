import os,shutil
import xlrd
import pandas as pd
from collections import defaultdict,Counter
# >> Read table <<
table=r'D:\0125\08.resultdata\a.华山医院给出NGS结果\12.5重新整理中英文.xlsx'
sheets=xlrd.open_workbook(table).sheet_names()
# row[0][:10]:{i.split(',')[1]:i.split(',')[0] for i in row[1].split(';')} 
patientsID={row[0][:10]:{i.split(',')[1]:i.split(',')[0] for i in row[1].split(';') if len(i.split(','))>1} for sheet in sheets[:-1] for index,row in pd.read_excel(table,sheet_name=sheet)[['标本编号','new_NGS_result']].iterrows() if not row[1].startswith('无')}
for idt,ptgs in patientsID.items():
    if idt in dataids:
        os.chdir(idt)
        temp = [j for i in [pd.read_table(i,encoding='gbk',engine='python')['SDSMRN'].tolist() for i in os.listdir() if not i.endswith('xlsx')] for j in i]