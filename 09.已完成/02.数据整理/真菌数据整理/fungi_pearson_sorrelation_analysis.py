import boxplot_fungi
import re
import os
import sys
from math import sqrt
import pandas as pd
sys.path.append(r'C:\Users\邓秋洋\Documents\python_learning\01.不同采样部位病原菌水平分析')
import extract_data_csv as data_read

data_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理03版'

# def pearson_distance(vector1, vector2) :
#     """
#     Calculate distance between two vectors using pearson method
#     See more : http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
#     """
#     sum1 = sum(vector1)
#     sum2 = sum(vector2)

#     sum1Sq = sum([pow(v,2) for v in vector1])
#     sum2Sq = sum([pow(v,2) for v in vector2])

#     pSum = sum([vector1[i] * vector2[i] for i in range(len(vector1))])

#     num = pSum - (sum1*sum2/len(vector1))
#     den = sqrt((sum1Sq - pow(sum1,2)/len(vector1)) * (sum2Sq - pow(sum2,2)/len(vector1)))

#     if den == 0 :
#         return 0.0
#     return 1.0 - num/den 
def multipl(a,b):
    sumofab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sumofab+=temp
    return sumofab
 
def corrcoef(x,y):
    n=len(x)
    #求和
    sum1=sum(x)
    sum2=sum(y)
    #求乘积之和
    sumofxy=multipl(x,y)
    #求平方和
    sumofx2 = sum([pow(i,2) for i in x])
    sumofy2 = sum([pow(j,2) for j in y])
    num=sumofxy-(float(sum1)*float(sum2)/n)
    #计算皮尔逊相关系数
    den=sqrt((sumofx2-float(sum1**2)/n)*(sumofy2-float(sum2**2)/n))
    return num/den

def obtain_Species_dict(pathogen_path,organ_name):
    pathogen_dict = {}
    for pathogen_file_path in [os.path.join(pathogen_path, sample_filename) for sample_filename in os.listdir(pathogen_path)]:
        sep = data_read.judge_sep(pathogen_file_path)
        df = open(pathogen_file_path,'rb')
        n = 0
        f = df.readlines()
        # print(f)
        for line in f:
            n += 1
            if line.rstrip().split(sep)[0] == b'#Sample':
                sample_column, Species_column, SDSMRN_column = line.rstrip().split(sep).index(b'#Sample'), \
                line.rstrip().split(sep).index(b'Species'), line.rstrip().split(sep).index(b'SDSMRN')
                # print(sample_column, Species_column, SDSMRN_column)
                for line in f:
                    if len(line.rstrip().split(sep)) < SDSMRN_column:
                        continue
                    elif line.rstrip().split(sep)[SDSMRN_column] == b'SDSMRN':
                        continue
                    else:
                        pathogen_dict[(line.rstrip().split(sep)[sample_column], line.rstrip().split(sep)[Species_column])] = \
                        line.rstrip().split(sep)[SDSMRN_column]
                break
    # print(sorted(pathogen_dict))              
    Spcies_set = set([])
    for sample in pathogen_dict.keys():
        sample_ID,Species = sample
        Spcies_set.add(Species)
    Spcies_dict = {}
    sample_ID_set = set([])
    for sample_ID, Species in sorted(pathogen_dict.keys()):
        # sample_ID, Species = sample_spcies
        sample_ID_set.add(sample_ID)
    for k in Spcies_set:
        i = 0
        n = 0
        for sample_spcies in sample_ID_set:
            n += 1
            if (sample_spcies,k) not in pathogen_dict.keys():
                pathogen_dict[(sample_spcies,k)] = 0
            Spcies_dict.setdefault(bytes.decode(k),[]).append(int(pathogen_dict[(sample_spcies,k)]))
            if int(pathogen_dict[(sample_spcies,k)]) == 0:
                i += 1 
        # print(i,len(Spcies_dict[bytes.decode(k)]))
        if sum(Spcies_dict[bytes.decode(k)]) < 10:
            Spcies_dict.pop(bytes.decode(k)) #如果有SDSMRN值为0有超过一半的样本数，删除这个species
    # print(organ_name, len(Spcies_dict) / n) 
    return Spcies_dict

