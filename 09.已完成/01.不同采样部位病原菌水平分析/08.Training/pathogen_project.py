# import os,sys
# import re
# import shutil

# import pandas as pd
# import xlrd

# #分析病人的excel表，获得病人样品编号和采样部位
# class Patient_Info(object):
#     def __init__(self):
#         self.dir_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet' # 非原始路径，勿用
#         # 文件输出路径
#         self.jieyang_sheet = 'E:\\jieyang_sheet'
#         # 目的文件
#         self.jieyang_CSV_file = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\all_csv2.csv'
#     # 提取所有的接样表
#     def Grab_JieyangSheet(self):
#         for pattern, dirname, filenames in os.walk(self.dir_path):  # 这里用walk可以遍历所有的文件夹和子文件夹的所有文件
#             for filename in filenames:
#                 if re.search('接样', filename):
#                     shutil.copy(os.path.join(pattern, filename), self.jieyang_sheet)  # 复制文件到指定路径
#     # 获得所有病人的数据，输出csv格式文件到当前目录
#     def Extract_JieyangSheet(self):
#         for i in os.listdir(self.jieyang_sheet):
#             if re.search('xls',i) and not re.search('~' , i) and not re.search('csv', i): # 读取bug问题原来是读到了系统的隐藏文件，比如‘~$2018-06-20病原接样表-武汉.xlsx’
#                 csv_name = os.path.basename(i)
#                 csv_name = csv_name + '.2.csv'
#                 csv_filepath = os.path.join(self.jieyang_sheet, csv_name)
#                 xls_filepath = os.path.join(self.jieyang_sheet,i)
#                 print("xls: ", xls_filepath)
#                 data = pd.read_excel(xls_filepath, sheet_name = '病原快检')
#                 if '样品类型' in data.columns: #不能使用data['样品类型']判断列是否存在
#                     temp = data.loc[:,['样品类型','样品编号']]
#                     temp.to_csv(csv_filepath, encoding='utf-8-sig', index = False)
#     #合并所有的csv文件
#     def Combine_Jieyang(self):
#             filenames=os.listdir(os.path.splitext(self.jieyang_CSV_file)[0])
#             outfile = self.jieyang_CSV_file
#             for filename in filenames:
#                     if re.search('csv',filename):
#                             filepath = os.path.splitext(self.jieyang_CSV_file)[0] + '\\' + filename
#                             df = pd.read_csv(filepath,engine = 'python') #不加engine（好像是中文的问题）会一直报错OSError: Initializing from file failed
#                             df.to_csv(outfile, encoding="utf-8-sig",index=False, header=False, mode='a+')#mode追加到outfile文件
# # 整理数据文件
# class Patient_Data(object):
#     def __init__(self):
#         self.jieyang_CSV_file = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\all_csv2.csv'
#         self.Initial_Data = r'C:\Users\邓秋洋\Desktop\病原分类数据'
#         self.Pathogen_organ_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理03版'
#     #寻找所有的病原文件,按照'fungi','bac','parasite','virus'整理
#     def Produce_SampleVector(self):
#         pathogens =['bac', 'virus', 'fungi', 'parasite']
#         pathogen_path_dict = {}
#         for pathogen in pathogens:
#             pathogen_path_dict[pathogen] = obtain_pathogen_path(pathogen, path) # 获得不同类病原菌不同组织下的文件路径列表
#         for pathogen in pathogens:
#             obtain_organ_dict(pathogen, pathogen_path_dict[pathogen])
#         def obtain_pathogen_path(pathogen,path): 
#             pathogen_path_temp = []
#             for organ_path in [os.path.join(path, i) for i in os.listdir(path)]:
#                 for pathogen_path in [os.path.join(organ_path, i) for i in os.listdir(organ_path)]:
#                     if os.path.basename(pathogen_path) ==pathogen:
#                         pathogen_path_temp.append((os.path.basename(organ_path), [os.path.join(pathogen_path, i) for i in os.listdir(pathogen_path)]))
#             return(pathogen_path_temp)
#         # 处理一种菌
#         def obtain_organ_dict(pathogen,pathogen_species): 
#             pathogens_dict = {}
#             species_set = set([])
#             for i in pathogen_species:
#                 organ_name, pathogen_species_list = i    
#                 sample_list,pathogen_dict = [], {}
#                 # 处理不同的组织
#                 for file_pathogen in pathogen_species_list:
#                     a =analysis_single_sample(file_pathogen)
#                     sample_list.append(os.path.basename(file_pathogen).split('.')[0])
#                     pathogen_dict[os.path.basename(file_pathogen).split('.')[0]] = a
#                     for species in a.keys():
#                         species_set.add(species)
#                 pathogens_dict[organ_name] = (sample_list, pathogen_dict)
#             produce_vectorfile(pathogen,  pathogens_dict, species_set)

