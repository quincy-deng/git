import re
import os
import sys
#处理根据组织归类好的(‘肠道感染\腹膜透析液\bac\18S4339681.bac.anno.xls’)原始文件，提取出目的数据，整合到如‘肠道感染’类别下所有bac归到一起（肠道感染\bac.txt）。

def judge_sep(csv):
    if os.path.splitext(csv)[1] == '.csv':
        return b','
    elif  os.path.splitext(csv)[1] =='.xls' or os.path.splitext(csv)[1] == '.xlsx':
        return b'\t'

def found_header(df,sep):
    n = 0 
    for i in df:
        if i.split(sep)[0] == r'#Sample':
            for k in range(len(i.split())):
                if i[k] == 'Species':
                    Species = k
                elif i[k] =='SMRN':
                    SMRN = k
            return Species, SMRN
        n += 1
    return -1

def analysis_single_sample(csv): # 解析单个csv文件
    sep = judge_sep(csv)
    # print(csv)
    df = open(csv, 'rb')
    header = df.readline().split(sep)
    data_SMRN = {}
    # print(header[0])
    if not re.search(b'#Sample', header[0]):
        data_frame = df.readlines()
        df.seek(0, os.SEEK_SET)
        Species, SMRN = found_header(data_frame, sep)
        print('header_row:', 0)
    else:
        for i in range(len(header)):
            if header[i] == b'Species':
                Species = i
            elif header[i] == b'SDSMRN':
                SMRN = i
    # print(df.readline(),sep, Species, SMRN)
    for i in df.readlines():
        data_SMRN[i.split(sep)[Species]] = i.split(sep)[SMRN]
    df.close()    
    return data_SMRN

def read_csv(organs_path, outpath): #解析单个组织（如肺部），organs_path = './dengqiuyang/06.采样部位整理/肺部'
    bac_dict, virus_dict, fungi_dict, parasite_dict = [{} for i in range(4)] # 谨记教训
    dict_list = {'bac':bac_dict, 'virus':virus_dict, 'fungi':fungi_dict, 'parasite':parasite_dict}
    for organ in [os.path.join(organs_path,i) for i in os.listdir(organs_path)]:# organ = './dengqiuyang/06.采样部位整理/肺部/肺泡灌洗液'     
        for bac in [os.path.join(organ,i) for i in os.listdir(organ)]:          
            dict_name = os.path.basename(bac)
            for csv_file in [os.path.join(bac, i) for i in os.listdir(bac)]:
                data_SMRN = analysis_single_sample(csv_file) #解析单个个体csv文件
                for k,v in data_SMRN.items():
                    dict_list[dict_name].setdefault(k,[]).append(v) #合并字典
    #  print(sys.getsizeof(dict_list['bac']), sys.getsizeof(dict_list['virus']))
    for k,v in dict_list.items():
        f = open(os.path.join(outpath,k+'.txt'),'wb') #编码问题比较麻烦了
        for x,y in v.items():
            f.write(x+b':\t')
            for i in y: 
                f.write(i+b'\t')
            f.write(b'\n')
        f.close()
        
def main():
    data_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理02版'
    outdata_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版'
    for organ in [os.path.join(data_path, i) for i in os.listdir(data_path)]: # 遍历得到采样部位(如肺部)文件夹名
        print(os.path.split(organ))
        outpath = os.path.join((outdata_path), os.path.split(organ)[1])
        if not os.path.exists(os.path.join((outdata_path), os.path.split(organ)[1])):
            os.makedirs(os.path.join(outdata_path, os.path.split(organ)[1])) # 创建采样部位(如肺部)输出文件夹名
        # [os.makedirs(os.path.join(outdata_path,i)) for i in ['bac', 'fungi', 'parasite', 'virus'] if not os.path.exists(os.path.join(outdata_path, i))]
        read_csv(organ,outpath)
if __name__ == '__main__':
    main()