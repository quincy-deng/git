import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import selfpck.remove_zero as sr

bgi = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\BGI100'
mgi_2557 = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\MGI200_2557'
mgi_2615 = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试\MGI200_2615'

def species_matrix(path):
    os.chdir(path)
    #统计物种和属的数目
    for j in ['bac','fungi','virus','parasite']:
        sp_o = open('species_SDSMRN_matrix_{}.txt'.format(j),'w')
        ge_o = open('genus_SDSMRN_matrix_{}.txt'.format(j),'w')
        species_dict = []
        genus_dict = []
        for i in os.listdir():
            if len(i.split('.')[0]) ==10:
                if i.split('.')[1] ==j:
                    df =pd.read_excel(i)
                    species_dict = species_dict+list(df.Species)
                    genus_dict = genus_dict+list(df.Genus)
        species_set =list(set(species_dict))
        genus_set = list(set(genus_dict))
        sp_o.write('sampleid'+'\t')
        ge_o.write('sampleid'+'\t')
        [sp_o.write(i+'\t') for i in species_set[:-1]]
        sp_o.write(species_set[-1]+'\n')
        [ge_o.write(i+'\t') for i in genus_set[:-1]]
        ge_o.write(genus_set[-1]+'\n')
        for i in os.listdir():
            if len(i.split('.')[0]) ==10:
                if i.split('.')[1] ==j:
                    temp_dict = {}
                    sampleID = i.split('.')[0]
                    sp_o.write(sampleID+'\t')
                    ge_o.write(sampleID+'\t')
                    df = pd.read_excel(i)
                    for x,y in zip(list(df.Species),list(df.SDSMRN)):
                        temp_dict[x] = y
                    for species in species_set[:-1]:
                        if species in temp_dict.keys():
                            sp_o.write(str(temp_dict[species])+'\t')
                        else:
                            sp_o.write(str(0)+'\t')
                    if species_set[-1] in temp_dict.keys():
                        sp_o.write(str(temp_dict[species_set[-1]])+'\n')
                    else:
                        sp_o.write(str(0)+'\n')
                    genus_list  = list(df.Genus)
                    genus_dict = {}
                    for x,y in zip(genus_list,list(df.SDSMRN)):
                        genus_dict.setdefault(x,[]).append(y)
                    for genus in genus_set[:-1]:
                            if genus in genus_dict.keys():
                                ge_o.write(str(sum(genus_dict[genus]))+'\t')
                            else:
                                ge_o.write(str(0)+'\t')
                    if genus_set[-1] in genus_dict.keys():
                        ge_o.write(str(sum(genus_dict[genus_set[-1]]))+'\n')
                    else:
                        ge_o.write(str(0)+'\n')
def species_genus(path,rank=0):
    os.chdir(path)
    species_sum = {}
    genus_sum = {}
    genus_rank_sum ={}
    sampleID_list = []
    for fl in sorted(os.listdir()):
        sampleID,ptg = fl.split('.')[0],fl.split('.')[1]
        if len(sampleID) == 10:
            if sampleID not in sampleID_list:
                sampleID_list.append(sampleID)
        df = pd.read_excel(fl)
        species_list = list(df.Species)
        genus_list = list(df.Genus)
        SDSMRN_list= list(df.SDSMRN)
        temp_dict = {}
        for i in range(len(genus_list)):
            temp_dict[genus_list[i],[]].append(SDSMRN_list[i])
        for i in temp_dict:
            temp_dict[i] =sum(temp_dict[i])
        temp_dict_Species = {}
        for x,y in zip(species_list,SDSMRN_list):
            temp_dict_Species[x]=y

        # genus_sum.setdefault((sampleID,ptg),[])

def df_concat(path):
    os.chdir(path)
    species,genus = [],[]
    for i in os.listdir():
        if i.split('_')[0]=='species' and i.split('_')[1]=='SDSMRN':
            sr.sheet_remove_zero(i,sep='\t')
        if i.split('_')[0]=='genus' and i.split('_')[1]=='SDSMRN':
            sr.sheet_remove_zero(i,sep='\t')

    for i in os.listdir():
        if i.split('_')[0]=='new' and i.split('_')[1]=='genus' and i.split('_')[2]=='SDSMRN':
            genus.append(i)
        if i.split('_')[0]=='new' and i.split('_')[1]=='species' and i.split('_')[2]=='SDSMRN':
            species.append(i)
# species_matrix(bgi)
# species_matrix(mgi_2557)
# species_matrix(mgi_2615)

#合并四种类型表格到一起
def find_target_file(path1):
    os.chdir(path1)
    
    genus_list = []
    flag1 = 0
    for fl in os.listdir():
        
        if len(fl.split('_')) != 4 or fl.split('_')[0] != 'genus':
            continue
        print(fl)
        if flag1 ==0:
            genus_out = '_'.join(fl.split('_')[:3])+'2.txt'
            flag1 += 1
        genus_list.append(pd.read_csv(fl,sep='\t',engine='python'))
    genus_df = pd.concat(genus_list,axis=1)
    
    genus_df.to_csv(os.path.join(os.getcwd(),genus_out),sep='\t',index=False)
    
    species_list = []
    flag2 = 0
    for fl in os.listdir():
        # print(fl.split('_')[0])
        if (len(fl.split('_')) != 4) or (fl.split('_')[0] != 'species'): #
            continue
        print(fl)
        if flag2 ==0:
            species_out = '_'.join(fl.split('_')[:3])+'2.txt'
            # print(species_out)
            flag2 += 1
        species_list.append(pd.read_csv(fl,sep='\t',engine='python'))
    species_df = pd.concat(species_list,axis=1)
    # print(os.path.join(os.getcwd(),species_out))
    species_df.to_csv(os.path.join(os.getcwd(),species_out),sep='\t',index=False)

# find_target_file(bgi)
# find_target_file(mgi_2557)
# find_target_file(mgi_2615)