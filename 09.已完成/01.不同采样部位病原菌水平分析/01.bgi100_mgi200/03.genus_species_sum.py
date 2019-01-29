import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import shutil
from collections import Counter

bgi100 = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\BGI100'
mgi200_2557 = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\S100002557.result.V4.0.0.tar.gz.dir'
mgi200_2615 = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\S100002615.result.V4.0.0.tar.gz.dir'
out_dir = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试'
#找出目的文件
def shutil_file(path):
    os.chdir(os.path.split(path)[0])
    dir_name = 'MGI200_' + (os.path.split(path)[1].split('.')[0])[-4:]
    # print(dir_name)
    # if not os.path.exists(dir_name):
    #     os.makedirs(dir_name)
    # for i in os.listdir(dir_name):
    #     os.remove(os.path.join(os.getcwd(),dir_name,i))
    # for i in [os.path.join(path,i) for i in os.listdir(path)]:
    #     file_ext = os.path.splitext(os.path.split(i)[1])[1]
    #     filter_ext = os.path.splitext(os.path.splitext(os.path.split(i)[1])[0])[1]
    #     if file_ext == '.xls' and filter_ext == '.filter':
    #         shutil.copy(i,dir_name)
    return os.path.join(os.getcwd(),dir_name)
mgi200_2557 = shutil_file(mgi200_2557)
mgi200_2615 = shutil_file(mgi200_2615)

def species_genus(path,rank=0):
    os.chdir(path)
    species_sum = {}
    genus_sum = {}
    genus_rank_sum ={}
    sampleID_list = []
    for fl in sorted(os.listdir()):
        sampleID,ptg = fl.split('.')[0],fl.split('.')[1]
        if len(sampleID) == 10:
            if sampleID not in sampleID_list:
                sampleID_list.append(sampleID)
        df = pd.read_excel(fl)
        # print(df.columns.tolist())
        # exit()
        if rank == 0:
            if len(fl.split('.')[0]) ==10:
                try:
                    species_sum.setdefault(ptg,[]).append(len(list(df.Species)))
                    # print(dict(Counter(list(df.Genus))))
                    genus_sum.setdefault(ptg,[]).append(len(dict(Counter(list(df.Genus)))))
                except:
                    print(fl)
        elif rank==1:
            if len(fl.split('.')[0]) ==10:
                try:
                    # species_sum.setdefault(ptg,[]).append(len(list(df.Species)))
                    # print(dict(Counter(list(df.Genus))))
                    genus_rank_sum.setdefault(sampleID,[]).append((ptg,dict(Counter(list(df.Genus)))))
                except:
                    print(fl)
    if rank == 1:
        return genus_rank_sum

    species_sum['#Sample'] = list(sampleID_list)
    genus_sum['#Sample'] = list(sampleID_list)
    # genus_rank_sum['#Sample'] = 
    df = pd.DataFrame(data = species_sum)
    df2 = pd.DataFrame(data = genus_sum)
    return df,df2
    # with pd.ExcelWriter(os.path.join(path,'species_sum.xlsx')) as writer:
    #     df.to_excel(writer,index=False)
    # with pd.ExcelWriter(os.path.join(path,'genum_sum.xlsx')) as writer:
    #     df2.to_excel(writer,index=False)
def plot_genus_species(bgi100,mgi200_2557,mgi200_2615):
    bac_list = list(bgi100['#Sample'])
    for n in range(len(bac_list)):
        x = [1, 2, 3]
        y1 = np.array([list(bgi100['bac'])[n],list(mgi200_2557['bac'])[n],list(mgi200_2615['bac'])[n]])
        y2 = np.array([list(bgi100['fungi'])[n],list(mgi200_2557['fungi'])[n],list(mgi200_2615['fungi'])[n]])
        y3 = np.array([list(bgi100['parasite'])[n],list(mgi200_2557['parasite'])[n],list(mgi200_2615['parasite'])[n]])
        y4 = np.array([list(bgi100['virus'])[n],list(mgi200_2557['virus'])[n],list(mgi200_2615['virus'])[n]])
        plt.subplot(331+n)
        plt.xlabel('Sequencing Platform')
        plt.ylabel('Species')
        plt.title(bac_list[n])
        plt.xticks(x,('BGI100', 'MGI200-2557', 'MGI200-2615'))
        plt.bar(x, y1, width=0.35, color='lightskyblue', label='bac')
        plt.bar(x, y2, width=0.35, bottom=y1, color='yellowgreen', label='fungi')
        plt.bar(x, y3, width=0.35, bottom=y1+y2, color='dodgerblue', label='parasite')
        plt.bar(x, y4, width=0.35, bottom=y1+y2+y3,color='sandybrown',label='virus')
        plt.legend(loc=[1, 0])
    plt.show()
        
def genum_rank(sample_dict):
    
    for sampleid in sample_dict.keys():
        n = 0 
        plt.figure(figsize=(16,9))
        plt.suptitle(sampleid)
        for ptg,genus_dict  in sample_dict[sampleid]:
            plt.subplot(221+n).set_adjustable('box')
            n += 1
            genus_list,genus_rank_list=[],[]
            for k,v in sorted(genus_dict.items(),key = lambda d:d[1],reverse=True):
                genus_list.append(k)
                genus_rank_list.append(v)
            # color_list= ['midnightblue','darkblue','mediumblue','dodgerblue','deepskyblue','lightsteelblue','steelblue','cadetblue','skyblue','azure']
            X = np.arange(5)+1
            try:
                plt.bar(X,genus_rank_list[:5],width = 0.35,color='yellowgreen',edgecolor = 'white')
            except:
                X = np.arange(len(genus_rank_list))+1
                plt.bar(X,genus_rank_list,width = 0.35,color='yellowgreen',edgecolor = 'white')
            plt.xlabel('Genus')
            plt.ylabel('Rank_sum')
            plt.title(ptg)
            plt.xticks(X,genus_list)#放在下面没法看
            # for y in x:
            #     plt.xticks(x,ptg)
            #     plt.bar(x,genus_rank_list[y],label=genus_list[y])
        # plt.tight_layout()
            # plt.subplots_adjust(top=0.963,bottom=0.062,left=0.035,right=0.99,hspace=0.203,wspace=0.079)
        plt.savefig(r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\种和属水平物种数以及排名\Genus_rank\bgi_rank_sum{}.jpeg'.format(sampleid))
        # plt.show()
        plt.close()

# 三个平台数据dir
print(bgi100,mgi200_2557,mgi200_2615)
exit()
file_list = [bgi100,mgi200_2557,mgi200_2615]
# from flush_data import  check_header
# species_genus(mgi200_2557)
# for path in file_list:
#     # check_header(path)
#     species_genus(path)
# bgi_sp_sum,bgi_genus_sum = species_genus(bgi100)
# mgi200_2557_sp_sum,mgi200_2557_genus_sum = species_genus(mgi200_2557)
# mgi200_2615_sp_sum,mgi200_2615_genus_sum = species_genus(mgi200_2615)
genus_rank_sum_bgi = species_genus(bgi100,1)
genus_rank_sum_mgi_2557 = species_genus(mgi200_2557,1)
genus_rank_sum_mgi_2615 = species_genus(mgi200_2615,1)

# plot_genus_species(bgi_sp_sum,mgi200_2557_sp_sum,mgi200_2615_sp_sum)
# plot_genus_species(bgi_genus_sum,mgi200_2557_genus_sum,mgi200_2615_genus_sum)
# print(genus_rank_sum_bgi)
genum_rank(genus_rank_sum_bgi)