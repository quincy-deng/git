import pandas as pd
import os
import math
import numpy as np

def check_header(path,fl_header):
    file_ext = {'xls':b'\t','csv':b','}
    a,b,c =0,0,0
    add_header = [len(i) for i in fl_header]
    for boot,dirnames,files in os.walk(path):
        dirnames # no use
        for fl in files:
            a += 1
            os.chdir(boot)
            sampleid,ptg_type,ext = fl.split('.')[0][:10],fl.split('.')[1],fl.split('.')[-1]
            line_list = []
            header = []
            with open(fl,'rb') as F:
                fl_content = F.readlines()
                for line in fl_content:
                    line_list.append(line)
                    if line.split(file_ext[ext])[0] != b'#Sample':
                        continue
                    header = line
                content = []
                for line in line_list:
                    content.append(line.rstrip().split(file_ext[ext]))   
                # check header 
                try:
                    line_list.remove(header)
                    header = header.rstrip().split(file_ext[ext])
                except:
                    try:
                        # no header,add it 
                        header_index =add_header.index(len(content[0]))
                        df =pd.core.frame.DataFrame(content,columns=fl_header[header_index])
                        print('ok')
                    except:
                        # empty file
                        print('empty file:{}'.format(fl))
                        continue 
                try:
                    df = pd.core.frame.DataFrame(content,columns= header)
                except:
                    try:
                        df = pd.core.frame.DataFrame(content,columns= header[:-1]) #some file header more one col
                    except:
                        print(fl)
                df.to_csv('{}_{}.xls'.format(sampleid,ptg_type),sep='\t',mode='w')
            # os.remove(fl)
                
fl_header = []
with open(r'F:\huashan_header.txt') as ff:
    for hline in ff.readlines():
        fl_header.append(hline.rstrip().split('\t'))

check_header(r'D:\华山医院整理数据',fl_header)