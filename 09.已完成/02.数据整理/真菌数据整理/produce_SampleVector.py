import os
import sys
sys.path.append(r'C:\Users\邓秋洋\Documents\python_learning\01.不同采样部位病原菌水平分析')
from extract_data_csv import analysis_single_sample as ass
path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理03版'

# 获取一种菌（如bac）的所有文件（按组织分类），输入路径是总路径
def obtain_pathogen_path(pathogen,path): 
    pathogen_path_temp = []
    for organ_path in [os.path.join(path, i) for i in os.listdir(path)]:
        for pathogen_path in [os.path.join(organ_path, i) for i in os.listdir(organ_path)]:
            if os.path.basename(pathogen_path) ==pathogen:
                pathogen_path_temp.append((os.path.basename(organ_path), [os.path.join(pathogen_path, i) for i in os.listdir(pathogen_path)]))
    return(pathogen_path_temp)

# 处理一种菌
def obtain_organ_dict(pathogen,pathogen_species): 
    pathogens_dict = {}
    species_set = set([])
    for i in pathogen_species:
        organ_name, pathogen_species_list = i    
        sample_list,pathogen_dict = [], {}
        # 处理不同的组织
        for file_pathogen in pathogen_species_list:
            a =ass(file_pathogen)
            sample_list.append(os.path.basename(file_pathogen).split('.')[0])
            pathogen_dict[os.path.basename(file_pathogen).split('.')[0]] = a
            for species in a.keys():
                species_set.add(species)
        pathogens_dict[organ_name] = (sample_list, pathogen_dict)
    produce_vectorfile(pathogen,  pathogens_dict, species_set)

def produce_vectorfile(pathogen, pathogens_dict,species_set):
    if not os.path.exists(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105')):
        os.makedirs(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105'))
    os.chdir(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'samplematrix1105'))
    f = open(pathogen+'vector_filter.csv','w')
    f.write('Sample_ID')
    [f.write(','+bytes.decode(i)) for i in species_set if i != b'Species' and i !=b'']
    f.write(',' + 'group'+'\n')
    for organ_name in pathogens_dict:
        sample_list, pathogen_dict =pathogens_dict[organ_name]
        # f.write('{:<50}'.format(''))
        # [f.write('{:<10}'.format(str(i+1)+'\t')) for i in range(len(sample_list))]
        # f.write('\n')
        for sample in sample_list:
            f.write(sample)
            for species in species_set:
                if species == b'Species' or species == b'':
                    continue
                if species in pathogen_dict[sample].keys():
                    if  pathogen_dict[sample][species] == b'':
                        f.write(','+str(0))
                    elif pathogen_dict[sample][species] == b'SDSMRN':
                        print('wrong!!!')
                        continue
                    elif int(pathogen_dict[sample][species])<= 10:
                        f.write(','+str(0))
                    else:
                        f.write(',' + str(int(pathogen_dict[sample][species])))
                else:
                    f.write(',' + str(0))
            f.write(','+organ_name + '\n')

def main(path):
    pathogens =['bac', 'virus', 'fungi', 'parasite']
    pathogen_path_dict = {}
    for pathogen in pathogens:
        pathogen_path_dict[pathogen] = obtain_pathogen_path(pathogen, path) # 获得不同类病原菌不同组织下的文件路径列表
    for pathogen in pathogens:
        obtain_organ_dict(pathogen, pathogen_path_dict[pathogen])



main(path)