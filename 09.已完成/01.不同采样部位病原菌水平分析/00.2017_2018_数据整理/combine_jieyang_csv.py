# -*- coding:utf-8 -*-
#合并当前目录下所有csv文件到一个csv文件
import os
import re
import pandas as pd
def main():
        filenames=os.listdir(os.getcwd())
        outfile = os.getcwd()+'\\'+'all_csv2.csv'
        for filename in filenames:
                if 'csv' in filename:
                        filepath = os.getcwd() + '\\' + filename
                        df = pd.read_csv(filepath,engine = 'python') #不加engine（好像是中文的问题）会一直报错OSError: Initializing from file failed
                        df.to_csv(outfile, encoding="utf-8-sig",index=False, header=False, mode='a+')#mode追加到outfile文件
if __name__ == '__main__':
        main()