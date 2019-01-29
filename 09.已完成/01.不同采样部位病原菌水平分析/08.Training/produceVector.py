import os
import re
fiol_path = r'C:\Users\邓秋洋\Desktop\新建文件夹'
out_path = os.path.join(fiol_path,'matrix.csv')
Species_set = set([])
data_dict = {}
for files in [os.path.join(fiol_path, i) for i in os.listdir(fiol_path)]:
    f = open(files,'r',encoding = 'gbk')
    tags = ['#Sample', 'Species', 'SDSMRN']
    line1 = f.readline().rstrip().split()
    file_tags = line1.index(tags[1])
    file_Species = line1.index(tags[2])
    for line in f.readlines():
        Species_set.add(line.rstrip().split()[file_tags])
        data_dict.setdefault(os.path.basename(files).split('.')[0],[]).append((line.rstrip().split()[file_tags],line.rstrip().split()[file_Species]))
o =open(out_path,'w')
o.write('#Sample')
[o.write(','+i) for i in Species_set]
o.write('\n')
for sample_id,v in data_dict.items():
    o.write(sample_id)
    Species_list = []
    SDSMRN_list = []
    for spcies,SDSMRN in v:
        Species_list.append(spcies)
        SDSMRN_list.append(SDSMRN)
    for Species in Species_set:
        if Species in Species_list:
            index = Species_list.index(Species)
            o.write(','+SDSMRN_list[index])
        else:
            o.write(','+str(0))
    o.write('\n')