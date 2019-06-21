import os,re
import pandas as pd
from collections import Counter

log=r'F:\华山医院\01.华山医院NGS测序报告\logging2.xls'
header = r'F:\华山医院\01.华山医院NGS测序报告\header6.xls'
data= r'F:\华山医院\01.华山医院NGS测序报告\1227.merge'



def Obtain_Mycobacterium(log):
    log_df = pd.read_csv(log,engine='python',sep='\t',header=None)
    log_df.columns=['sampleid','logging']
    a = Counter(log_df.logging)
    print(a)
    # for i,j in zip(log_df['sampleid'],log_df['logging']):
    #     if isinstance(j,str):
    #         if re.search('Mycobacterium',j):
Obtain_Mycobacterium(log)
def Obtain_filelist(data):
    files = {}
    for i in os.listdir(data):
        files[i.split('.')[0]]=os.path.join(data,i)
    return files

def main():
    files = Obtain_filelist(data)
    for i in Obtain_Mycobacterium(log):
        if i in files.keys():
            df = pd.read_table(files[i],engine='python')
            df1 = df[df.Species.str.contains('Mycobacterium*')]
            rows,cols=df1.shape
            if rows==0:
                continue
                # print(i,end=',') # 17P0836020,18S3298549,17S0585501,17S0585375,17S0585610
            if 'SDSMRNG' in df1:
                continue # 17S0588726
            yield (i,sum(df1.SDSMRN))

# for sampleid,sdsmrn in main():
#     header_df = pd.read_excel(header,index_col='标本编号')
#     header_df.loc[sampleid,'致病病原体SDSMRN']=sdsmrn

# header_df.to_excel(r'F:\华山医院\01.华山医院NGS测序报告\header7.xls')