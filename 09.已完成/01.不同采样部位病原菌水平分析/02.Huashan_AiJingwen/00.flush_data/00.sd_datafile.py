import os

# 合并bac,fungi,parasite,virus四个文件
def concat_ptg(path):
    os.chdir(path)
    for result_dir in os.listdir():
        os.chdir(result_dir)
        concat_file()
        os.chdir(os.pardir)
        
def concat_file():
    sample_dict = {}
    for i in os.listdir():
        sample_dict.setdefault(i.split('_')[0],[]).append(i)
    for k,v in sample_dict.items():
        if len(v)!=4:
            print(k,v)

datafile = r'D:\华山医院\华山医院整理数据'
concat_ptg(datafile)
