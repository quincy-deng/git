# library and dataset
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = sns.load_dataset('tips')
 
path = r'D:\华山医院\result\01.阳性和阴性结果统计,画箱线图'
os.chdir(path)

for boot,dirs,files in os.walk(path):
    for fl in files:
        try:
            if fl.split('.')[0].split('_')[1]=='cutoff2':
                os.chdir(boot)
                df = pd.read_table(fl,engine='python',encoding='gbk')
                
                sns.set_style("whitegrid")
                # sns.set()
                # Grouped boxplot
                plt.rcParams['font.sans-serif'] = ['FangSong']
                sns.boxplot(y="log10(SDSMRN)", 
                x="species", 
                hue="P|N",
                data=df, 
                palette="Set2",
                flierprops = {'marker':'o','markerfacecolor':'white','color':'black'}).set_title('Multiple Species with SDSMRN in {}'.format(fl.split('_')[0]))
                # 设置异常值属性，点的形状、填充色和边框色
                
                # Change the appearance of that box
                plt.tight_layout()
                plt.legend(loc = 'best')
                plt.xticks(rotation=90)
                # plt.show()
                os.chdir(r'D:\华山医院\result\01.阳性和阴性结果统计,画箱线图')
                plt.savefig('{}_boxplot.png'.format(fl.split('_')[0]),dpi=600)
                plt.close()

        except:
            pass 
