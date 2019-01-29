import pandas as pd
import numpy as np

file_list = ['new.species.SDSMRN.matrix.txt','species.merge.TOP10.txt','bgi100_mgi200_2557.species.merge.TOP10.txt','bgi100_mgi200_2615.species.merge.TOP10.txt','mgi200_2557_mgi200_2615.species.merge.TOP10.txt']
species_diversity = r'F:\BGI100_MGI200\BGI100_MGI200.data\{}'.format(file_list[0])
df = pd.read_table(species_diversity,index_col='sampleid')

def compare_three_platform(df):
    sample_list = ['17P0589200','17P0589258','17S0287438','17S0287602','17S0588122','17S0588124','17S0588156','17S0590566','18S0133946']
    sample_index = df.index.tolist()
    cols = df.columns.tolist()
    temp_dict = {}
    ## （Abc, aBc, ABc, abC, AbC, aBC, ABC） ##
    temp_dict['types'] = ['bgi100 only','mgi200_2557 only','bgi100 and mgi200_2557 positive','mgi200_2615 only','bgi100 and mgi200_2615 positive',
    'mgi200_2557 and mgi200_2615 positive','positive','sum species']
    for i in range(9):
        bgi = list(df.iloc[i,])
        mgi2557 = list(df.iloc[i+9,])
        mgi2615 = list(df.iloc[i+18])
        a_only,b_only,c_only,pos,a_b,b_c,a_c=0,0,0,0,0,0,0
        for a,b,c in zip(bgi,mgi2557,mgi2615):
            if a==0 and b==0 and c==0:
                continue
            elif a>0 and b>0 and c>0:
                pos += 1
            elif a>0 and b>0 and c==0:
                a_b += 1
            elif a>0 and c>0 and b==0:
                a_c += 1
            elif b>0 and c>0 and a==0:
                b_c += 1
            elif a>0 and b==0 and c==0:
                a_only += 1
            elif b>0 and a==0 and c==0:
                b_only += 1
            else:
                c_only += 1
        sum_species = pos + a_b + a_c + b_c + a_only + b_only + c_only
        # temp_dict[cols[i]] = 
        # print('{}'.format(sample_list[i]))
        # print('positive:{}'.format(pos))
        # print('bgi100 and mgi200_2557 positive:{}'.format(a_b))
        # print('bgi100 and mgi200_2615 positive:{}'.format(a_c))
        # print('mgi200_2557 and mgi200_2615 positive:{}'.format(b_c))
        # # print('single species positive:{}'.format(single_pos))
        # print('species sum:{}\n'.format(sum_species))
        ## （Abc, aBc, ABc, abC, AbC, aBC, ABC） ##
        temp_dict[sample_list[i]] = [a_only,b_only,a_b,c_only,a_c,b_c,pos,sum_species]
        df_t =  pd.DataFrame(data = temp_dict)
    df_t.to_csv(r'F:\BGI100_MGI200\BGI100_MGI200.data\1210species_vn.txt',sep='\t',index=False)
    print('END')


compare_three_platform(df)