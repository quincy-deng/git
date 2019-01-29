import numpy as np
import scipy.stats as st
import os
from compute_confidence_interal import filter_phogen

data_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据按照组织归类SDSMRN版'
outdata_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\秩和检验-组织SDSMRN版'


def test_two_file(organ1, organ2):
    rank_dict = {}
    for pathogen in organ1.keys():
        if pathogen in organ2.keys():
            a, b = st.ranksums(organ1[pathogen], organ2[pathogen])
            a = format(a, '.2f')  #
            b = '%.2e' % b  # 科学记数法 '%e'%number
            rank_dict[pathogen] = format(str(a), '<5') + ',' + format(str(b),
                                                                      '<10')
            # scipy.stats.ranksums(x, y) (4.415880433163923, 1.0059968254463979e-05)
    return rank_dict


# pathogens_dict = {}
def main():
    for pathogen_path in [os.path.join(data_path, i) for i in
                          os.listdir(data_path)]:
        pathogens_key = os.path.basename(pathogen_path)
        pathogen_dict = {}
        os.chdir(outdata_path)
        rank_dict = {}
        specieses = set([])
        # print(pathogen_path)
        if not os.path.exists(pathogens_key):
            os.makedirs(pathogens_key)
        for pathogen in [os.path.join(pathogen_path, i) for i in
                         os.listdir(pathogen_path)]:
            filter_dict = filter_phogen(pathogen)
            pathogen_dict[
                (os.path.basename(pathogen)).split('.txt')[0]] = filter_dict
        organ_list = list(pathogen_dict.keys())
        for i in range(len(organ_list) - 1):
            compare_dict = organ_list.pop()
            for new_organ_name in organ_list:
                compare_two_organ = compare_dict + '_' + new_organ_name
                rank_dict[compare_two_organ] = test_two_file(
                    pathogen_dict[compare_dict], pathogen_dict[new_organ_name])
        for i in rank_dict.keys():
            for i in rank_dict[i].keys():
                specieses.add(i)
        dict_save = {}
        for species in specieses:
            for compare_two_organ in sorted(rank_dict.keys()):
                if species in rank_dict[compare_two_organ].keys():
                    dict_save.setdefault(species, []).append(
                        rank_dict[compare_two_organ][species])
                else:
                    dict_save.setdefault(species, []).append('-,-')
        f = open(os.path.join(outdata_path, pathogens_key + '.txt'), 'w')
        f.write(format('species', '<40'))
        for species in rank_dict.keys():
            f.write('\t' + format(species, '<45'))
        f.write('\n')
        for k, v in dict_save.items():
            f.write(format(bytes.decode(k), '<40'))
            for pvalue in v:
                f.write('\t' + format(str(pvalue), '<45'))
            f.write('\n')


if __name__ == '__main__':
    main()
    # organs_dict[os.path.basename(organ_path)] ={}
    # for pathogen_file in [os.path.join(organ_path, i) for i in os.listdir(organ_path)]:
    #     filter_dict = filter_phogen(pathogen_file)
    #     organs_dict[os.path.basename(organ_path)][os.path.basename(pathogen_file)]={}
    #     for pathogen,SDSMRN in filter_dict.items():
    #         organs_dict[os.path.basename(organ_path)][os.path.basename(pathogen_file)][pathogen] = SDSMRN

# pathogens_dict = {}
# for organ in organs_dict.keys():
#     print(organ)
#     for pathogen_file in organs_dict[organ].keys():
#         print(pathogen_file)
#         for pathogen in organs_dict[organ][pathogen_file].keys():
#             print(pathogen)
#             pathogens_dict[pathogen_file][organ][pathogen] = organs_dict[organ][pathogen_file][pathogen]      

# for pathogen in pathogens_dict:
#     print(pathogen)
#     for organ in pathogens_dict[pathogen]:
#         print(organ)
