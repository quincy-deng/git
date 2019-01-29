#coding: utf8
import os
import pandas as pd
import xlrd
class Produce_Matrix(object):
    def __init__(self,path,path2):
        self.path = path
        self.path2 =path2
        self.df= None
        self.sampleids = None
        self.files_path = None
        self.organ_files = []
        # path 不同组织二代测序结果表格;path2 原始数据目录
        
    def Organ_dir(self):
        os.chdir(self.path)
        # 工作目录,处理各个组织
        for fl in os.listdir():
            if os.path.isdir(fl):
                continue
            df = open(fl)
            print(fl)
            ids_results=list(self.ob_sampleid(df))
            ids = []
            [ids.append(i) for i,j in ids_results]
            # 样本编号       
            
            self.files_path = list(self.Organ_files_path(ids))
            # 组织原始数据路径
            os.chdir(self.path)
            if not os.path.exists(fl.split('.')[0]):
                os.mkdir(fl.split('.')[0])
            os.chdir(fl.split('.')[0])
            
            self.Paroduce_matrix(fl)
            
            os.chdir(os.pardir)
            print('{} 完成!'.format(fl.split('.')[0]))

    def Organ_files_path(self,ids):
        os.chdir(self.path2)
        temp = set([])
        for boot,dir2,files in os.walk(self.path2):
            for fl in files:
                if fl.split('_')[0] in ids:
                    if fl in temp:
                        continue
                    temp.add(fl)
                    yield os.path.join(boot,fl)
    # 从不同目录获得所有文件的路径

    def ob_sampleid(self,df):
        sps= []
        for line in df.readlines():
            for sp in line.rstrip().split('\t')[1].split(';'):
                try:
                    sps.append(sp.split(',')[1])
                except:
                    print(sp)
                    sps.append(0)
            yield (line.split('\t')[0][:10],sps)
    # 输出标本编号和阳性类型

    def produce_matrix(self):
        species=set([])
        for fl in self.files_path:
            try:
                df = pd.read_table(fl,engine='python')
                [species.add(sp) for sp in list(df['Species']) if isinstance(sp,str)]
            except:
                df = pd.read_csv(fl,engine='python')
                [species.add(sp) for sp in list(df['Species']) if isinstance(sp,str)]

    def Paroduce_matrix(self,fl):
        fl_dict ={}
        species=set([])
        organ_type = fl.split('.')[0]
        data_matrix = open('{}_matrix.xls'.format(organ_type),'w')
        # info_matrix = open('{}_info.xls'.format(organ_type),'w')
        for fl in self.files_path:
            try:
                df = pd.read_table(fl,engine='python')
                [species.add(sp) for sp in list(df['Species']) if isinstance(sp,str)]
            except:
                df = pd.read_csv(fl,engine='python')
                [species.add(sp) for sp in list(df['Species']) if isinstance(sp,str)]
        # print(species)
        data_matrix.write('sampleid'+'\t')
        data_matrix.write('\t'.join(species)+'\n')
        # info_matrix.write('\t'.join(species)+'\n')
        for fl in self.files_path:
            data_matrix.write(os.path.split(fl)[1].split("_")[0]+'\t')
            # info_matrix.write(os.path.split(fl)[1].split("_")[0]+'\t')
            df = pd.read_csv(fl,sep='\t',engine='python')
            if len(df.columns.tolist())<5:
                df = pd.read_csv(fl,sep=',',engine='python')
            try:
                for sp in species:
                    if sp in list(df['Species']):
                        data_matrix.write(str(list(df['SDSMRN'])[list(df['Species']).index(sp)])+'\t')
                    else:
                        data_matrix.write(str(0)+'\t')
            except:
                print(fl,len(df.columns.tolist()))
            data_matrix.write('\n')

path =r'D:\华山医院\1114医院感染数据\组织分类'
path2= r'D:\华山医院\华山医院整理数据'
hahah = Produce_Matrix(path,path2)
hahah.Organ_dir()