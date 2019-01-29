# from bs4 import BeautifulSoup
# import re
# from urllib.request import urlopen
# import random

# base_url = "https://baike.baidu.com"
# his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
# url = base_url + his[-1]

# html = urlopen(url).read().decode('utf-8')
# soup = BeautifulSoup(html, features='lxml')
# # print(soup.find('h1').get_text(), '    url: ', his[-1])so
# sub_urls = soup.find_all('a', {"target":"_blank", "href":re.compile("/item/(%.{2})+$")})

# if len(sub_urls) != 0:
#     his.append(random.sample(sub_urls, 1)[0]['href'])
#     # his.append(random.sample(sub_urls, 1)[0]['href'])
# else:
#     his.pop()

# print(his)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\vector1.csv' 
df=pd.read_csv(file_path, header=0, encoding='utf-8')
df1=df.ix[:,2:]
kmeans = KMeans(n_clusters=3, random_state=10).fit(df1)
df1['group']=kmeans.labels_
df_count_type=df1.groupby('group').apply(np.size)
 
 
 
##各个类别的数目
df_count_type
##聚类中心
kmeans.cluster_centers_
##新的dataframe，命名为new_df ，并输出到本地，命名为new_df.csv。
new_df=df1[:]
new_df
new_df.to_csv('new_df.csv')
 
##将用于聚类的数据的特征的维度降至2维，并输出降维后的数据，形成一个dataframe名字new_pca
pca = PCA(n_components=2)
new_pca = pd.DataFrame(pca.fit_transform(new_df))
 
##可视化
d = new_pca[new_df['group'] == 0]
plt.plot(d[0], d[1], 'r.')
d = new_pca[new_df['group'] == 1]
plt.plot(d[0], d[1], 'go')
d = new_pca[new_df['group'] == 2]
plt.plot(d[0], d[1], 'b*')
plt.gcf().savefig('kmeans.png')
plt.show()