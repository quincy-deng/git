import pandas as pd
import os,xlrd

result_path=r'D:\1114医院感染数据\12.5重新整理中英文.xlsx'
sheet_names = xlrd.open_workbook(result_path).sheet_names()
df = pd.read_excel(result_path,sheet_name=sheet_names[0])
ngs_culture_Positive = {}
for x,y in zip(df['标本编号'].tolist(),df['new_NGS_result'].tolist()):
    ngs_culture_Positive[x] = y
print(ngs_culture_Positive)
# for sheet_name in sheet_names:
#     df = pd.read_excel(result_path,sheet_name=sheet_name)