#         def produce_vectorfile(pathogen, pathogens_dict,species_set):
#             if not os.path.exists(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105')):
#                 os.makedirs(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105'))
#             os.chdir(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105'))
#             f = open(pathogen+'vector_filter.csv','w')
#             f.write('Sample_ID')
#             [f.write(','+bytes.decode(i)) for i in species_set if i != b'Species' and i !=b'']
#             f.write(',' + 'group'+'\n')
#             for organ_name in pathogens_dict:
#                 sample_list, pathogen_dict =pathogens_dict[organ_name]
#                 for sample in sample_list:
#                     f.write(sample)
#                     for species in species_set:
#                         if species == b'Species' or species == b'':
#                             continue
#                         if species in pathogen_dict[sample].keys():
#                             if  pathogen_dict[sample][species] == b'':
#                                 f.write(','+str(0))
#                             elif pathogen_dict[sample][species] == b'SDSMRN':
#                                 print('wrong!!!')
#                                 continue
#                             elif int(pathogen_dict[sample][species])<= 10:
#                                 f.write(','+str(0))
#                             else:
#                                 f.write(',' + str(int(pathogen_dict[sample][species])))
#                         else:
#                             f.write(',' + str(0))
#                     f.write(','+organ_name + '\n')
#         def analysis_single_sample(csv): # 解析单个csv文件
#             sep = judge_sep(csv)
#             # print(csv)
#             df = open(csv, 'rb')
#             header = df.readline().split(sep)
#             data_SMRN = {}
#             # print(header[0])
#             if not re.search(b'#Sample', header[0]):
#                 data_frame = df.readlines()
#                 df.seek(0, os.SEEK_SET)
#                 Species, SMRN = found_header(data_frame, sep)
#                 print('header_row:', 0)
#             else:
#                 for i in range(len(header)):
#                     if header[i] == b'Species':
#                         Species = i
#                     elif header[i] == b'SDSMRN':
#                         SMRN = i
#             # print(df.readline(),sep, Species, SMRN)
#             for i in df.readlines():
#                 data_SMRN[i.split(sep)[Species]] = i.split(sep)[SMRN]
#             df.close()    
#             return data_SMRN


# import numpy as np
# import scipy.stats as st
# import os
# from math import sqrt
# from functools import reduce

# class analysis_bypogenData(object):
#     def __init__(self):
#         self.data_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照感染归类SMRN版'
#         self.confidence_interal_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData'
#     def compute_confidence_interal(self):
#         def filter_phogen(pathogen_path):
#             # print(pathogen_path)
#             f = open(pathogen_path, 'rb')
#             data_dict ={}
#             filter_data = []
#             for data_line in f.readlines():
#                 filter_data.clear()
#                 initial_data = data_line.rstrip().split(b'\t')[1:]
#                 for data in initial_data:
#                     if data != b'0':
#                         filter_data.append(data) 
#                         #print(data)
#                 # print(data_line.split(b'\t')[0],filter_data)
#                 if len(filter_data)<5:
#                     continue
#                 data_dict[data_line.split(b'\t')[0]] = filter_data.copy()
#             # print(len(data_dict))
#             return data_dict 

#         def compute_confidence_interal(pathogen_dict):
#             pathogenfilter_dict ={}
#             for pathogen_species,SMRN in pathogen_dict.items():
#                 SMRN = [int(i) for i in SMRN]
#                 mean = float(sum(SMRN)) / len(SMRN)
#                 stdev = sqrt(float(reduce(lambda x, y: x + y, map(lambda x: (x - mean) ** 2, SMRN))) / len(SMRN))
#                 confidence_interal = [mean - 1.96 * (stdev / sqrt(len(SMRN))),mean + 1.96 * (stdev / sqrt(len(SMRN)))]
#                 # confidence_interal =st.t.interval(0.95, len(SMRN)-1, loc=np.mean(SMRN), scale=st.sem(SMRN))
#                 print(SMRN,mean,stdev,confidence_interal)
#                 exit()
#                 pathogenfilter_dict[pathogen_species] = confidence_interal
#             return pathogenfilter_dict

