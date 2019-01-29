import xlrd
import pandas as pd
import os
class Deal_result(object):
    def __init__(self,file_path):
        self.file_path =file_path
        self.df = None
        self.out_dict ={}
    def out_file(self):
        for organ_type in self.out_dict.keys():
            f = open('{}.xls'.format(os.path.join(os.path.split(self.file_path)[0],organ_type)),'w')
            f.write('\t'.join(['sampleid','species'])+'\n')
            for sample_result in self.out_dict[organ_type]:
                f.write('\t'.join(sample_result)+'\n')

    def Extract_data(self):
        data = self.Read_excel()
        for sheet_data in list(data):
            x,y,z = sheet_data
            for a,b,c in zip(x,y,z):
                self.out_dict.setdefault(b,[]).append([a,c])

    def Read_excel(self):
        sheets = xlrd.open_workbook(self.file_path).sheet_names()
        for sheet in sheets:
            print(sheet)
            self.df = pd.read_excel(self.file_path,sheet_name=sheet)
            yield list(self.df['标本编号']),list(self.df['标本类型']),list(self.df['new_NGS_result'])

file_path = r'D:\华山医院\1114医院感染数据\12.5重新整理中英文.xlsx'
result = Deal_result(file_path)
result.Extract_data()
result.out_file()