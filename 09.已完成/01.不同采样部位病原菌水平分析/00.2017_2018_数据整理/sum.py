# import pandas as pd
# all_csv = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\all_csv2.csv'
# file_path = r'C:\Users\邓秋洋\Documents\WeChat Files\huanghujian1990\Files\复旦中山感染科.xlsx'
# csv_filepath = r'C:\Users\邓秋洋\Documents\WeChat Files\huanghujian1990\Files\复旦中山感染科样本编号.xlsx'
# data = pd.read_excel(file_path)
# o = open(all_csv, 'rb')
# o.readline()
# sum1 = []
# for i in o.readlines():
#     sum1.append(i.rstrip().split(b',')[1])
# all_sample = data.loc[:,['NGS编号']]
# all_sample.to_csv(csv_filepath, encoding='utf-8-sig', index = False)
# f = open(csv_filepath,'rb')
# f.readline()
# n = 0
# k = 0

# for i in f.readlines():
#     k += 1
#     samp_num = i.rstrip().split()[0]
#     if samp_num in sum1:
#         print(samp_num)
#         n += 1
# print('交集数量:', n,'\n', '样本总数:', k, '\n', '交集比例:', float(n/k))
import sys

# input 2 vector array
# output pearson correlation score
def PearsonCorrelationSimilarity(vec1, vec2):
	value = range(len(vec1))

	sum_vec1 = sum([ vec1[i] for i in value])
	sum_vec2 = sum([ vec2[i] for i in value])

	square_sum_vec1 = sum([ pow(vec1[i],2) for i in  value])
	square_sum_vec2 = sum([ pow(vec2[i],2) for i in  value])

	product = sum([ vec1[i]*vec2[i] for i in value])

	numerator = product - (sum_vec1 * sum_vec2 / len(vec1))
	dominator = ((square_sum_vec1 - pow(sum_vec1, 2) / len(vec1)) * (square_sum_vec2 - pow(sum_vec2, 2) / len(vec2))) ** 0.5

	if dominator == 0:
		return 0
	result = numerator / (dominator * 1.0)

	return result

vec1 = [0, 22, 22, 5.0, 3.0, 3, 2, 3, 3, 4, 4, 2.5]
vec2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

from math import sqrt

def multipl(a,b):
    sumofab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sumofab+=temp
    return sumofab
 
def corrcoef(x,y):
    n=len(x)
    #求和
    sum1=sum(x)
    sum2=sum(y)
    #求乘积之和
    sumofxy=multipl(x,y)
    #求平方和
    sumofx2 = sum([pow(i,2) for i in x])
    sumofy2 = sum([pow(j,2) for j in y])
    num=sumofxy-(float(sum1)*float(sum2)/n)
    #计算皮尔逊相关系数
    den=sqrt((sumofx2-float(sum1**2)/n)*(sumofy2-float(sum2**2)/n))
    return num/den

print(PearsonCorrelationSimilarity(vec1, vec2), corrcoef(vec1, vec2))