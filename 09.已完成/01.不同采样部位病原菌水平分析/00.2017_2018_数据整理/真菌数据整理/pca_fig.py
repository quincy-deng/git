import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import numpy as np
import PCA_analysis as pca
import csv

fungi_vector_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi不同组织vector-1102'


organ_path_list = [os.path.join(fungi_vector_path,i) for i in os.listdir(fungi_vector_path)]
f = open(organ_path_list[0],'r')
f.readline()
f.readline()
organ_name = os.path.basename(organ_path_list[0]).split('vect')[1].split('.txt')[0]
fungi_name,sample_list = [], []
for i in f.readlines():
    fungi_name.append(i.rstrip().split()[0])
    temp_list = [int(i) for i in i.rstrip().split()[1:]]
    sample_list.append(temp_list)
a = np.matrix(sample_list)
b_temp = a.T
b = b_temp.tolist()
for i in b:
    i.append(organ_name)
fungi_name.append('group')
f.close()
for organ in organ_path_list[1:]:
    # print(organ)
    organ_name_temp = os.path.basename(organ).split('vect')[1].split('.txt')[0]
#     print(organ_name_temp)
    f = open(organ,'r')
    f.readline()
    f.readline()
    sample_list_temp = []
    for i in f.readlines():
        temp_list = [i for i in i.rstrip().split()[1:]]
        sample_list_temp.append(temp_list)
    j = np.matrix(sample_list_temp)
    k_temp = j.T
    k = k_temp.tolist()
    for i in k:
        i.append(organ_name)
    for i in k:
        b.append(i)
    f.close()

with open(os.path.join(r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版', 'vector1.csv'),'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fungi_name)
        writer.writerows(b)