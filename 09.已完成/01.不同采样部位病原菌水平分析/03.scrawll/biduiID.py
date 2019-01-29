import os
import gzip
accession_file = r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/export_ID_accession.csv'
f = open(accession_file)
accession_dict = {}
accession_list = []
for line in f.readlines():
    accession_dict[line.split(',')[0]] = line.rstrip().split(',')[1:]
for k,v in accession_dict.items():
    for i in v:
        accession_list.append(i)
print('accession length equal {}'.format(len(accession_list)))
# exit()
taxid_path = r'/ldfssz1/ST_CANCER/CVD/USER/liqiongfang/accession2taxid'
file_list = ['nucl_est.accession2taxid.gz','nucl_gb.accession2taxid.gz']
yizhi = []
for i in file_list:
    print(os.path.join(taxid_path,i))
    f1 = gzip.open(os.path.join(taxid_path,i))
    print(f1.readline())
    n = 0
    while True:
        n += 1
        print(n)
        accession = bytes.decode(f1.readline().split(b'\t')[1])
        if accession in accession_list:
            print(accession)
            yizhi.append(accession)
print(len(yizhi))
