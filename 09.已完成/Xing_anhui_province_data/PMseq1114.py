# -- coding: utf-8 --
import os

file_path = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/安徽.txt'
csv_path = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/2017-20180814病原下机&报告数据'
out = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/Anhui.txt'
f = open(file_path)
o = open(out,'w',encoding = 'utf8')
sample = []
for i in f.readlines():
    sample.append(i.rstrip())
sample = [i.split('-')[0] for i in sample]
print(len(sample))
file_list = []
for root,dirs,files in os.walk(csv_path):
    for file1 in files:
        # print(file1.split('.')[0])
        if file1.split('.')[0] in sample:
            # print(file1.split('.')[0])
            file_list.append(os.path.join(root, file1))
print(len(file_list))