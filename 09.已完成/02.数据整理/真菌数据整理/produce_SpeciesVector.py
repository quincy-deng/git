import os
import sys
sys.path.append(r'C:\Users\邓秋洋\Documents\python_learning\01.不同采样部位病原菌水平分析')
from extract_data_csv import analysis_single_sample as ass
path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理03版'

def obtain_pathogen_path(pathogen,path):
    pathogen_path_temp = []
    for organ_path in [os.path.join(path, i) for i in os.listdir(path)]:
        for pathogen_path in [os.path.join(organ_path, i) for i in os.listdir(organ_path)]:
            if os.path.basename(pathogen_path) ==pathogen:
                pathogen_path_temp.append((os.path.basename(organ_path), [os.path.join(pathogen_path, i) for i in os.listdir(pathogen_path)]))
    return(pathogen_path_temp)

def obtain_organ_dict(pathogen,pathogen_species): #处理一种菌8个组织
    pathogen_dict = {}
    for i in pathogen_species:
        organ_name, pathogen_species_list = i    
        species_set = set([])
        sample_list,pathogen_dict_list = [], []
        for file_pathogen in pathogen_species_list:
            a =ass(file_pathogen)
            sample_list.append(os.path.basename(file_pathogen).split('.')[0])
            pathogen_dict_list.append(a)
            for species in a.keys():
                species_set.add(species)
        pathogen_dict[organ_name] = (sample_list, pathogen_dict_list, species_set)
    produce_vectorfile(pathogen,  pathogen_dict)

def produce_vectorfile(pathogen, pathogen_dict):
    if not os.path.exists(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'matrix1105')):
        os.makedirs(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'matrix1105'))
    os.chdir(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版',pathogen + 'matrix1105'))
    for organ_name in pathogen_dict:
        f = open(organ_name+'vector.txt','w')
        f.write('{:<50}'.format(''))
        sample_list, pathogen_dict_list, species_set =pathogen_dict[organ_name]
        [f.write('{:<10}'.format(i+'\t')) for i in sample_list]
        f.write('\n')
        f.write('{:<50}'.format(''))
        [f.write('{:<10}'.format(str(i+1)+'\t')) for i in range(len(sample_list))]
        f.write('\n')
        for species in species_set:
            if species == b'Species':
                print('wrong line')
            else:
                f.write('{:<50}'.format(bytes.decode(species)))
            for sample_dict in pathogen_dict_list:
                if species in sample_dict.keys():
                    if  sample_dict[species] == b'':
                        f.write('{:<10}'.format(str(0)+'\t'))
                    elif sample_dict[species] == b'SDSMRN':
                        print('wrong!!!')
                        continue
                    else:
                        f.write('{:<10}'.format(str(int(sample_dict[species])) + '\t'))
                else:
                    f.write('{:<10}'.format(str(0)+'\t'))
            f.write('\n')

def main(path):
    pathogens =['virus', 'fungi', 'parasite', 'bac']
    pathogen_path_dict = {}
    for pathogen in pathogens:
        pathogen_path_dict[pathogen] = obtain_pathogen_path(pathogen, path) # 获得不同类病原菌不同组织下的文件路径列表
    for pathogen in pathogens:
        obtain_organ_dict(pathogen, pathogen_path_dict[pathogen])


main(path)