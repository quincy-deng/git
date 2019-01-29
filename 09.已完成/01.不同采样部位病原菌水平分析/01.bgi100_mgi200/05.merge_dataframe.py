#合并表单,纵向合并数据，会产生一些空值。可以用Excel的查找选项下的的定位条件，然后选择“空值”；顶部赋值栏输入“0”，敲击键盘“Ctrl+Enter”组合键，给所选单元格赋“0”的值。
import os
import pandas as pd
def merge_df():
    path = r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试'
    df=[]
    for boot,dirnames,filenames in os.walk(path):
        dirnames #不使用
        for fl in filenames:
            if fl !='species_SDSMRN_matrix2.txt':
                continue
            print(boot+'\\'+fl)
            df.append(pd.read_csv(os.path.join(boot,fl),sep='\t',engine='python'))
    new_df = pd.concat(df,ignore_index=True)
    new_df.to_csv(os.path.join(path,'species.SDSMRN.matrix.txt'),sep='\t',index=False)
# merge_df()
#删除全为零的列
def strin_cols(df):
    for cols in df:
        try:
            if sum(list(df[cols]))==0:
                df.pop(cols)
        except:
            print(df[cols])
    return df
os.chdir(r'D:\wechat\WeChat Files\huanghujian1990\Files\200平台测试')
df = pd.read_csv('genus.SDSMRN.matrix.txt',sep='\t',engine='python')
new_df = strin_cols(df)
new_df.to_csv('new.genus.SDSMRN.matrix.txt',sep='\t',index=False)