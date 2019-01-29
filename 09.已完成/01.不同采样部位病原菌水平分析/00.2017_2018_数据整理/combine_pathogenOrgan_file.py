import os


# 所有的bac（或者fungi）文件分别根据组织（如血流感染bac.txt，脑部感染bac.txt...）合并成一个文件，没有的细菌种类标记为['-','-']。
def combine_pathogen_file(pathgen_organ_path, out_path):
    # bac_dict, virus_dict, fungi_dict, parasite_dict = [{} for i in range(4)] # 谨记教训
    # dict_list = {'bac':bac_dict, 'virus':virus_dict, 'fungi':fungi_dict, 'parasite':parasite_dict}
    for pathogen in [os.path.join(pathgen_organ_path, i) for i in
                     os.listdir(pathgen_organ_path)]:  # 创建字典例如{‘bac’：bac_dict}
        jianchu_bili = []
        pathogen_name = os.path.basename(pathogen)
        specieses = set([])
        dict_save = {}
        organ_name = [os.path.basename(pathogen)]
        jianchu = []
        for pathgenOrgan_file in [os.path.join(pathogen, i) for i in
                                  os.listdir(pathogen)]:
            organ_name.append(
                os.path.basename(os.path.splitext(pathgenOrgan_file)[0]).split(
                    pathogen_name)[0])
            f = open(pathgenOrgan_file, 'r')
            n = 0
            for i in f.readlines():
                n += 1
                species = i.rstrip().split('\t')[0].split(':')[0]
                specieses.add(species)
            jianchu.append(n)
        f.close()
        sum_sp = len(specieses)
        for pathgenOrgan_file in [os.path.join(pathogen, i) for i in
                                  os.listdir(pathogen)]:
            save_species = {}
            f = open(pathgenOrgan_file, 'r')
            for line in f.readlines():
                species = line.rstrip().split('\t')[0].split(':')[0]
                float_list = []
                float_list.append(float(line.rstrip().split('\t')[1]))
                float_list.append(float(line.rstrip().split('\t')[2]))
                new_list = []
                for i in float_list:
                    new_list.append(round(i, 2))
                save_species[species] = new_list

            for species in specieses:
                if species in save_species.keys():
                    dict_save.setdefault(species, []).append(
                        save_species[species])
                else:
                    dict_save.setdefault(species, []).append(['-', '-'])
        f.close()
        for i in jianchu:
            jianchu_bili.append(round(i / sum_sp, 2))
        organ_number = [947, 1406, 29, 54, 20, 74, 1707, 1946]
        jianchu_dict = {jianchu_bili[i]: organ_number[i] for i in
                        range(len(jianchu_bili))}
        zhenshi = []
        for k, v in jianchu_dict.items():
            zhenshi.append(round(k * 100 / v, 2))
        o = open(os.path.join(out_path, pathogen_name + '.txt'), 'w')
        o.write(format(organ_name[0], '<40'))
        for i in organ_name[1:]:
            o.write(format(i, '<20'))
        o.write('\n')
        o.write(format('样本总数', '<40'))
        for i in organ_number:
            o.write(format(i, '<20'))
        o.write('\n')
        o.write(format('检出率', '<40'))
        for i in jianchu_bili:
            o.write(format(i, '<20'))
        o.write('\n')
        o.write(format('均一化检出率', '<40'))
        for i in zhenshi:
            o.write(format(i, '<20'))
        o.write('\n')
        for k, v in dict_save.items():
            o.write(format(k, '<40'))
            for i in v:
                o.write(format(str(i), '<20'))
            o.write('\n')

        # exit()


pathgen_organ_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData\病原数据整理'
out_path = r'C:\Users\邓秋洋\Desktop\07.analysis_bypogenData'


def main():
    combine_pathogen_file(pathgen_organ_path, out_path)


if __name__ == '__main__':
    main()
