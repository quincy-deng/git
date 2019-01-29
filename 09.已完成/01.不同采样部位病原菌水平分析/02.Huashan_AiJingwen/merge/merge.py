import os
import pandas as pd
test = {}
for i in os.listdir():
    if i=='merge.py':
        continue
    test.setdefault(i.split('.')[1],[]).append(i)
for k,v in test.items():
    seps = {'xls':'\t','csv':','}
    dfs = [pd.read_csv(i,sep=seps[i.split('.')[-1]],engine='python') for i in v]
    df = pd.concat(dfs)
    cols=[]
    for col in ['#Sample','Species','Genus','Re_Abu','SDSMRN','SDSMRNG']:
        if col in df.columns.tolist():
            cols.append(col)
    df=df[cols]
    df.to_csv(r'/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/华山医院/0103.merge/{}.merge.xls'.format(k),sep='\t',index=False)
