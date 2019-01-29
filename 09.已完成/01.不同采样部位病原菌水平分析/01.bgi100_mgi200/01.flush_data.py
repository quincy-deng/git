# 调整header位置，输出excel文件
def check_header(path):
	import os
	import pandas as pd
	file_ext = {'.xls':'\t','.csv':','}
	for root,filenames,files in os.walk(path):
		filenames #no use
		for fl in files:
			os.chdir(root)
			sampleID,ext = fl.split('.')[0],os.path.splitext(fl)[1]
			# print(ext)
			if len(sampleID)==10 and ext in file_ext.keys():
				f = open(fl)
				fl_content = f.readlines()
				f.close()
				fl_content_list = [i.split(file_ext[ext]) for i in fl_content]
				# print(fl_content_list)
				flag = 0
				for line in fl_content_list:
					if line[0] == '#Sample':
						break
					flag += 1
				if flag !=0:
					header = fl_content_list[flag]
					# print(fl)
					fl_content_list.pop(flag)
					fl_content_list.insert(0,header)
				df = pd.core.frame.DataFrame(fl_content_list[1:],columns = fl_content_list[0])
				try:
					with pd.ExcelWriter(os.path.splitext(fl)[0]+'.xlsx') as writer:
						df.to_excel(writer,index=False)
					os.remove(fl)
				except:
					print(fl)
			elif ext in file_ext.keys():
				print(fl)
			# print(fl)
