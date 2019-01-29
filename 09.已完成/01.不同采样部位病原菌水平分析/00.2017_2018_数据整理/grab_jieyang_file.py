import os
import re
import shutil

# 提取所有的接样表
dir_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet' # 非原始路径，勿用
def main(dir_path):
    for pattern, dirname, filenames in os.walk(dir_path):  # 这里用walk可以遍历所有的文件夹和子文件夹的所有文件
        print(dirname)
        for filename in filenames:
            if re.search('接样', filename):
                shutil.copy(os.path.join(pattern, filename), 'E:\\jieyang_sheet')  # 复制文件到指定路径

if __name__ == '__main__':
    main(dir_path)