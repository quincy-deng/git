import os
import pandas as pd
import shutil
#allfile = os.listdir(r'C:\Users\邓秋洋\Desktop\合并\bac') #统计bac目录下样本的数目
#s = set([])
#for i in allfile:
   # filename = os.path.basename(i)
  #  sampleID = filename.split('.')[0]
 #   s.add(sampleID)

def main():
    sample_jieyang = {}
    sample_allcsv = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\all_csv2.csv'
    data_path = r'C:\Users\邓秋洋\Desktop\病原分类数据'
    a = [os.path.join(data_path, i) for i in  ['bac', 'parasite', 'virus', 'fungi']]
    bypogen = {}
    for i in a:
        bypogen[os.path.split(i)[1]] = os.listdir(i)
    # df = open(sample_allcsv)
    # [print(df.readline()) for i in range(5)]
    df = pd.read_csv(sample_allcsv,engine = 'python',encoding = 'utf-8-sig')
    for i in range(len(df)):
        sample_jieyang[str(df.loc[i,'样品编号']).split('-')[0]] = df.loc[i,'样品类型']
    sample_sum = {}
    sample_type = []
    for i in sample_jieyang:
        if sample_jieyang[i] not in sample_type:
            sample_type.append(sample_jieyang[i])
            sample_sum[sample_jieyang[i]] = [i]
        else:
            sample_sum[sample_jieyang[i]].append(i)

    for sample_type in sample_sum: #遍历取样类型，比如全血，脑脊椎液等
        if not os.path.exists(os.getcwd() + '\\' + str(sample_type)):
            os.mkdir(os.getcwd() + '\\' + str(sample_type)) # 创建样品目录
        [os.mkdir(os.getcwd() + '\\' + str(sample_type) + '\\' + i) for i in ['bac', 'parasite', 'virus', 'fungi'] if not os.path.exists(os.getcwd() + '\\' + str(sample_type) + '\\' + i)] #创建位于取样类型下的病毒、细菌等四大类病原菌的目录
        for sample_ID in sample_sum[sample_type]: #遍历收样表某一种取样类型所有的样品编号,samplr_ID为收样表的编号
            for byogen_path in bypogen: #遍历病毒、细菌等四大类病原菌的数据目录，byogen是['bac', 'parasite', 'virus', 'fungi']中的一种
                data_sampleID = {(i.split('.')[0]):i for i in bypogen[byogen_path]} # 拆分4种病原菌文件名中的样品编号
                if sample_ID in data_sampleID: #从data文件夹匹配收样表的样品编号
                    shutil.copy(os.path.join(data_path, byogen_path,data_sampleID[sample_ID]), os.getcwd() + '\\' + sample_type + '\\' + byogen_path)

if __name__ =='__main__':
    main()