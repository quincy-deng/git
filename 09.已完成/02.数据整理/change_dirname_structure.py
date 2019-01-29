import os
import re 
import shutil

out_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版'

# 按照bac，fungi，parasite。virus 四种进行分类
# for organ_path in [os.path.join(data_path, i) for i in os.listdir(data_path)]: 
#     os.chdir(organ_path)
#     dir_name = os.path.basename(organ_path)
#     print(os.listdir(os.getcwd()))
#     [os.rename(i,dir_name+i) for i in os.listdir(os.getcwd())]
#     print(os.listdir(os.getcwd()))

pathogen_list = ['bac', 'fungi', 'virus', 'parasite']
# for organ_path in [os.path.join(data_path, i) for i in os.listdir(data_path)]:
#     # print(organ_path)
#     for n in [os.path.join(organ_path, k) for k in os.listdir(organ_path)]:
#         # print(n)
#         for pathogen_name in pathogen_list:
#             if re.search(pathogen_name, n):
#                 shutil.move(n,os.path.join(out_path, pathogen_name))
for pathogens in [os.path.join(out_path, k) for k in os.listdir(out_path)]:
    os.chdir(pathogens)
    for organ in [os.path.join(pathogens, i) for i in os.listdir(pathogens)]:
        os.rename(os.path.basename(organ),os.path.basename(organ)+'.txt')