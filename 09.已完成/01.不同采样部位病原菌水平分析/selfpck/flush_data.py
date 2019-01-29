# -*- coding=utf-8 -*-
# 调整header位置,处理xls和csv格式文件,参数是文件的绝对路径
def check_header(abs_path,test_list):
    file_ext = {'.xls':'\t','.csv':','}
    import os
    import pandas as pd
    import chardet
    boot,fl = os.path.split(abs_path)
    os.chdir(boot)
    sampleID,ptg_type,ext = fl.split('.')[0].split('_')[0].split('-')[0],fl.split('.')[1],os.path.splitext(fl)[1]
    #读取文件,加入encoding是为了避免输出文件的中文乱码问题,以没有header的方式读取
    try:
        # print(abs_path)
        df = pd.read_csv(os.path.join(boot,fl),sep=file_ext[ext],engine='python',header=None)
    except:
        test_list.append(abs_path)
        return test_list
        print('Can not read {}'.format(fl))
    try:
        header_index = df.iloc[:,0].tolist().index('#Sample')           
    except:
        test_list.append(abs_path)
        return test_list
        print('No header in {}'.format(fl))
    if header_index != 0:
        print('Header line:','{:<5d}'.format(header_index,),fl) 
    #去掉header这一行
    new_df = df.drop(header_index)
    ## 取出header这一行
    header = list(df.iloc[header_index])
        # ### 添加header
        # new_df.columns = header
        # if not os.path.exists(os.path.split(boot)[1]):
        #     os.mkdir(os.path.split(boot)[1])
        # os.chdir(os.path.split(boot)[1])
        # new_df.to_csv('.'.join([sampleID,ptg_type,'xls']),sep='\t',encoding="gb2312",index=False)
        
    
    return test_list

#此处处理的文件夹没有其他文件
def deal_dir(path):
    import os
    test_list = []
    import os
    for boot,filenames,files in os.walk(path):
        filenames #no use
        for fl in files:
            test_list= check_header(os.path.join(boot,fl),test_list)
    print('END')
    os.chdir(path)
    with open('no.txt','w') as f:
        for i in test_list:
            f.write(i+'\n')

# deal_dir(r'D:\测试文件')
wrong_file = r'D:\测试文件\no.txt'
test_list = []
for line in open(wrong_file).readlines():
    test_list = check_header(line.rstrip(),test_list)
print(len(test_list))