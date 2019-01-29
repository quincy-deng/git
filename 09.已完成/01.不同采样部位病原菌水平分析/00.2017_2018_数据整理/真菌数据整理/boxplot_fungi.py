import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties 
import scipy.stats as st

fungi_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi'

def judge_pathogen(organ_file_path,n):
    pathogen_dict = {}
    for pathogen_SDSMRN in open(organ_file_path, 'r').readlines():
        pathogen,SDSMRN = pathogen_SDSMRN.rstrip().split('\t')[0], pathogen_SDSMRN.rstrip().split('\t')[1:]
        # print(SDSMRN)
        number_list = []
        for number in SDSMRN:
            if int(number) > 0:
                number_list.append(math.log(int(number)))
        # print(number_list)
        if len(number_list) > n:
            pathogen_dict[pathogen] = number_list
    # print(pathogen_dict)
    return pathogen_dict

def produce_organ_pathogen_dict(organ_dict): #输入dict([organs][pathogens]:SDSMRN),获得同一病原菌不同组织的字典dict(pathogen:[organ1, organ2...])
    organ_pathogen_dict = {}
    for organ_name,pathogen_dict in organ_dict.items():
        organ_pathogen_dict[organ_name] = pathogen_dict.keys()
    organ_list = list(organ_pathogen_dict.keys())
    compare_dict_temp ={}
    for n in range(len(organ_list)-1):
        compare_organ = organ_list.pop()
        # print(organ_pathogen_dict[compare_organ])
        for compare_organ2 in organ_list:
            for pathogen in list(organ_pathogen_dict[compare_organ]):
                if pathogen in list(organ_pathogen_dict[compare_organ2]):
                    compare_dict_temp.setdefault(pathogen,set([])).add(compare_organ)
                    compare_dict_temp.setdefault(pathogen,set([])).add(compare_organ2)
                    # print(organ_pathogen_dict[compare_organ2])
                    list(organ_pathogen_dict[compare_organ2]).remove(pathogen)
    # print(len(compare_dict_temp))
        # exit()
    return compare_dict_temp

def filter_by_rankSum(data):
    filter_set = set([])
    sum_tab = []
    for i in range(len(data)-1):
        for j in [n for n in range(len(data)) if n >i]:
            a,b = st.ranksums(data[i],data[j])
            if b < 0.05:
                filter_set.add(i)
                filter_set.add(j)
                sum_tab.append((i, j, b))
    return filter_set,sum_tab

def produce_boxplot(organ_dict,pathogen_dict): #不同病原菌下的不同类型组织SDSMRN比较的箱线图
    f = open('C:/Users/邓秋洋/Desktop/'+'sum_tab.txt', 'w')
    for pathogen,organ_set in pathogen_dict.items(): 
        data = [np.array(organ_dict[i][pathogen]).astype(np.float) for i in organ_set] #np的作用是把字符串格式的列表转换成数字列表
        filter_set, sum_tab = filter_by_rankSum(data)
        f.write(format(pathogen,'<45') + '\n')
        if len(filter_set)<1:
            continue
        for a,b,c in sum_tab:
            f.write('{0:{1}<15}'.format(list(organ_set)[a], chr(12288)) + '{0:{1}<15}'.format(list(organ_set)[b], chr(12288))+format(str('%.2e'%c),'<10') + '\n')
        data =[data[i] for i in filter_set]
        organ_list = [list(organ_set)[i] for i in filter_set]
        font = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc',size = 14)
        # df = pd.DataFrame(data) #dataframe要求数组的长度都一样才可以，此处不适用
        path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi箱线图'
        figname = 'fig1_{}.png'.format(pathogen.split(':')[0]) # 优雅的命名方式
        dest = os.path.join(path, figname)
        # print(dest)
        fig = plt.figure()  # 创建画布
        ax = plt.subplot()  # 创建作图区域
        ax.boxplot(data) # 作图
        ax.set_xticklabels(organ_list, fontproperties=font) #设置中文格式
        plt.title(pathogen.split(':')[0])
        fig.savefig(dest) #用了savefig就不要用show。
        plt.close() #相当于关闭文件句柄，这样不会报错
        # plt.show()
        # exit()

def main(fungi_path):
    organ_dict = {}
    for organ_file_path in [os.path.join(fungi_path, i) for i in os.listdir(fungi_path)]:
        organ_name = os.path.basename(organ_file_path).split('.txt')[0]
        organ_dict[organ_name] = judge_pathogen(organ_file_path, 10)
        # print(organ_dict)
        # exit()
    compare_dict = produce_organ_pathogen_dict(organ_dict)
    produce_boxplot(organ_dict,compare_dict)

if __name__ == '__main__':
    main(fungi_path)