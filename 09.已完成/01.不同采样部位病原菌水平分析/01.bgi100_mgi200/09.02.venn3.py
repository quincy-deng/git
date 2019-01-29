from matplotlib_venn import venn3
from matplotlib.cbook import flatten
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

figure, axes = plt.subplots(3, 3, figsize=(18.5,10.5))
figure.suptitle('species distribution in bgi100 and mgi200')
# print(axes)
path = r'F:\BGI100_MGI200\BGI100_MGI200.data\1210species_vn.txt'
df = pd.read_table(path)
cols=df.columns.tolist()
data = [tuple(df[col])[:-1] for col in cols[1:]]
max_area = max(map(sum, data))

def set_venn_scale(vd, ax, true_area, reference_area=max_area):
    sx = np.sqrt(float(reference_area)/true_area)
    sy = max(vd.radii)*1.5
    ax.set_xlim(-sx, sx)
    ax.set_ylim(-sy, sy)
    

for a,d,col_name in zip(flatten(axes), data,cols[1:]):
    vd = venn3(subsets = d, set_labels = ('bgi100', 'mgi200(1)','mgi200(2)'), ax=a)
    a.set_title(col_name)
    # set_venn_scale(vd, a, sum(d))

# axes[1,2].axis('off')

figure.tight_layout(pad=0.1)
plt.show()