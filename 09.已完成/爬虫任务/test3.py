sunjingmeng = r'C:\Users\邓秋洋\Desktop\sunjingmeng.fmt6'
initial_file = r'C:\Users\邓秋洋\Desktop\sunjingmeng.txt'
sun = open(initial_file)
n = 0
seq_list = []
while True:
    n += 1
    line = sun.readline().rstrip()
    if not line:
        break
    if n % 2 == 1:
        seq_list.append(line.split('>')[1])

sunjingmeng_filter = r'C:\Users\邓秋洋\Desktop\sunjingmeng_filter.fmt6'
o = open(sunjingmeng_filter,'w')
fmt6 = open(sunjingmeng)
seqid_list = []
data_dict = {}
while True:
    line = fmt6.readline()
    if  line.split() == []:
        break
    seqid = line.split()[0]
    if seqid not in seqid_list:
        seqid_list.append(seqid)
        data = line.split('\t')[11:14]
        print(line.split('\t')[14])
        data_dict[seqid] = data
for seqid in seq_list:
    if seqid in data_dict.keys():
        o.write(seqid)
        for res in data_dict[seqid]:
            o.write('\t'+res)
        o.write('\n')
    else:
        o.write(seqid + '\t' + 'No Matching'+'\n')