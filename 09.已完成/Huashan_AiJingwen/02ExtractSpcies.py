import os
check_dir = ['bac','fungi','virus','parasite']
iniData_path = r'E:\华山医院原始数据'
# 分别统计原始数据bac等菌种数
for dir_name in check_dir:
    spcies = []
    outpath = os.path.join(os.path.split(iniData_path)[0],dir_name+'.csv')
    o = open(outpath,'w')
    spcies_tmp = []
    for root,dirs,files in os.walk(iniData_path):
        if os.path.split(root)[1] == dir_name:
            for p_file in files:
                flag = 0
                index_spE,index_spCH,index_geE,index_geCH = 0,0,0,0
                sep = {'.csv':',','.xls':'\t'}
                f = open(os.path.join(root,p_file))
                file_content = f.readlines()
                cotent_len = len(file_content)
                n = 0
                for i in range(cotent_len):
                    line_list = file_content[i].rstrip().split(sep[os.path.splitext(p_file)[1]])
                    if line_list[0] == '#Sample':
                        n = i
                        try:
                            index_spE,index_spCH,index_geE,index_geCH = line_list.index('Species'),line_list.index('Chinese'),line_list.index('Genus'),line_list.index('GenusCh')
                            flag = 1
                        except:
                            print(p_file)
                        break
                if flag == 1:
                    # print(n)
                    file_content.pop(n)
                    # print(index_spE,index_spCH,index_geE,index_geCH)
                    for line in file_content:
                        line_list = line.rstrip().split(sep[os.path.splitext(p_file)[1]])
                        # print(line_list)
                        try:
                            spcies_tmp.index(line_list[index_spE])
                        except:
                            spcies_tmp.append(line_list[index_spE])
                            spcies.append(line_list[index_geCH]+','+line_list[index_geE]+','+line_list[index_spCH]+','+line_list[index_spE])
                f.close()
    [o.write(i+'\n') for i in spcies[:-1]]
    o.write(spcies[-1])
    o.close()
                
