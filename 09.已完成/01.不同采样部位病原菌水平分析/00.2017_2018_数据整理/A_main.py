import grab_jieyang_file # 01 寻找原始路径下包含‘接样’接样表，拷贝到jieyang_sheet目录；1,os.walk;2,shutil.copy;3,re.search
import extract_jieyang_csv # 02 读取所有的接样表，提取样品编号和类型内容到csv文件；1,pandas.read_excel;data.loc;data.cloumns
import combine_jieyang_csv # 03 将所有的接样csv文件合并到一个文件
import grab_data_csv # 04 根据病原菌关键词提取文件到各个目录
import split_data_bypoint # 05 根据取样部位分别归类data文件
import extract_data_csv # 06 处理根据组织归类好的(‘肠道感染\腹膜透析液\bac\18S4339681.bac.anno.xls’)原始文件，提取出目的数据，整合到如‘肠道感染’类别下所有bac归到一起（肠道感染\bac.txt）
import compute_confidence_interal # 07 计算各组织病原菌的置信区间
import combine_pathogenOrgan_file # 08 所有的bac（或者fungi）文件分别根据组织（如血流感染bac.txt，脑部感染bac.txt...）合并成一个文件，没有的细菌种类标记为['-','-']。
import rank_sum_test # 09 秩和检验两个组织之间是否存在不同病原菌的显著性差异

dir_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet' # 非原始路径，勿用


grab_jieyang_file.main(dir_path)