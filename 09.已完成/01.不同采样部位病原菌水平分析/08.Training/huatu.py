import heapq
jianchu_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\真菌不同类型不同菌株梯度检出率统计-SDSMRN\不同类型下的不同菌株的检出率03版.txt'
filter_jianchu_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\真菌不同类型不同菌株梯度检出率统计-SDSMRN\jianchulv2.csv'
f = open(jianchu_path,'r',encoding = 'gbk')
o = open(filter_jianchu_path,'w', encoding ='gbk')
f.readline()
organ_dict = {}
pathogen_list = []
for line in f.readlines():
    if line == '\n':
        continue
    name = line.rstrip().split()[0].split('_')[0]
    species = line.rstrip().split()[0].split('_')[2] + ' ' + line.rstrip().split()[0].split('_')[3].split(':')[0]
    organ_dict_key = name
    organ_dict_value = (species,line.rstrip().split()[1:])
    organ_dict.setdefault(organ_dict_key,[]).append(organ_dict_value)
organ_species_rata_list = []
species_set = []
for organ_name in organ_dict.keys():
    rate_list = []
    for species,jianchu_rate in organ_dict[organ_name]:
        rate_list.append(float(jianchu_rate[0].strip('%')))
    a_max_index = []
    for i in range(25):
        inf = 0
        a_max_index.append(rate_list.index(max(rate_list)))
        rate_list[rate_list.index(max(rate_list))] =inf
    species_rata_list = [organ_dict[organ_name][i] for i in a_max_index]
    species_set.append(species_rata_list)
    organ_species_rata_list.append((organ_name,species_rata_list))
for i in organ_species_rata_list:
    organ_name,species_rata_list = i
    o.write(organ_name )
    [o.write(','+str(i)) for i in range(1,21)]
    o.write('\n')
    for species,rate_list in species_rata_list:
        o.write(species)
        # print(type(rate_list))
        rate_temp = [float(i.strip('%')) for i in rate_list]
        [o.write(',' + str(i)) for i in rate_temp]
        o.write('\n')
    o.write('\n')
