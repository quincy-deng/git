# coding =utf-8
matrix_file = r'D:\华山医院\03.各组织matrix和总matrix\总matrix\merge_matrix.xls'
ngsResult_file = r'D:\华山医院\a.华山医院给出NGS结果\12.5重新整理中英文.xlsx'
Groupfile = r'D:\华山医院\03.各组织matrix和总matrix\Group_pathogen.xls'
import xlrd
import pandas as pd
import os

def species_genus():
    os.chdir(r'D:\华山医院\00.4种病原菌.菌种统计')
    species_genus_dict = {}
    for fl in os.listdir():
        df = pd.read_excel(fl)
        for z,b in zip(list(df['Species']),list(df['Genus'])):
            species_genus_dict[z] = b
    return species_genus_dict
def obtain_organame_ngsresult(ngsResult_file):
    genus_dict = species_genus()
    sheet_names = xlrd.open_workbook(ngsResult_file).sheet_names()
    group_dict = {}
    jishu =set([])
    for sheet_name in sheet_names:
        df = pd.read_excel(ngsResult_file,sheet_name=sheet_name)
        #new_NGS_result;标本编号,标本类型
        for a,b,c in zip(list(df['标本编号']),list(df['new_NGS_result']),list(df['标本类型'])):
            if len(b.split(';'))==1:
                try:
                    b = b.split(',')[1]
                    try:
                        b = genus_dict[b]
                    except:
                        if b != 'Mycobacterium_tuberculosis_complex_group':
                            b = '*'+b[:17]
                        else:
                            b = 'Mycobacterium_tuberculosis_complex_group'
                except:
                    b='Negative'
                jishu.add(b)           
            else:
                t = []
                for i in b.split(';'):
                    try:
                        n = i.split(',')[1]
                        try:
                            t.append(genus_dict[n])
                        except:
                            if n != 'Mycobacterium_tuberculosis_complex_group':
                                t.append('*'+n[:17])
                            else:
                                t.append('Mycobacterium_tuberculosis_complex_group')
                    except:
                        if b == 'Filifactor;alocis':
                            t.append(genus_dict['Filifactor_alocis'])
                        elif a=='17S0587286':
                            t=[genus_dict[b.split(';')[1].split(',')[1]]]
                b = ' | '.join(t[:1])
                jishu.add(b)
            group_dict[a[:10]] = (b,c)
    print(jishu)
    return group_dict

def obtain_organame_pathogen(ngsResult_file):
    sheet_names = xlrd.open_workbook(ngsResult_file).sheet_names()
    group_dict = {}
    for sheet_name in sheet_names:
        df = pd.read_excel(ngsResult_file,sheet_name=sheet_name)
        #new_NGS_result;标本编号,标本类型
        for a,b,c in zip(list(df['标本编号']),list(df['new_NGS_result']),list(df['标本类型'])):
            if len(b.split(';'))==1:
                try:
                    b,kk = b.split(',')[0],b.split(',')[1]
                except:
                    # print(b)
                    b='Negative'        
            else:
                t = []
                for i in b.split(';'):
                    try:
                        n,kk = i.split(',')[0],i.split(',')[1]
                        t.append(n)
                    except:
                        # print(b)
                        if b == 'Filifactor;alocis':
                            t.append('bac')
                        elif a=='17S0587286':
                            t.append(b.split(';')[1].split(',')[0])
                        else:
                            t.append('Negative')
                b = ' | '.join(sorted(list(set(t))))
            group_dict[a[:10]] = (b,c)
    return group_dict
# 标本编号:(new_NGS_result,标本类型)
# group_dict=obtain_organame_ngsresult(ngsResult_file)
group_dict = obtain_organame_pathogen(ngsResult_file)

# 取出matrix的标本编号
df = pd.read_table(matrix_file,engine='python')
sampleids =list(df['#Sample'])

# 输出matrix标本编号结果
group_list = []
for spampleid in sampleids:
    x,y = group_dict[spampleid[:10]]
    group_list.append([spampleid,y,x])

# print(group_list)
group_df = pd.core.frame.DataFrame(group_list,columns=['#Sample','OrganType','PathogenType'])
group_df.to_csv(Groupfile,sep='\t',index=False,encoding='gbk')