import os
import re
import shutil

#寻找所有的病原文件

bac_file = []
fungi_file = []
parasite_file = []
virus_file = []

def main():
	dir_path = os.getcwd()
	bingyuan_list = ['fungi','bac','parasite','virus']

	for i in bingyuan_list:
		out_dir = os.path.join('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang',i)
		if os.path.exists(out_dir):
			continue
		else:
			os.mkdir(out_dir)

	for pattern,dirname,filenames in os.walk(dir_path):
		print(dirname)
		for filename in filenames:
			if re.search('csv',filename) and re.search('fungi',filename):
				shutil.copy(os.path.join(pattern,filename),os.path.join('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang','fungi'))
			elif re.search('csv',filename) and re.search('bac',filename):
				shutil.copy(os.path.join(pattern,filename),os.path.join('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang','bac'))
			elif re.search('csv',filename) and re.search('parasite',filename):
				shutil.copy(os.path.join(pattern,filename),os.path.join('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang','parasite'))
			elif re.search('csv',filename) and re.search('virus',filename):
				shutil.copy(os.path.join(pattern,filename),os.path.join('/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang','virus'))
if __name__ == 'main':
	main()