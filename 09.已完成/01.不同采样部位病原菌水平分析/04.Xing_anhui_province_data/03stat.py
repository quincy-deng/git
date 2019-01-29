import pandas as pd
import os

wuhan = r'E:\2017-20180814病原下机&报告数据\安徽省立医院（武汉交付）1123-检出列表\安徽省立医院（武汉交付）-检出列表~\data2.xlsx'
xingli = r'C:\Users\邓秋洋\AppData\Local\Packages\microsoft.windowscommunicationsapps_8wekyb3d8bbwe\LocalState\Files\S0\139\安徽省立医院未收到报告列表[1926].xls'

df1 = pd.read_excel(wuhan)
df2 = pd.read_excel(xingli)

col_names2 = list(df2.columns.tolist())
data2 =[]
for i in col_names2:
    data2.append(list(df2[i]))

data1 = []
col_names1 = ['#SampleID','Total','Hg19_rate','Strin_bac','Strin_vir','Strin_fungi','Strin_pro']
for i in col_names1:
    data1.append(list(df1[i]))

ngs_id = list(set(df1['#SampleID'])&set(df2['NGS编号']))
index1 = [list(df1['#SampleID']).index(i) for i in ngs_id]
index2 = [list(df2['NGS编号']).index(i) for i in ngs_id]
newdata2 = {}
for i in range(len(data2)):
    temp_list = []
    for n in index2:
        temp_list.append(data2[i][n])
    newdata2[col_names2[i]]=temp_list

for i in range(len(data1)):
    temp_list = []
    for n in index1:
        temp_list.append(data1[i][n])
    if i == 0:
        continue
    newdata2[col_names1[i]] = temp_list

new_df = pd.DataFrame(data = newdata2)
t_list = list(new_df['NGS编号'])
# with pd.ExcelWriter(r'E:\2017-20180814病原下机&报告数据\安徽省立医院（武汉交付）1123-检出列表\data2.stat.xlsx') as writer:
#     new_df.to_excel(writer,index = False)
os.chdir(r'E:\2017-20180814病原下机&报告数据\安徽省立医院（武汉交付）1123-检出列表\安徽省立医院（武汉交付）-检出列表~')
for i in os.listdir():
    if i.split('.')[0] not in t_list:
        print(i)