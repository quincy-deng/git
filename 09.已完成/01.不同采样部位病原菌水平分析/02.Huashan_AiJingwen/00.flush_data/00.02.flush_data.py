import pandas as pd
import os
import math
import numpy as np

def export_file(sampleid,ptg_type,df):
    f = open('{}_{}.xls'.format(sampleid,ptg_type),'wb')
    print(df)
    for line in df:
        for i in line[:-1]:
            f.write(i+b'\t')
        f.write(line[-1]+b'\n')

def NoHeader_NoEmpty(content):
    try:
        line_list.remove(header)
        header = header.rstrip().split(file_ext[ext])
        for line in line_list:
                content.append(line.rstrip().split(file_ext[ext])) 
    except:
        return 0
def Cols_exssive():
    pass
def check_header(path,fl_header):
    file_ext = {'xls':b'\t','csv':b','}
    add_header = [len(i) for i in fl_header]
    for boot,dirnames,files in os.walk(path):
        dirnames # no use
        for fl in files:
            df = []
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
                # check header 
                
                except:
                    try:
                        for line in line_list:
                            content.append(line.rstrip().split(file_ext[ext])) 
                        # no header,add it 
                        header_index =add_header.index(len(content[0]))
                        df =content.insert(0,fl_header[header_index])
                        # print('ok')
                    except:
                        # empty file
                        print('empty file:{}'.format(fl))
                        continue 
                try:
                    df = content.insert(0,header)
                except:
                    try:
                        df = content.insert(0,header[:-1]) #some file header more one col
                    except:
                        print(fl)
                        continue
                
            # os.remove(fl)



fl_header = []
with open(r'F:\huashan_header.txt') as ff:
    for hline in ff.readlines():
        fl_header.append(hline.rstrip().split('\t'))

check_header(r'D:\华山医院整理数据',fl_header)