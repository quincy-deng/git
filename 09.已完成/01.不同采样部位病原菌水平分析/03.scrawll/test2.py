import pandas as pd
import os

path=r'D:\华山医院\03.各组织matrix和总matrix\各组织matrix'
out_path = r'D:\华山医院\03.各组织matrix和总matrix\总matrix'
def merge_df(path):
    os.chdir(path)
    for fl in os.listdir():
        yield pd.read_table(fl,engine='python',index_col='#Sample')

merge_dfs = list(merge_df(path))
df_merge = pd.concat(merge_dfs)
df_merge.to_csv(os.path.join(out_path,'merge_matrix.xls'),sep='\t')