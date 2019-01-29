import pandas as pd
import os
import xlrd
import re

# 统计表格
hospital_results = r'D:\1114医院感染数据\副本to麻老师1114 整理的标本.xlsx'
# #整理输出所有病原菌
# out = r'D:\1114医院感染数据\pathogen.txt'
# o =open(out,'w')
# 获取workbook中所有的表格,括号一半是中文一半英文，有的都是中文.....
wb = xlrd.open_workbook(hospital_results)
sheets = wb.sheet_names()
pgen = []


with pd.ExcelWriter(r'D:\1114医院感染数据\1121自整理.xlsx') as writer:
    for i in range(len(sheets)):
        print(i)
        df = pd.read_excel(hospital_results,sheet_name = sheets[i])
        col_names = df.columns.tolist()
        temp_list = list(df['二代测序结果'])
        new_list = []
        for n in temp_list:
            #利用正则去掉冗余信息，首先去除括号和括号内文本信息，然后去掉中文逗号，括号，分号等无关符号。
            new1_list = re.split('(\(|\（)[^()]*(\)|\）)', str(n))
            new2_list = []
            for m in new1_list:
                new2_list += re.split('[，()（）\s,\?\？]',str(m))
            new_list.append(','.join([k for k in new2_list if k != '']))
        col_num = col_names.index('二代测序结果')
        # print(col_num,df['二代测序结果'])
        df.pop('二代测序结果')
        df.insert(col_num,'二代测序结果',new_list)
        df2=df[['标本编号','患者姓名','标本','标本类型','二代测序结果','二代测序阳性','复合菌群','真阳性','最终/目前诊断','同步培养','培养结果','其他金标准','复合金标准真阳性','复合金标准阳性','综合阳性']].copy()
        df2.to_excel(writer,sheet_name = sheets[i],index = False)
        
# [o.write(i+'\n') for i in all_pathogen