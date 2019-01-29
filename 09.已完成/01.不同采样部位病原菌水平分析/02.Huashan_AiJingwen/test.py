def deal_a_file(new_path,fl):
    import os
    o=open(os.path.join(new_path,'new.{}'.format(os.path.split(fl)[1])),'wb')
    flag = True
    sep = b'\t'
    lines = open(fl,'rb').readlines()
    header,inf='None',0
    for index,line in enumerate(lines):
        cols = line.split(sep)
        # print(cols)
        if flag:
            if len(cols)<3:
                sep=b','
                cols = line.split(sep)
                if len(cols)<3:
                    sep = b' '
                    cols  = line.split(sep)
                    if len(cols)<3:
                        print(fl)
                        break
                flag =False
            else:
                flag=False
        if cols[0]==b'#Sample':
            header = line
            inf =index
            break
    if header != 'None':
        del lines[inf]
        lines=[header] + lines
        o.write(b''.join(lines))
    else:
        print(lines)

        print('{} no header'.format(fl))

import os
for i in open('weild.sh').readlines():
    fl = i.split(' ')[1].split('|')[0]
    # print(fl)
    deal_a_file(os.getcwd(),fl)

