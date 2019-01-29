for line in open('wield_file_list.txt').readlines():
    line = line.rstrip()
    o =open('{}'.format(''.join(line.split('anno.'))),'wb')
    f = open(line,'rb')
    for i in f.readlines():
        if len(i.split(b'\t'))>16:
            i = i.split(b'\t')[:14]+[i.split(b'\t')[15]+b'\n']
            i =b'\t'.join(i)
        o.write(i)
    f.close()
    o.close()
