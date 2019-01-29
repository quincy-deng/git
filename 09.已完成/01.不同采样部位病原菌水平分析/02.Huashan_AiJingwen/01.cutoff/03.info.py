#coding: utf8
import os
import pandas as pd
import xlrd
import math
class Produce_Matrix(object):
    def __init__(self,path,path2):
        self.path = path
        self.path2 =path2
        self.df= None
        self.sampleids = None
        self.files_path = None
        self.organ_files = []
        self.sps = {}
        # path 不同组织二代测序结果表格;path2 原始数据目录
        
    def Organ_dir(self):
        os.chdir(self.path)
        # 工作目录
        # f = open('organ_postive_species.xls','w')
        for fl in os.listdir():
            if os.path.isdir(fl):
                continue
            df = open(fl)
            # print(df.readlines())
            self.ob_sampleid(df)
            # print(self.sps)
            # 获得物种:id的字典

            os.chdir(fl.split('.')[0])
            # 进入对应组织目录

            matrix=pd.read_csv('{}_matrix.xls'.format(fl.split('.')[0]),sep='\t',engine='python',index_col=False)
            print(matrix.shape)
            matrix = matrix.groupby('sampleid').sum()
            sample_list = matrix.index.tolist()
            # print(sample_list)
            print(matrix.shape)
            #合并id相同的行

            o = open('{}_cutoff2.xls'.format(fl.split('.')[0]),'w')
            o.write('log10(SDSMRN)\tP|N\tspecies\n')
            for spe,sample in self.sps.items():
                pos = []
                try:
                    sdsmrn = list(matrix[spe])
                    # o.write('{}\t'.format(spe))
                    for sam in sample:
                        try:
                            tp=sample_list.index(sam)
                            pos.append(sdsmrn[tp])
                            sdsmrn.pop(tp)
                        except:
                            print(sam)
                    pos=[str(math.log10(x)) for x in pos if x!=0]
                    neg=[str(math.log10(x)) for x in sdsmrn if x!=0]
                    if len(pos)>3:
                        for i in pos:
                            o.write('{}\tP\t{}\n'.format(i,spe))
                        if neg:
                            for i in neg:
                                o.write('{}\tN\t{}\n'.format(i,spe))
                except:
                    print(spe)
            os.chdir(os.pardir)

    def ob_sampleid(self,df):
        self.sps= {}
        for line in df.readlines():
            for sp in line.rstrip().split('\t')[1].split(';'):
                try:
                    i = sp.split(',')[1]
                    self.sps.setdefault(i,[]).append(line.rstrip().split('\t')[0][:10])
                except:
                    pass
        # print(self.sps)
            
path =r'D:\华山医院\1114医院感染数据\组织分类'
path2= r'D:\华山医院\华山医院整理数据'
hahah = Produce_Matrix(path,path2)
hahah.Organ_dir()