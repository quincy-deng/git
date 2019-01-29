
from matplotlib_venn import venn3
from matplotlib.cbook import flatten
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# 简单的子图
def subplot1():
    data = [1, 2, 3, 4, 5]
    fig = plt.figure()
    fig.suptitle("Title for whole figure", fontsize=16)
    ax = plt.subplot("212")
    ax.set_title("Title for first plot")
    ax.plot(data)
    plt.show()

# 设置更多的子图
def subplot2():
    #子图相关设置
    figure, axes = plt.subplots(3, 3, figsize=(18.5,10.5))
    figure.suptitle('species distribution in bgi100 and mgi200')
    # print(axes)
    path = r'F:\BGI100_MGI200\BGI100_MGI200.data\1210species_vn.txt'
    df = pd.read_table(path)
    cols=df.columns.tolist()
    data = [tuple(df[col])[:-1] for col in cols[1:]]
    max_area = max(map(sum, data))
    
    # 根据数据设置子图大小
    def set_venn_scale(vd, ax, true_area, reference_area=max_area):
        sx = np.sqrt(float(reference_area)/true_area)
        sy = max(vd.radii)*1.5
        ax.set_xlim(-sx, sx)
        ax.set_ylim(-sy, sy)
        
    for a,d,col_name in zip(flatten(axes), data,cols[1:]):
        vd = venn3(subsets = d, set_labels = ('bgi100', 'mgi200(1)','mgi200(2)'), ax=a)
        a.set_title(col_name)
        # set_venn_scale(vd, a, sum(d))

    figure.tight_layout(pad=0.1)
    plt.show()

def 