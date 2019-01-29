import pandas as pd
import numpy as np

file_list = ['new.species.SDSMRN.matrix.txt']
species_diversity = r'F:\BGI100_MGI200\BGI100_MGI200.data\{}'.format(file_list[0])
df = pd.read_table(species_diversity,index_col='sampleid')

def compare_three_platform(df):
    sample_list = ['17P0589200','17P0589258','17S0287438','17S0287602','17S0588122','17S0588124',
    '17S0588156','17S0590566','18S0133946']
    ## （Abc, aBc, ABc, abC, AbC, aBC, ABC） ##
    for i in range(9):
        cols = df.columns.tolist()
        bgi = list(df.iloc[i,])
        bgi_arr=list(np.array(bgi).argsort())[::-1]
        
        mgi2557 = list(df.iloc[i+9,])
        mgi1_arr = list(np.array(mgi2557).argsort())[::-1]
        
        mgi2615 = list(df.iloc[i+18])
        mgi2_arr = list(np.array(mgi2615).argsort())[::-1]
        
        intersection = {}
        for a,b,c,d in zip(bgi,mgi2557,mgi2615,cols):
            if a==0 and b==0 and c==0:
                continue
            elif a>0 and b>0 and c>0:
                intersection[d] = 'abc'
            elif a>0 and b>0 and c==0:
                intersection[d] = 'ab'
            elif a>0 and c>0 and b==0:
                intersection[d] = 'ac'
            elif b>0 and c>0 and a==0:
                intersection[d] = 'bc'
            elif a>0 and b==0 and c==0:
                intersection[d] = 'a'
            elif b>0 and a==0 and c==0:
                intersection[d] = 'b'
            else:
                intersection[d] = 'c'
        temp_a,temp_b,temp_c = [],[],[]
        for a,b,c in zip(bgi_arr,mgi1_arr,mgi2_arr):
            if bgi[a]!=0:
                temp_a.append([cols[a],intersection[cols[a]]])
            if mgi2557[b]!=0:
                temp_b.append([cols[b],intersection[cols[b]]])
            if mgi2615[c]!=0:
                temp_c.append([cols[c],intersection[cols[c]]])
        df1=pd.core.frame.DataFrame(temp_a,columns = ['bgi100','section'])
        df2= pd.core.frame.DataFrame(temp_b,columns = ['mgi200_1','section'])
        df3= pd.core.frame.DataFrame(temp_c,columns = ['mgi200_2','section'])
        df1.to_csv(r'F:\BGI100_MGI200\BGI100_MGI200.data\1212species_intersection_bgi_{}.txt'.format(sample_list[i]),sep='\t',index=False)
        df2.to_csv(r'F:\BGI100_MGI200\BGI100_MGI200.data\1212species_intersection_mgi1_{}.txt'.format(sample_list[i]),sep='\t',index=False)
        df3.to_csv(r'F:\BGI100_MGI200\BGI100_MGI200.data\1212species_intersection_mgi2_{}.txt'.format(sample_list[i]),sep='\t',index=False)
    print('END')

compare_three_platform(df)
