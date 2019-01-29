# import os
# path = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/2017-20180814病原下机&报告数据'
# filt_list = []
# for filepath,temp,filename in os.walk(path):
#     for file_name in filename:
#         if file_name == 'data.stat.xls':
#             filt_list.append(os.path.join(filepath, file_name))

# 2007版以前的Excel（xls结尾的），需要使用xlrd读，xlwt写。
# 2007版以后的Excel（xlsx结尾的），需要使用openpyxl来读写
def data_stat_extract():    
    # import shutil
    import os
    # import pandas as pd
    path_file = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/Anhui.txt'
    out = open('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/data.stat.xls', 'w')
    f = open(path_file)
    dataline = set([])
    sampleID_set = set([])
    datalines =[]
    for i in f.readlines():
        # print(i)
        # shutil.copy(i.rstrip(),os.path.split(path_file)[0]+'/pathogen_path')
        os.chdir(os.path.split(i.rstrip())[0])
        sampleID = os.path.split(i.rstrip())[1].split('.')[0]
        sampleID_set.add(sampleID)
        data_file = os.path.split(i.rstrip())[0]+'/data.stat.xls'
        dataline.add(data_file)
    # print(len(dataline),sampleID_set)
    for data_file1 in dataline:
        if os.path.exists(data_file1):
            o = open(data_file1)
        elif os.path.exists(os.path.splitext(data_file1)[0]+'.csv'):
            o =open(os.path.splitext(data_file1)[0]+'.csv')
        else:
            print(data_file1)
        for line in o.readlines():
            if line.rstrip().split()[0]in sampleID_set:
                datalines.append(line.rstrip().split())
    for sample in datalines:
        for i in sample[:-1]:
            out.write(i+',')
        out.write(sample[-1]+'\n')
def combine_xlsxSheet():
    import pandas as pd
    data_path = r'C:\Users\邓秋洋\Downloads\PMseq临床数据整理需求\报告汇总表安徽省立医院.xlsx'
    data_path #报告汇总表安徽省立医院
    data_stat = r'C:\Users\邓秋洋\Downloads\PMseq临床数据整理需求\安徽省立医院\data.stat.xlsx'
    data_stat #包含数据量、人源比率、严格比对等信息
    # data_stat_new = r'C:\Users\邓秋洋\Downloads\PMseq临床数据整理需求\安徽省立医院\data2.stat.xlsx'
    f1 = pd.read_excel(data_path)
    f2 = pd.read_excel(data_stat)
    sampleID1 = list(f1['NGS编号'])
    sampleID2 = list(f2['#SampleID'])
    f1_list = [sampleID1.index(i) for i in sampleID2]
    select_row = f1.loc[f1_list,] #f1.loc[]指定行
    print(select_row)
    # select_row.to_excel(data_stat_new)
combine_xlsxSheet()