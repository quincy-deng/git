import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import pandas as pd

def int2bin(n):
    s = bin(n)[2:]
    return (3-len(s))*'0'+s
                            # 1 ⇒ '001'
                            # 2 ⇒ '010'
                            # 3 ⇒ '011'
                            # ...
                            # 7 ⇒ '111'


path = r'F:\BGI100_MGI200\BGI100_MGI200.data\1210species_vn.txt'
df = pd.read_table(path)
cols=df.columns.tolist()
idt = list(df[cols[0]][:-1])

# figure, axes = plt.subplots(2, 3, figsize=(11.69,5.5))

# （Abc, aBc, ABc, abC, AbC, aBC, ABC）
for n in range(9):
    v = venn3(subsets=(1, 1, 1, 1, 1, 1, 1))
    plt.subplot(331+n)
    # plt.set_size_inches(18.5,10.5)
    data = list(df[cols[n+1]])[:-1]
    for i in range(1,8):
        v.get_label_by_id(int2bin(i)).set_text(data[i-1])
plt.show()
plt.close()