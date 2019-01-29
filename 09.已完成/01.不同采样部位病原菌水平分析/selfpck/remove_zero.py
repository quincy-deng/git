import pandas as pd
import os
#删除全为零的列
def strin_cols(df):
    for cols in df:
        try:
            if sum(list(df[cols]))==0:
                df.pop(cols)
        except:
            df.pop(cols)
    return df

def main(file1,sep='xlsx'):
    if sep =='xlsx':
        df = pd.read_excel(file1)
    else:
        df = pd.read_csv(file1,sep='\t',engine='python')
    df = strin_cols(df)
    if sep=='xlsx':
        with pd.ExcelWriter('{}'.format(os.path.join(os.path.dirname(file1),'new_'+os.path.basename(file1)))) as writer:
            df.to_excel(writer,index=False)
    else:
        df.to_csv('{}'.format(os.path.join(os.path.dirname(file1),'new_'+os.path.basename(file1))),sep='\t',index=False,)    