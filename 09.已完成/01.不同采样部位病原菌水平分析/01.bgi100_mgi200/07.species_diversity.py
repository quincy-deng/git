import pandas as pd
import numpy as np

def compare_three_platform(df):
    sample_index = df.index.tolist()
    cols = df.columns.tolist()
    diver = []
    sum_list = []
    for col in cols:
        col_content = df[col].tolist()
        temp_dict = {}
        for x,y in zip(sample_index,col_content):
            temp_dict.setdefault(x,[]).append(y)
        for x,y in temp_dict.items():
            a,b,c =y
            if a==0 and b==0 and c==0:
                continue
            elif a == 0 or b==0 or c==0:
                diver.append((x,col,a,b,c,))
                sum_list.append(max([a,b,c]))
    return sum_list,diver
def compare_two_platform(df):
    sample_index = df.index.tolist()
    cols = df.columns.tolist()
    diver = []
    sum_list = []
    for col in cols:
        col_content = df[col].tolist()
        temp_dict = {}
        for x,y in zip(sample_index,col_content):
            temp_dict.setdefault(x,[]).append(y)
        for x,y in temp_dict.items():
            a,b =y
            if a==0 and b==0:
                continue
            elif a == 0 or b==0:
                if a+b >10:
                    diver.append((x,col,a,b))
                    sum_list.append(max([a,b]))
    return sum_list,diver
# print(diver)
file_list = ['new.species.SDSMRN.matrix.txt','species.merge.TOP10.txt','bgi100_mgi200_2557.species.merge.TOP10.txt','bgi100_mgi200_2615.species.merge.TOP10.txt','mgi200_2557_mgi200_2615.species.merge.TOP10.txt']
species_diversity = r'F:\BGI100_MGI200\BGI100_MGI200.data\{}'.format(file_list[0])
df = pd.read_table(species_diversity,index_col='sampleid')
# sum_list,diver=compare_two_platform(df)
sum_list,diver=compare_three_platform(df)
arr = np.array(sum_list)
col_index =list(arr.argsort()[])[::-1]
top = [diver[i] for i in col_index]
print(top)