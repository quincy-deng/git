import os
class Flush_data(object):
    def __init__(self,path,header_file):
        self.file_ext = {'xls':b'\t','csv':b','}
        self.path = path
        self.f =open(header_file)
        self.sep=None
        self.fl_content = None
        self.header = None
        self.flag = None
        self.fl = None
    
    # Custom header
    def Header(self):
        for line in self.f.readlines():
            yield line.rstrip().split('\t')

    def check_header_exist(self):
        self.header = 0
        for line in self.fl_content:
            if line.split(self.sep)[0] != b'#Sample':
                continue
            self.header = line
    
    # File missing header,add header based on content length
    def Add_header(self):
        self.flag =1
        header = list(self.Header())
        header_len = [len(i) for i in header]
        try:
            self.header = header(header_len.index(len(fl_content[0].split(self.sep))))
            self.Export_file()
        except:
            print('empty file{}'.format(self.fl))
            self.flag=0

    def Export_file(self):
        sampleid,ptg_type = self.fl.split('.')[0][:10],self.fl.split('.')[1]
        o = open('{}_{}.{}'.format(sampleid,ptg_type,self.fl.split('.')[-1]),'wb')
        o.write(self.header)
        for i in self.fl_content:
            o.write(i)
   
    def Main(self):
        for boot,dirs,files in os.walk(self.path):
            for self.fl in files:
                os.chdir(boot)
                f = open(self.fl,'rb')
                self.sep = self.file_ext[self.fl.split('.')[-1]]
                self.fl_content = f.readlines()
                self.check_header_exist()
                if self.header !=0:
                    self.fl_content.remove(self.header)
                else:
                    self.Add_header()
                    if self.flag ==0:
                        f.close()
                        os.remove(self.fl)
                        continue
                self.Export_file()
                f.close()
                os.remove(self.fl)
                            
        print("END")

path = r'D:\华山医院\华山医院整理数据'  
header_file = r'F:\huashan_header.txt'               
test1 = Flush_data(path,header_file)
test1.Main()