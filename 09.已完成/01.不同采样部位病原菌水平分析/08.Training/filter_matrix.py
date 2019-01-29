import pandas as pd
import re 
import os

pathogen_file_path = r"C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\01pathogen_matrix"
for matrix_file in [os.path.join(pathogen_file_path,i) for i in os.listdir(pathogen_file_path) if os.path.splitext(i)[1] == '.csv']:
    # 如果包含中文，可以先打开文件句柄，再pandas读取
    f = open(matrix_file,encoding='gbk')
    df = pd.read_csv(f,header=0)
    print(list(df.columns))
    exit()

    