import os
import re

fungi_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi'
fungi_vector_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版\fungi不同组织vector'


def compute_pathogen_positive_rate(SDSMRN, cutoff, sample_sumNumber):
    positive_number = 0
    # print(cutoff,'ssssllllllllllllllllllllllllllllll')
    for i in SDSMRN:
        if int(i) > cutoff:
            positive_number += 1
    positive_number_rate = '%.2f%%' % ((positive_number / sample_sumNumber) *100)
    return positive_number_rate

def output_pathogen_positive_rate(pathogen_rate, fungi_path):
    output_pathogen_results = open(fungi_path + 'pathogen_positive_detext_rate.txt', 'w')
    output_pathogen_results.write(format(format('species','<20'),'<40'))
    for i in [format(str(i),'<10') for i in range(20)]:
        output_pathogen_results.write(i)
    output_pathogen_results.write('\n')
    output_pathogen_results.write('\n')
    for k in sorted(pathogen_rate.keys()):
        organ_name,pog_number,pog =k
        output_pathogen_results.write('{:<50}'.format(organ_name + '_' + str(pog_number) + '_'+ pog))
        [output_pathogen_results.write('{:<10}'.format(str(i)+'\t')) for i in pathogen_rate[k]]
        output_pathogen_results.write('\n')

def pathogen_positive_rate(fungi_path,fungi_vector_path):
    pathogen_rate = {}
    
    for organ_file in [os.path.join(fungi_path, i) for i in os.listdir(fungi_path)]:
        f = open(organ_file, 'r')
        file_line = f.readlines()
        f.close()
        organ_name = os.path.basename(organ_file).split('.txt')[0]
        for n in [os.path.join(fungi_vector_path, i) for i in os.listdir(fungi_vector_path)]:
            if re.search(organ_name, n):
                # print(i)
                sample_sumNumber = len(open(n,'r').readline().rstrip().split())-1
                # print(sample_sumNumber)
        if not sample_sumNumber:
            exit()        
        for pathogen_SDSMRN in file_line:
            pathogen, SDSMRN = pathogen_SDSMRN.rstrip().split('\t')[0], pathogen_SDSMRN.rstrip().split('\t')[1:]
            if sum([int(c) for c in SDSMRN]) == 0:
                continue
            for i in range(20):
                pathogen_rate.setdefault((organ_name, sample_sumNumber, pathogen),[]).append(compute_pathogen_positive_rate(SDSMRN, i, sample_sumNumber))
    output_pathogen_positive_rate(pathogen_rate,fungi_path)

def obtian_sampleSDSMRN_max(organ_file):
    f = open(organ_file, 'r')
    pog_lines = f.readlines()
    pog_list = []
    f.close()
    [pog_list.append(pog_line.rstrip().split()[1:]) for pog_line in pog_lines]
    sample_list = map(list, zip(*pog_list))
    max_list = [max(i) for i in sample_list]
    return max_list

def compute_organ_detect_rate(max_list, cutoff):
    n = 0
    for i in max_list:
        if int(i) >cutoff:
            n += 1
    return '%.2f%%' % ((n / len(max_list)) * 100)

def output_organ_detect_rate(organ_rate_dict, fungi_path):
    out_organ_reults = open(fungi_path + 'organ_positive_detect_rate.txt','a+')
    out_organ_reults.write(format('','<25'))
    for i in [format(str(i),'<10') for i in range(20)]:
        out_organ_reults.write(i)
    out_organ_reults.write('\n')
    out_organ_reults.write('\n')
    for k,v in organ_rate_dict.items():
        organ_name, lengs = k
        out_organ_reults.write('{0:{1}<5}'.format(organ_name,chr(12288)) + '\t' + '{:<5}'.format(str(lengs)))
        out_organ_reults.write(format('','<5'))
        for i in v:
            out_organ_reults.write(format(str(i),'<10'))
        out_organ_reults.write('\n')
    out_organ_reults.close()

def organ_detect_rate(fungi_vector_path):
    organ_rate_dict ={}
    for organ_file in [os.path.join(fungi_vector_path, i) for i in os.listdir(fungi_vector_path)]:
        sampleSDSMRN_max= obtian_sampleSDSMRN_max(organ_file)
        lengs = len(sampleSDSMRN_max)
        for i in range(20):
            organ_rate_dict.setdefault((os.path.basename(organ_file).split('vector.txt')[0], lengs), []).append(compute_organ_detect_rate(sampleSDSMRN_max,i))
    output_organ_detect_rate(organ_rate_dict,fungi_path)


def main(fungi_path, fungi_vector_path):
    organ_detect_rate(fungi_vector_path) # 不同类型样本的真菌阳性检出率（需要设定不同梯度cutoff值，1-20）
    # pathogen_positive_rate(fungi_path,fungi_vector_path) # 不同类型下的不同菌株的检出率（需要设定不同梯度cutoff值，1-20）

if __name__ == '__main__':
    main(fungi_path,fungi_vector_path)