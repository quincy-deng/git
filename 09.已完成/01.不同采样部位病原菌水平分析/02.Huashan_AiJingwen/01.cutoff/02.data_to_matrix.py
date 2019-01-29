# 输入需要提取:data目录,IDs,列名称,和任务ID
import os
import sys
sys.stdout = open(r'D:\华山医院\1225数据整理需求\lackID.xls','w')
import pandas as pd
class RawData_to_Matrix(object): 
    def __init__(self,RawdataDir,sampleids,col_names,job_id):
        self.RawdataDir = RawdataDir
        self.sampleids = sampleids
        self.col_names = col_names
        self.job_id = job_id
        self.files = None
        self.matrix = None

    # 获得指定数据路径下所有原始文件
    def obtain_rawdata_files(self):
        for root,dirs,files in os.walk(self.RawdataDir):
            dirs # No use
            for fl in files:
                if fl.split('.')[-1]!='xls' and fl.split('.')[-1]!='csv':
                    continue
                elif fl[0]=='.':
                    continue
                yield os.path.join(root,fl)
    
    # 根据sampleid找出所有包含此id的文件
    def return_files(self):
        print('\tsearching for {} samples!'.format(len(self.sampleids)))
        rawdata_list = list(self.obtain_rawdata_files())
        sample_dict = {}
        # 根据sampleid生成文件列表
        for i in rawdata_list:
            try:
                sample_dict.setdefault(os.path.split(i)[1][:10],[]).append(i) 
            except:
                print("{} is not a rawdatafile".format(i)) # 文件后缀正确但不是原始文件  
        # 根据指定sampleid返回文件列表
        for sampleid in self.sampleids:
            try:
                yield sample_dict[sampleid]
            except:
                print('\tlose {} rawdatafile'.format(sampleid)) #缺少目的文件
                pass
    
    # 过滤同类型的病原文件
    def return_format_BacFungiParasiteVirus(self):
        files_list = list(self.return_files())
        # print(len(files_list))
        for sample_file in files_list:
            sample_dict ={}
            for fl in sample_file:
                sample_dict.setdefault(os.path.split(fl)[-1].split('.')[1],[]).append(fl)
            sample_list = []
            for ptg,files in sample_dict.items():
                if len(files)>1:
                    fls_size = [os.path.getsize(fl) for fl in files]
                    index = fls_size.index(max(fls_size)) # 选取更大的文件
                    sample_list.append(files[index])
                    continue
                sample_list.append(files[0])
            yield sample_list # 返回四种文件
    
    def col_match(self,df):
        for col in self.col_names:
            if col in df.columns.tolist():
                yield col

    def merge_df(self,sample_file):
        df =pd.DataFrame()
        split_ext={'xls':'\t','csv':','}
        for fl in sample_file:
            # print(fl)
            try:
                df=pd.read_csv(fl,sep=split_ext[fl.split('.')[-1]],engine='python',header=None)
                # print(df.shape)
            except:
                print('{}\tempty file'.format(fl))
                pass
            if df.empty:
                continue
            for index,row in df.iterrows():
                if list(row)[0]=='#Sample':
                    # print(row)
                    df = df.drop(index)
                    df.columns = list(row)
            cols = list(self.col_match(df))
            if os.path.split(fl)[1].split('.')[1]=='virus':
                try:
                    df=df.assign(SDSMRNG =sum([int(i) for i in list(df['SDSMRN'])]))
                except:
                    print(fl)
            df2 = df[cols]
            yield df2
    def merge_bacfungiparasitevirus(self):
        samples_file = list(self.return_format_BacFungiParasiteVirus())
        print('found {} samples'.format(len(samples_file)))
        os.chdir(self.RawdataDir)
        # if not os.path.exists(self.job_id):
        #     os.makedirs(self.job_id)
        # os.chdir(self.job_id)
        for sample_file in samples_file:
            df = list(self.merge_df(sample_file))
            if df==[]:
                continue     
            merge_df = pd.concat(df)
            # merge_df.to_csv('{}.merge.xls'.format(os.path.split(sample_file[0])[1].split('.')[0][:10]),sep='\t',index=False)
    
def main():
    data_path=r'D:\华山医院\01.华山医院NGS测序报告'
    path = r'D:\华山医院\1225数据整理需求\表头修改2.xlsx'
    import pandas as pd
    df = pd.read_excel(path)
    sampleids = list(df['标本编号'])
    colnames=['#Sample','Species','Genus','Re_Abu','SDSMRN','SDSMRNG']
    jobs = RawData_to_Matrix(data_path,sampleids,colnames,'1227.merge')
    jobs.merge_bacfungiparasitevirus()

main()

# def main()
#     path =r'D:\华山医院\b.NGS结果.组织分类'
#     data_path= r'D:\华山医院\01.华山医院NGS测序报告'
#     os.chdir(path)
#     for fl in os.listdir():
#         os.chdir(path)
#         print('Treat {} organ!'.format(fl.split('.')[0]))
#         if os.path.isdir(fl):
#             continue
#         df = pd.read_table(fl,header=None,names=['#Sample','NGS results'],engine='python')
#         ids = list(set([i[:10] for i in list(df['#Sample'])]))
#         # print(ids)
#         col_name ='SDSMRN'
#         job_id = fl.split('.')[0]
#         jobs = RawData_to_Matrix(data_path,ids,col_name,job_id)
#         jobs.merge_bacfungiparasitevirus()
#         jobs.produce_matrix()
#         print('#### {} complete ####'.format(fl.split('.')[0])) 

# if __name__ == "__main__":
#     main()