def obtain_file_list(data_path):
    bac_dict = {}
    fungi_dict = {}
    for organ_path in [os.path.join(data_path, organ_name) for organ_name in os.listdir(data_path)]:
        for pathpgen_path in [os.path.join(organ_path, pathogen_name) for pathogen_name in os.listdir(organ_path)]:
            if os.path.basename(pathpgen_path) == 'bac':
                bac_dict[os.path.basename(organ_path)] = obtain_Species_dict(pathpgen_path, os.path.basename(organ_path))
            elif os.path.basename(pathpgen_path) == 'fungi':
                fungi_dict[os.path.basename(organ_path)] = obtain_Species_dict(pathpgen_path, os.path.basename(organ_path))
    # # for organ in bac_dict.keys():
    #     f = open(r'C:/Users/邓秋洋\Desktop/07.analysis_bypogenData/病原数据按照组织归类SDSMRN版/'+ organ + r'vector2.txt', 'w')
    #     for k,v in fungi_dict[organ].items():
    #         f.write('{0:<40}'.format(k))
    #         for i in v:
    #             f.write('{0:<5}'.format(i) )
    #         f.write('\n')
    #     f.close()
    return bac_dict,fungi_dict

def compare_TwoPathogen(organ_bac_dict,organ_fungi_dict, organ_name): #将同一组织下所有样本的bac的所有种类与fungi的所有种类一一做关联分析
    f = open(r'C:/Users/邓秋洋\Desktop/07.analysis_bypogenData/病原数据按照组织归类SDSMRN版/'+ organ_name + r'pearson_number2.txt', 'w')
    sample_sum = len(organ_bac_dict.keys())
    # sample_fungi_sum =  sum(organ_fungi_dict.values())
    f.write('{0:{1}<20}'.format('样本总数：', chr(12288)) + organ_name + '{:<10}'.format(str(sample_sum)) + '\n')
    n = 0
    for bac_pathogen in organ_bac_dict.keys():
        for fungi_pathogen in organ_fungi_dict.keys():
            pearson_number = corrcoef(organ_bac_dict[bac_pathogen],organ_fungi_dict[fungi_pathogen])
            if pearson_number < n:
                    n =pearson_number
            if abs(pearson_number) > 0.8:
                pass
                # f.write('{0:<10}'.format(str('%.2f'%pearson_number))) 
                # f.write(format(str('%.2f'%pearson_number),'<10') + '\t')
                # f.write(format(bac_pathogen,'<45') + '\t')
                # f.write(format(str('%.2f'%(sum(organ_bac_dict[bac_pathogen])/len(organ_bac_dict[bac_pathogen]))),'<10') + '\t')
                # f.write(format(fungi_pathogen,'<45') + '\t')
                # f.write(format(str('%.2f'%(sum(organ_fungi_dict[fungi_pathogen])/len(organ_fungi_dict[fungi_pathogen]))),'<10'))
                # # f.write('{0:<45}'.format(bac_pathogen))
                # # f.write('{0:<45}'.format(fungi_pathogen))
                # # [f.write(str(i)+',') for i in organ_bac_dict[bac_pathogen]]
                # # f.write(':')
                # # [f.write(str(i)+',') for i in organ_fungi_dict[fungi_pathogen]]
                # f.write('\n')
    print(organ_name, n)
    f.close()
                    
def main(data_path):
    bac_dict, fungi_dict = obtain_file_list(data_path)
    for organ_name in bac_dict.keys():
        compare_TwoPathogen(bac_dict[organ_name],fungi_dict[organ_name], organ_name)

main(data_path)