import shutil
import os
# 将\呼吸道疾病\肺泡灌洗液\fungi\1.csv和\呼吸道疾病\肺组织\2.csv等  调整为\呼吸道疾病\fungi\1/2.csv
# 适用于将下一级目录上移一层

pathogen_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理02版' 
out_path = r'C:\Users\邓秋洋\Desktop\jieyang_sheet\提取接样表样品类型编号02版\采样部位整理03版'

def obtain_file_dict(pathogen_path, out_path):
    all_file = {}
    for organ_path in [os.path.join(pathogen_path, i) for i in os.listdir(pathogen_path)]:
        # for pathogen in [os.path.join(out_path, i) for i in os.listdir(out_path)]:
        if not os.path.exists(os.path.join(out_path, os.path.basename(organ_path))): #在输出目录建立‘bac’和‘fungi’等目录
            os.makedirs(os.path.join(out_path, os.path.basename(organ_path)))
        for sub_organ_path in [os.path.join(organ_path, i) for i in os.listdir(organ_path)]:
            for bvfg_path in  [os.path.join(sub_organ_path, i) for i in os.listdir(sub_organ_path)]:
                all_file[(os.path.basename(organ_path), os.path.basename(sub_organ_path) , os.path.basename(bvfg_path))] = [os.path.join(bvfg_path, i) for i in os.listdir(bvfg_path)]
    for k, v in all_file.items():
        organ, sub_organ , bvfg = k
        if not os.path.exists(os.path.join(out_path, organ, bvfg)):
            os.makedirs(os.path.join(out_path, organ, bvfg))
        for bvfg_file in v:
            shutil.copy(bvfg_file, os.path.join(out_path, organ, bvfg))

if __name__ == '__main__':
    obtain_file_dict(pathogen_path, out_path)