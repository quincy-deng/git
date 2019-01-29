# 有的患者缺少文件，如翁佰欢；有的患者测了好几种，文件夹层级与其他不同，如刑宗芳，表格里面的二代测序结果和华大出具的正式报告结果不一致；
# 输入文件原始目录和接样表文件
import pandas as pd
import os
import xlrd
from collections import Counter
import shutil
import re

#病原菌文件目录
reports1_path = r'E:\NGS总测序报告第一部分\NGS总测序报告第一部分'
reports2_path = r'E:\NGS总测序报告第二部分\NGS总测序报告第二部分'
reports3_path = r'E:\NGS总测序报告第三部分\NGS总测序报告第三部分'
reports_path = [reports1_path,reports2_path,reports3_path]

# 统计表格
hospital_results = r'D:\1114医院感染数据\副本to麻老师1114 整理的标本.xlsx'

# 获取workbook中所有的表格
wb = xlrd.open_workbook(hospital_results)
sheets = wb.sheet_names()

# 判断是否包含目的文件
def judge_sampleID(files,sample_list):
    flag = 0
    file_list = []
    for fileID in files:
        if len(fileID.split('.')) >3:
            fileID1 = fileID[:10]
            if fileID1 in sample_list:
                flag = 1
                file_list.append(fileID)
    sample_set = set([fileID[:10] for fileID in file_list])
    mutisample_list = []
    if len(sample_set) > 1:
        # print(sample_set)
        for sample_id in sample_set:
            temp_list = []
            for temp in file_list:
                if temp[:10] == sample_id:
                    temp_list.append(temp)
            mutisample_list.append(temp_list)
        file_list = []

    return flag,file_list,mutisample_list

# 筛选原始文件，优先选择非top文件
def judge_files(files,sample_list):  
    flag,file_list,mutisample_list = judge_sampleID(files,sample_list)
    result = Counter([len(filename.split('.')) for filename in file_list])
    # print(result)
    if flag == 0:
        return 'NoMatch',0
    elif result[4] == 4:
        return [filename for filename in file_list if len(filename.split('.'))==4],1
    elif result[5] == 4:
        return [filename for filename in file_list if len(filename.split('.'))==5],1
    elif  (result[4] + result[5]) ==4:
        return [filename for filename in file_list if len(filename.split('.'))==4 or len(filename.split('.'))==5],1
    elif file_list == []:
        new_mutisample_list = []
        for p_list in mutisample_list:
            result = Counter([len(filename.split('.')) for filename in p_list])
            if result[4] == 4:
                new_mutisample_list.append([filename for filename in p_list if len(filename.split('.'))==4])
                continue
            elif result[5] == 4:
                new_mutisample_list.append([filename for filename in p_list if len(filename.split('.'))==5])
                continue
            elif  (result[4] + result[5]) ==4:
                new_mutisample_list.append([filename for filename in p_list if len(filename.split('.'))==4 or len(filename.split('.'))==5])
        # print(len(new_mutisample_list))
        return new_mutisample_list,len(new_mutisample_list)
    else:
        # print(files)
        return 'NoMatch',0

# 根据样本编号，获得文件路径
def extraction_filepath(sample_list,files_path):
    sample_list = [i.split('-')[0] for i in sample_list]
    filePath_list = []
    samle_sum = 0
    for file_path in files_path:
        for boot,dirnames,files in os.walk(file_path):
            result,n = judge_files(files,sample_list)
            samle_sum += n
            if result != 'NoMatch':
                if n==1:
                    filePath_list.append([os.path.join(boot,filename) for filename in result])
                elif n>1:
                    for i in range(n):
                        filePath_list.append([os.path.join(boot,filename) for filename in result[i]])
    # test =[i[0] for i in filePath_list]
    # test_dict = Counter(test)
    # print([k+':'+str(v) for k,v in test_dict.items() if v >1])
    # print(filePath_list)
    # print(len(test))
    print('{} found in {}'.format(samle_sum,len(sample_list)))
    return filePath_list

sheets_dict = {}
lists = []
for i in range(len(sheets)):
    df = pd.read_excel(hospital_results,sheet_name = i)
    columns = df.columns.values.tolist()
    file_list = extraction_filepath(list(df['标本编号']),reports_path)
    outpath = r'E:\{}'.format(sheets[i])
    sub_dirsname = ['bac','fungi','virus','parasite']
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        for sub_dir in sub_dirsname:
            sub_dir_path = r'E:\{}\{}'.format(sheets[i],sub_dir)
            if not os.path.exists(sub_dir_path):
                os.makedirs(sub_dir_path)

    for filespath in file_list:
        for filepath in filespath:
            file_ext = ''
            for sub_dir in sub_dirsname:
                if re.search(sub_dir,os.path.split(filepath)[1]):
                    file_ext = sub_dir
            if not os.path.exists(os.path.join(outpath,file_ext,os.path.split(filepath)[1])):
                shutil.copy(filepath,os.path.join(outpath,file_ext,os.path.split(filepath)[1]))