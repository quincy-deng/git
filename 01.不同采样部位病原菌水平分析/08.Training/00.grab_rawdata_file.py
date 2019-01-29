# 根据表格去数据库寻找文件,将文件转移以患者名称_sampleID文件夹名
import os,shutil
import xlrd
import pandas as pd
from collections import defaultdict,Counter
# >> Read table <<
table=r'D:\0125\08.resultdata\a.华山医院给出NGS结果\12.5重新整理中英文.xlsx'
sheets=xlrd.open_workbook(table).sheet_names()
patientsID={row[0][:10]:row[1] for sheet in sheets for index,row in pd.read_excel(table,sheet_name=sheet)[['标本编号','患者姓名']].iterrows()}
print('华山医院给出表格包含 {} 个sampleID！'.format(len(patientsID.keys())))
#1 到数据库寻找
rawdatapaths = [r'D:\华山医院\01.Rawdata(所有)\华山医院交付数据',r'D:\华山医院\01.Rawdata(所有)\非华山医院交付数据']
rawfiles = defaultdict(list)
for rawdatapath in rawdatapaths:
    {rawfiles[patientsID[fl.split('.')[0][:10]]+'_'+fl.split('.')[0][:10]].append(os.path.join(boot,fl)) for boot,dirs,files in os.walk(rawdatapath) for fl in files if (fl.endswith(('xls','csv','xlsx')) and len(fl.split('.')) in [2,4,5]) if fl.split('.')[0][:10] in patientsID.keys()}
print('找到 {} 个样本!'.format(len(rawfiles.keys())))
print(Counter([len(i) for i in rawfiles.values()]))

os.chdir(r'D:\0125\华山医院整理后病人数据')
[os.mkdir(patients_name) for patients_name,flpath in rawfiles.items() if not os.path.exists(patients_name)]
[shutil.copy(fl,os.path.join(os.getcwd(),patients_name)) for patients_name,flpath in rawfiles.items() for fl in flpath]

# logging:20190125
['17S0587768', '17S0835757','17S0835758', '17S0835759', '17P3249182', '18S4003055', '18S4003074', '17P0587591', '17S0324914', '17P0836072', '18S4003066', '18S400308', '17P0836048', '17P0836005', '17P0587681', '17P0587572', '17S0836876', '18S0064105', '18S0064195'] # 这些sample在所有地方找不到
['17S0587768', '17S0835757', '17S0835758', '17S0835759', '17P3249182', '18S4003055', '18S4003074', '17P0587591', '17S0324914', '17P0836072'] # 这10个是阳性没找到的
# not_found_patientsID2 = {id:patientsID[id] for id in patientsID if id not in [name_id.split('_')[1] for name_id in rawfiles]}
