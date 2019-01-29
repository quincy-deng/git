import os
import xlrd
import pandas as pd
import re
dir1 = r'C:\Users\邓秋洋\Desktop\jieyang_sheet'
all_xls = os.listdir(dir1)
# re.comepile('\~\$\w+.xls[x?]$')
def main(all_xls):
    j = 0
    for i in all_xls:
        if re.search('xls',i) and not re.search('~' , i) and not re.search('csv', i): # 读取bug问题原来是读到了系统的隐藏文件，比如‘~$2018-06-20病原接样表-武汉.xlsx’
            csv_name = os.path.basename(i)
            csv_name = csv_name + '.2.csv'
            csv_filepath = os.path.join(dir1, csv_name)
            xls_filepath = os.path.join(dir1,i)
            print("xls: ", xls_filepath)
            data = pd.read_excel(xls_filepath, sheet_name = '病原快检')
            if '样品类型' in data.columns: #不能使用data['样品类型']判断列是否存在
                temp = data.loc[:,['样品类型','样品编号']]
                temp.to_csv(csv_filepath, encoding='utf-8-sig', index = False)
            else:
                j +=1
            print(j)
if __name__ == '__main__':
    main(all_xls)