import numpy as np
import scipy.stats as st
import os
from math import sqrt
from functools import reduce
#处理各组织的SMRN数据（四种病原菌），过滤值为零，数据小于5的数据，然后计算得到置信区间，调整原有的‘肠道感染\bac.txt’结构为‘肠道感染bac.txt’，为下一步根据bac整理为四个文件准备。

data_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照感染归类SMRN版'
confidence_interal_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData'

def filter_phogen(pathogen_path):
    # print(pathogen_path)
    f = open(pathogen_path, 'rb')
    data_dict ={}
    filter_data = []
    for data_line in f.readlines():
        filter_data.clear()
        initial_data = data_line.rstrip().split(b'\t')[1:]
        for data in initial_data:
            if data != b'0':
                filter_data.append(data) 
                #print(data)
        # print(data_line.split(b'\t')[0],filter_data)
        if len(filter_data)<5:
            continue
        data_dict[data_line.split(b'\t')[0]] = filter_data.copy()
    # print(len(data_dict))
    return data_dict 

def compute_confidence_interal(pathogen_dict):
    pathogenfilter_dict ={}
    for pathogen_species,SMRN in pathogen_dict.items():
        SMRN = [int(i) for i in SMRN]
        mean = float(sum(SMRN)) / len(SMRN)
        stdev = sqrt(float(reduce(lambda x, y: x + y, map(lambda x: (x - mean) ** 2, SMRN))) / len(SMRN))
        confidence_interal = [mean - 1.96 * (stdev / sqrt(len(SMRN))),mean + 1.96 * (stdev / sqrt(len(SMRN)))]
        # confidence_interal =st.t.interval(0.95, len(SMRN)-1, loc=np.mean(SMRN), scale=st.sem(SMRN))
        print(SMRN,mean,stdev,confidence_interal)
        exit()
        pathogenfilter_dict[pathogen_species] = confidence_interal
    return pathogenfilter_dict

def main(data_path):

    for organ in [os.path.join(data_path,i) for i in os.listdir(data_path)]:
        print(organ)
        bac_dict, virus_dict, fungi_dict, parasite_dict = [{} for i in range(4)] # 谨记教训
        dict_list = {'bac':bac_dict, 'virus':virus_dict, 'fungi':fungi_dict, 'parasite':parasite_dict}
        organ_name = os.path.basename(organ)
        # print(organ_name,os.listdir(organ))
        for pathogen_path in [os.path.join(organ,i) for i in os.listdir(organ)]:
            print(pathogen_path)
            pathogen_name = os.path.basename(os.path.splitext(pathogen_path)[0])
            pathogen_dict = filter_phogen(pathogen_path)
            dict_list[pathogen_name] = compute_confidence_interal(pathogen_dict)       
        for pathogen,data in dict_list.items():
            pathogen_name = os.path.basename(os.path.splitext(pathogen)[0])
            sample_name = organ_name + pathogen_name
            f = open(os.path.join(confidence_interal_path+'\\'+sample_name+'.txt'),'w')
                #print(pathogen,data)          
            for pathogen_species,confidence_interal_data in data.items():
                a, b = confidence_interal_data
                    # print(pathogen_species)
                f.write(bytes.decode(pathogen_species)+'\t'+str(a)+'\t'+str(b)+'\n')
            f.close()
        # exit()
if __name__ == '__main__':
    main(data_path)