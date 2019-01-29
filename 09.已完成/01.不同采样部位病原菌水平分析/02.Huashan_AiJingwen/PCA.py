# tab1
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

iris = load_iris()
# print(iris['data'])
pca = PCA(n_components=2)

# iris['data']来训练PCA模型，同时返回降维后的数据。
datas = pca.fit_transform(iris['data'])
# print(datas)

labels = list(set(iris['target']))
print(datas[iris['target']])
colors = ["r", "b", "g"]


plt.figure(figsize=(16, 10))

for idx, label in enumerate(labels):
    plt.scatter(datas[iris['target']==label][:, 0], datas[iris['target']==label][:, 1], c=colors[idx], label=iris['target_names'][idx])

plt.legend(loc='upper right')
# plt.show()
# plt.savefig("iris.png")