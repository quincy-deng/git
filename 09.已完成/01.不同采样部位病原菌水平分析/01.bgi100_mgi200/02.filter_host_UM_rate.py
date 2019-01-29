import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np



bgi100 = r'F:\BGI100_MGI200\BGI100_MGI200.data\未整理\BGI100data.tar.gz.dir\data2.stat.xls'
mgi200_2557 = r'F:\BGI100_MGI200\BGI100_MGI200.data\未整理\S100002557.result.V4.0.0.tar.gz.dir\data2.stat.xls'
mgi200_2615 = r'F:\BGI100_MGI200\BGI100_MGI200.data\未整理\S100002615.result.V4.0.0.tar.gz.dir\data2.stat.xls'
file_list = [bgi100,mgi200_2557,mgi200_2615]

def filter_Host_UMhost(f1,f2,f3):
    name = os.path.split(os.path.split(f1)[0])[1].split('.')[0]+'_'+os.path.split(os.path.split(f2)[0])[1].split('.')[0]+ '.xlsx'
    print(name)
    df1 = pd.read_excel(f1)
    df2 = pd.read_excel(f2)
    df3 = pd.read_excel(f3)
    columns_name = list(df1['#SampleID'])
    
    map_bac1,map_vir1,map_fungi1,map_pro1 = list(df1['Map_bac']),list(df1['Map_vir']),list(df1['Map_fungi']),list(df1['Map_pro'])
    map_ptg1 = list(np.sum([map_bac1,map_fungi1,map_pro1,map_vir1],axis=0))
    map_bac2,map_vir2,map_fungi2,map_pro2 = list(df2['Map_bac']),list(df2['Map_vir']),list(df2['Map_fungi']),list(df2['Map_pro'])
    map_ptg2 = list(np.sum([map_bac2,map_fungi2,map_pro2,map_vir2],axis=0))
    map_bac3,map_vir3,map_fungi3,map_pro3 = list(df3['Map_bac']),list(df3['Map_vir']),list(df3['Map_fungi']),list(df3['Map_pro'])
    map_ptg3 = list(np.sum([map_bac3,map_fungi3,map_pro3,map_vir3],axis=0))

    um_host1,um_host2,um_host3 = list(df1['UMhost']),list(df2['UMhost']),list(df3['UMhost'])
    host1,host2,host3 = list(df1['Host_rate']),list(df2['Host_rate']),list(df3['Host_rate'])
    map_ptg_rate1,map_ptg_rate2,map_ptg_rate3 = [],[],[]
    for i in range(9):
        map_ptg_rate1.append(map_ptg1[i]/(um_host1[i]/(1-host1[i])))
        map_ptg_rate2.append(map_ptg2[i]/(um_host2[i]/(1-host2[i])))
        map_ptg_rate3.append(map_ptg3[i]/(um_host3[i]/(1-host3[i])))
    unknown1,unknown2,unknown3 = [],[],[]
    for i in range(9):
        unknown1.append(1-map_ptg_rate1[i]-host1[i])
        unknown2.append(1-map_ptg_rate2[i]-host2[i])
        unknown3.append(1-map_ptg_rate3[i]-host3[i])
    outdata = {}
    for n in range(9):
        outdata[columns_name[n]] = [host1[n],unknown1[n],map_ptg_rate1[n],host2[n],unknown2[n],map_ptg_rate2[n],
        host3[n],unknown3[n],map_ptg_rate3[n]]
    outdata['rate_type']=['host','unknown','map','host','unknown','map','host','unknown','map']
    outdata['Group'] = ['BGI100','BGI100','BGI100','MGI200_2557','MGI200_2557','MGI200_2557','MGI200_2615','MGI200_2615','MGI200_2615']
    # outdata = {'sampleid':columns_name,'host1':host1,'host2':host2,'host3':host3,
    # 'unknown1':unknown1,'unknown2':unknown2,'unknown3':unknown3,
    # 'map1':map_ptg_rate1,'map2':map_ptg_rate2,'map3':map_ptg_rate3}
    df =pd.DataFrame(data=outdata)
    # df = df.T
    df.to_csv(r'F:\BGI100_MGI200\BGI100_MGI200.result\host_unknown_map rate\rate.txt',sep='\t',index=False)

    # for n in range(len(columns_name)):
    #     x = [0, 1, 2]
    #     y1 = np.array([host1[n],host2[n],host3[n]])
    #     y2 = np.array([unknown1[n],unknown2[n],unknown3[n]])
    #     y3 = np.array([map_ptg_rate1[n],map_ptg_rate2[n],map_ptg_rate3[n]])
    #     plt.subplot(331+n)
    #     plt.xlabel('Sequencing Platform')
    #     plt.ylabel('Proportion')
    #     plt.title(columns_name[n])
    #     plt.xticks(x,('BGI100', 'MGI200-2557', 'MGI200-2615'))
    #     plt.bar(x, y1, width=0.35, color='lightskyblue', label='Host')
    #     plt.bar(x, y2, width=0.35, bottom=y1, color='yellowgreen', label='Unknown')
    #     plt.bar(x, y3, width=0.35, bottom=y1+y2, color='dodgerblue', label='Pathogen')
    #     plt.legend(loc=[1, 0])
        
    #     #设置画布大小
    #     # plt.set_size_inches(18.5,10.5)
    # plt.tight_layout()
    # plt.show()
    
    #     plt.savefig(r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\人源序列、微生物序列、未知序列比例\{}.jpg'.format(columns_name[n]),dpi= 300)
    #     plt.close()


filter_Host_UMhost(file_list[0],file_list[1],file_list[2])