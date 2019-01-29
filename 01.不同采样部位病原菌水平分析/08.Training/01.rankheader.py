#-*- coding=utf-8 -*-
import os
import pandas as pd
os.chdir(r'D:\0125\华山医院整理后病人数据')
files = [os.path.join(os.getcwd(),path,fl) for path in os.listdir() for fl in os.listdir(os.path.abspath(path))]
seper={'csv':b',','xls':b'\t'}
seper2={'csv':',','xls':'\t'}
header = {}
header[13] = ['#Sample','Species','Chinese','Coverage','Cov_Rate','Depth','MRN','SMRN','SDCOV','SDdepth','SDMRN','SDSMRN','ID']
header[14] = ['#Sample','Species','Chinese','Gram','Coverage','Cov_range','Depth','MRN','SMRN','SDCOV','SDdepth','SDMRN','SDSMRN','ID']
header[16] =['#Sample','Species','Chinese','Coverage','Cov_Rate','CR_range','Depth','MRN','MRN_range','SMRN','SMRN_range','SDCOV','SDdepth','SDMRN','SDSMRN','ID']
header[17] =['#Sample','Species','Chinese','Gram','Coverage','Cov_Rate','CR_range','Depth','MRN','MRN_range','SMRN','SMRN_range','SDCOV','SDdepth','SDMRN','SDSMRN','ID']
header[21] = ['#Sample','Species','Chinese','Coverage','CovRate','Depth','Abs_Abu','Re_Abu','Genus','GenusCh','Genus_Abs_Abu','Genus_Re_Abu','MRN','SMRN','SMRNG','SDCOV','SDdepth','SDMRN','SDSMRN','SDSMRNG','ID']
header[22] = ['#Sample','Species','Chinese','Coverage','CovRate','Depth','Abs_Abu','Re_Abu','Genus','GenusCh','Genus_Abs_Abu','Genus_Re_Abu','MRN','SMRN','SMRNG','SDCOV','SDdepth','SDMRN','SDSMRN','SDSMRNG','Gram','ID']
def find_header(fl):
    with open(fl,'rb') as f:
        flag=0
        length = -1
        for index,line in enumerate(f):
            if line.startswith(b'#Sample'):
                flag=1
                lines=[str(i).rstrip("'").lstrip("b'") for i in line.rstrip().split(b'\t')]
                if len(lines)>10:
                    return index,lines,'\t'
                if len(lines)<10:
                    lines=[str(i).rstrip("'").lstrip("b'") for i in line.rstrip().split(b',')]
                    return index,lines,','
            if length==-1:
                length = len(line.rstrip().split(seper[fl.split('.')[-1]]))
        if flag==0:
            if length in header.keys():
                return -2,header[length]
            else:
                return -1,-1    
os.chdir(r'D:\0125\华山医院整理后病人数据2.rankheader')
for fl in files:
    if os.stat(fl).st_size == 0:
        continue
    if fl.endswith('xlsx'):
        # print(os.path.split(fl)[1]+'!!!')
        continue
    if find_header(fl)[0]==-1:
        print(os.path.split(fl)[1])
        continue
    elif find_header(fl)[0]==-2:
        df = pd.read_csv(fl,sep=seper2[fl.split('.')[-1]],encoding='gb18030',engine='python',names=find_header(fl)[1])
    else:
        df = pd.read_csv(fl,sep=find_header(fl)[2],encoding='gb18030',engine='python',names=find_header(fl)[1])
        df = df.drop(find_header(fl)[0])
    if not os.path.exists(os.path.split(fl)[1].split('.')[0]):
        os.mkdir(os.path.split(fl)[1].split('.')[0])
    df.to_csv(os.path.join(os.getcwd(),os.path.split(fl)[1].split('.')[0],'.'.join(os.path.split(fl)[1].split('.')[:-1]+['xls'])),encoding='gbk',sep='\t',index=False)