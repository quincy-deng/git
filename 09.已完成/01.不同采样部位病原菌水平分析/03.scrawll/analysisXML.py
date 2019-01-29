import requests
from bs4 import BeautifulSoup
file_path = r'C:\Users\邓秋洋\Downloads\YW9D421801R-Alignment3.txt'
export_ID_accession = r'C:\Users\邓秋洋\Downloads\export_ID_accession.txt'
o =open(export_ID_accession,'w')
f = open(file_path)
all_content = f.read().split('Query=')

# numberID = all_content[1].split('\n')[0]
# species = all_content[1].split('\n')[8:18]
# print(species)
all_csv_dict = {}
for part in all_content[1:]:
    key = part.split('\n')[0]
    species_lines = part.split('\n')[8:13]
    temp_accession = []
    for line in species_lines:
        # print(line.split()[0])
        # exit()
        try:
            if line.split()[0]=='ALIGNMENTS':
                break
            temp_accession.append(line.split()[0])
        except:
            print('{} lesser than  5'.format(part.split('\n')[0]))
    all_csv_dict[key] = temp_accession
# for i in range(len(numberID)):
#     o.write(numberID[i]+',')
#     [o.write(acc+',') for acc in accession[i][:-1]]
#     o.write(accession[i][-1]+'\n')
