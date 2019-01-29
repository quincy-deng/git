import pandas as pd
import os

#检查参数是文件夹还是文件名
def check_fileType(file_dir):
    if os.path.isfile(file_dir):
        print(os.path.split(file_dir)[1])
        return 0
    elif os.path.isdir(file_dir):
        print(os.path.abspath(file_dir))
        return 1
    else:
        raise OSError('please check file again')
#删除全为0的行
def strin_rows(df):
    for index,rows in df.iterrows():
        try:
            index_list = []
            if sum(list(rows)[1:]) ==0:
                print(list(rows)[0])
                index_list.append(index)
        except:
            raise TypeError('please check content type')
    df = df.drop(index_list)
    return df
#删除全为零的列
def strin_cols(df):
    flag=1
    for cols in df:
        if flag ==1:
            flag +=1
            continue
        try:
            if sum(list(df[cols]))==0:
                df.pop(cols)
        except:
            df.pop(cols)
    return df

def main(file1,sep):
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
  
def dir_handle(dir1,sep):
    for file1 in os.listdir():
        main(file1,sep)

def sheet_remove_zero(file_dir,sep='xlsx'):
    flag = check_fileType(file_dir)
    if flag == 0:
        main(file_dir,sep)
    elif flag ==1:
        dir_handle(file_dir,sep)