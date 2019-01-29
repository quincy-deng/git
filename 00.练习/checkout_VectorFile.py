
import os
fungi_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi1102'
for i in [os.path.join(fungi_path, i) for i in os.listdir(fungi_path)]:
    n = 0
    f = open(i,'r')
    first_line = len(f.readline().rstrip().split()) + 1
    f.readline()
    organ_name = os.path.basename(i).split('vector.txt')[0]
    for line in f.readlines():
        n += 1
        if len(line.rstrip().split()) != first_line:
            print(organ_name,n,len(line.rstrip().split()), first_line)
