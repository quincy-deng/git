# 2018.01.18 
# >> step1 整理ID对应文件路径,存到一个list文件,路径在LD盘01.HuaShan/09.result下<<
def SampleID_correspond_rawdata_FilePath():
    import os
    path='/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/00.rawdata/01.华山医院NGS测序报告'
    fls=(os.path.join(boot,fl) for boot,dirs,files in os.walk(path) for fl in files if not fl.startswith('.') if fl.endswith('xls') or fl.endswith('csv') if len(fl.split('.'))==4 if len(fl.split('.')[0])>9)
    # fls_dict ={(fl.split('.')[0][:10],fl.split('.')[1]):fl for fl in list(fls)}
    fls_dict =dict()
    for fl in fls:
        print(os.path.split(fl)[1].split('.')[0][:10])
        fls_dict.setdefault(os.path.split(fl)[1].split('.')[0][:10],[]).append(fl)
    # print('MARKER')
    f=open('/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/09.result/files_list.xls','w')
    f.write('sampleid\tpathogen\treindex\tfile_pathway\n')
    for sample,fls in fls_dict.items():
        sample_dict = dict()
        for fl in fls:
            sample_dict.setdefault(os.path.split(fl)[1].split('.')[1],[]).append(fl)
        sample_list=[]
        for ptg,fls in sample_dict.items():
            if len(fls)>1:
                fls_size = [os.path.getsize(fl) for fl in fls]
                index = fls_size.index(max(fls_size))
                f.write('\t'.join(['\t'.join([sample,ptg]),'.'.join([sample,ptg]),fls[index]+'\n']))
                continue
            f.write('\t'.join(['\t'.join([sample,ptg]),'.'.join([sample,ptg]),fls[0]+'\n']))
    f.close()
# SampleID_correspond_rawdata_FilePath()

# >> step2 ngs results 整理,去重,去阴性,得到1076个样本<<
def SampleID_NGS_Result():
    import pandas as pd
    import xlrd
    path='/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/08.resultdata/a.华山医院给出NGS结果/12.5重新整理中英文.xlsx'
    sheets = xlrd.open_workbook(path).sheet_names()
    ngs_results=dict()
    for sheet in sheets:
        df =pd.read_excel(path,sheet_name=sheet)
        for index,row in df.iterrows():
            # print(list(row)[4])
            if list(row)[4].find('无')==-1:
                if len(list(row)[0])<10:
                    continue
                ngs_results[list(row)[0][:10]]=list(row)[4]       

    f =open('/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/09.result/NGS_Results.xls','w')
    f.write('sampleid\tngs_results\n')
    print(ngs_results)
    for sampleid,ngs_result in ngs_results.items():
        f.write('\t'.join([sampleid,ngs_result+'\n']))
    f.close()
# >> step3 找到文件header,输出到一个目录 <<

def rule_rawfile():
    '''
    Not found header in 17S0287145.bac.anno.csv
    Not found header in 18S4003050.virus.top10.xls
    Not found header in 18S4003050.parasite.top10.xls
    Not found header in 18S4003050.fungi.top10.xls
    Not found header in 17S0836483_12.fungi.anno.csv
    Not found header in 17S0836483_12.virus.anno.csv
    Not found header in 17S0836483_12.parasite.anno.csv
    Not found header in 17S0836483_12.bac.anno.csv
    '''
    import os
    import pandas as pd
    cols = ['#Sample','Species','Genus','Re_Abu','SDSMRN','SDSMRNG']
    os.chdir('/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/00.rawdata/02.整理ID和header/rawdata')
    for filepath in os.listdir():
        if len(filepath.split('.'))!=4:
            continue
        with open(filepath,'rb') as f:
            header_lines=[(index,line) for index,line in enumerate(f) if line.startswith(b'#Sample')]
            if header_lines:
                header_line,header_bytes =header_lines[0]
            else:
                print(filepath)
                continue
        # print(header_line,filepath)
        if filepath.endswith('csv'):
            headers = [str(i).rstrip("'").lstrip("b'") for i in header_bytes.split(b',')]
            file_df = pd.read_csv(filepath,engine='python',header=None,names=headers)
            file_df =file_df.drop(header_line)
        if filepath.endswith('xls'):
            headers = [str(i).rstrip("'").lstrip("b'") for i in header_bytes.split(b'\t')]
            file_df = pd.read_table(filepath,engine='python',header=None,names=headers)
            file_df =file_df.drop(header_line)
        file_df.to_csv('/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/00.rawdata/02.整理ID和header/RankHeader/{}'.format(os.path.split(filepath)[1]),sep='\t',index=False)
        
# rule_rawfile()

# >> step4
def export_results():   
    import os
    os.chdir('/ldfssz1/ST_HEALTH/Population_Genomics/USER/dengqiuyang/01.HuaShan/09.result')
    # ngs_negative = open('Negative_list.xls','w')
    import pandas as pd
    results=pd.read_table('00.SampleID_correspond_rawdata_FilePath3.20190118',engine='python',index_col='reindex')
    df = pd.read_table('NGS_Results.xls',engine='python')
    for index,row in df.iterrows():
        for i in row[1].split(';'):
            index = '.'.join([row[0],i.split(',')[0]])
            if len(i.split(','))==1:
                print(i)
                index = '.'.join([row[0],'bac'])
            try:
                print(results.loc[index,'file_pathway'])
                data = pd.read_csv(results.loc[index,'file_pathway'],engine='python')
                print(data)
                if i.split(',')[1] not in data['Species']:
                    ngs_negative.write('{}\t{}\n'.format(row[0],i.split(',')[1]))
            except:
                continue
            
# export_results()