#         def main():
#             for organ in [os.path.join(self.data_path,i) for i in os.listdir(self.data_path)]:
#                 print(organ)
#                 bac_dict, virus_dict, fungi_dict, parasite_dict = [{} for i in range(4)] # 谨记教训
#                 dict_list = {'bac':bac_dict, 'virus':virus_dict, 'fungi':fungi_dict, 'parasite':parasite_dict}
#                 organ_name = os.path.basename(organ)
#                 # print(organ_name,os.listdir(organ))
#                 for pathogen_path in [os.path.join(organ,i) for i in os.listdir(organ)]:
#                     print(pathogen_path)
#                     pathogen_name = os.path.basename(os.path.splitext(pathogen_path)[0])
#                     pathogen_dict = filter_phogen(pathogen_path)
#                     dict_list[pathogen_name] = compute_confidence_interal(pathogen_dict)       
#                 for pathogen,data in dict_list.items():
#                     pathogen_name = os.path.basename(os.path.splitext(pathogen)[0])
#                     sample_name = organ_name + pathogen_name
#                     f = open(os.path.join(self.confidence_interal_path+'\\'+sample_name+'.txt'),'w')
#                         #print(pathogen,data)          
#                     for pathogen_species,confidence_interal_data in data.items():
#                         a, b = confidence_interal_data
#                             # print(pathogen_species)
#                         f.write(bytes.decode(pathogen_species)+'\t'+str(a)+'\t'+str(b)+'\n')
#                     f.close()
#         main()
    
#     def combine_pathogenOrgan_file(self):
#         def combine_pathogen_file(pathgen_organ_path, out_path):
#             # bac_dict, virus_dict, fungi_dict, parasite_dict = [{} for i in range(4)] # 谨记教训
#             # dict_list = {'bac':bac_dict, 'virus':virus_dict, 'fungi':fungi_dict, 'parasite':parasite_dict}
#             for pathogen in [os.path.join(pathgen_organ_path, i) for i in
#                             os.listdir(pathgen_organ_path)]:  # 创建字典例如{‘bac’：bac_dict}
#                 jianchu_bili = []
#                 pathogen_name = os.path.basename(pathogen)
#                 specieses = set([])
#                 dict_save = {}
#                 organ_name = [os.path.basename(pathogen)]
#                 jianchu = []
#                 for pathgenOrgan_file in [os.path.join(pathogen, i) for i in
#                                         os.listdir(pathogen)]:
#                     organ_name.append(
#                         os.path.basename(os.path.splitext(pathgenOrgan_file)[0]).split(
#                             pathogen_name)[0])
#                     f = open(pathgenOrgan_file, 'r')
#                     n = 0
#                     for i in f.readlines():
#                         n += 1
#                         species = i.rstrip().split('\t')[0].split(':')[0]
#                         specieses.add(species)
#                     jianchu.append(n)
#                 f.close()
#                 sum_sp = len(specieses)
#                 for pathgenOrgan_file in [os.path.join(pathogen, i) for i in
#                                         os.listdir(pathogen)]:
#                     save_species = {}
#                     f = open(pathgenOrgan_file, 'r')
#                     for line in f.readlines():
#                         species = line.rstrip().split('\t')[0].split(':')[0]
#                         float_list = []
#                         float_list.append(float(line.rstrip().split('\t')[1]))
#                         float_list.append(float(line.rstrip().split('\t')[2]))
#                         new_list = []
#                         for i in float_list:
#                             new_list.append(round(i, 2))
#                         save_species[species] = new_list

#                     for species in specieses:
#                         if species in save_species.keys():
#                             dict_save.setdefault(species, []).append(
#                                 save_species[species])
#                         else:
#                             dict_save.setdefault(species, []).append(['-', '-'])
#                 f.close()
#                 for i in jianchu:
#                     jianchu_bili.append(round(i / sum_sp, 2))
#                 organ_number = [947, 1406, 29, 54, 20, 74, 1707, 1946]
#                 jianchu_dict = {jianchu_bili[i]: organ_number[i] for i in
#                                 range(len(jianchu_bili))}
#                 zhenshi = []
#                 for k, v in jianchu_dict.items():
#                     zhenshi.append(round(k * 100 / v, 2))
#                 o = open(os.path.join(out_path, pathogen_name + '.txt'), 'w')
#                 o.write(format(organ_name[0], '<40'))
#                 for i in organ_name[1:]:
#                     o.write(format(i, '<20'))
#                 o.write('\n')
#                 o.write(format('样本总数', '<40'))
#                 for i in organ_number:
#                     o.write(format(i, '<20'))
#                 o.write('\n')
#                 o.write(format('检出率', '<40'))
#                 for i in jianchu_bili:
#                     o.write(format(i, '<20'))
#                 o.write('\n')
#                 o.write(format('均一化检出率', '<40'))
#                 for i in zhenshi:
#                     o.write(format(i, '<20'))
#                 o.write('\n')
#                 for k, v in dict_save.items():
#                     o.write(format(k, '<40'))
#                     for i in v:
#                         o.write(format(str(i), '<20'))
#                     o.write('\n')
#         pathgen_organ_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据整理'
#         out_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData'
#         def main():
#             combine_pathogen_file(pathgen_organ_path, out_path)

