import xlrd
import pandas as pd
import os
result_sheet_path = r'D:\1114医院感染数据\1121自整理.xlsx'
data_dir = r'D:\1114医院感染数据\菌种'
# 获取sheet名称
sheet_names = xlrd.open_workbook(result_sheet_path).sheet_names()
# 纠错对应表
pathogen_namedict = {'肺炎克雷伯':'肺炎克雷伯菌','肺炎克雷伯杆菌':'肺炎克雷伯菌','大肠埃希菌':'大肠杆菌','白念':'白色念珠菌','H7N9':'甲型流感病毒H7N9','肺克':'肺炎克雷伯菌',\
'鲍曼':'鲍曼不动杆菌','EbV':'人类疱疹病毒4型(EBV)','EBV':'人类疱疹病毒4型(EBV)','ebv':'人类疱疹病毒4型(EBV)','CMV':'人类疱疹病毒5型(CMV)','人类细小病毒':'人类细小病毒B19',\
'HHV6型':'人类疱疹病毒6B','HSV-1':'人类疱疹病毒1型(HSV1)','HSV1':'人类疱疹病毒1型(HSV1)','嗜麦芽假单胞菌':'嗜麦芽寡养单胞菌','巴西奴卡菌':'巴西诺卡菌',\
'鼻疽奴卡菌':'鼻疽诺卡菌','金葡菌':'金黄色葡萄球菌','金葡':'金黄色葡萄球菌','绿脓假单胞':'绿脓假单胞菌'}

speCH_EN ={}
for sheet_file in [os.path.join(data_dir,i) for i in os.listdir(data_dir)]:
    df = pd.read_excel(sheet_file)
    for i in range(len(list(df['Chinese']))):
        speCH_EN[list(df['Chinese'])[i]] = (os.path.splitext(os.path.split(sheet_file)[1])[0],list(df['Species'])[i])

with pd.ExcelWriter(r'D:\1114医院感染数据\1121自整理3.xlsx') as writer:
    for sheet_name in sheet_names:
        df = pd.read_excel(result_sheet_path,sheet_name = sheet_name)
        result = list(df['二代测序结果'])
        temp_sheet_list = []
        for i in range(len(result)):
            try:
                sample_reult_list = result[i].split(',')
            except:
                print(result[i])
            temp_sample_list = []
            for sample in sample_reult_list:
                if sample in pathogen_namedict.keys():
                    sample = pathogen_namedict[sample]
                if sample in speCH_EN.keys():
                    ptg_type,Species = speCH_EN[sample]
                    temp_sample_list.append(ptg_type+','+Species)
                else:
                    temp_sample_list.append('('+sample+')')
            temp_sheet_list.append(';'.join(sorted(temp_sample_list)))
        col_num = list(df.columns.tolist()).index('二代测序结果')
        df.insert(col_num,'new_NGS_result',temp_sheet_list)
        df.to_excel(writer,sheet_name = sheet_name,index = False)


# df = pd.core.frame.DataFrame(temp_list)
# writer = pd.ExcelWriter(r'D:\1114医院感染数据\PositiveSample.xlsx')
# df.to_excel(writer,'sheet1',index=False,columns=['PathogenType','SampleID','Species'])
# writer.save()
# print(m,n)
