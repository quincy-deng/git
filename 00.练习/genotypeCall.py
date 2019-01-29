import argparse
import re
def sum_allposition(readysam): #produce all position frequency
    SAM = open(readysam,'rb')
    q=0
    SEQ ={}
    while True:
        line = SAM.readline().strip()
        line=line.decode('GBK')
        if re.match('^@',line): #why not '''continue if re.match('^@',line)'''
            continue
        if not line:
            break
        (start,seq) = [line.split()[x] for x in [3, 9]]
        q += 1
        z = []
        for i in range(len(seq)):
            z.append(int(start)+i) #all position number
        seq_list = list(zip(z,seq))
        for i in seq_list:
            #print(i)
            SEQ[i] = SEQ.get(i,0) + 1
    #print(SEQ)
    return SEQ
def compare_ref(readysam,ref):
    all_pos = sum_allposition(readysam)
    REF = open(ref,'r')
    pos_ref = REF.readlines()
    for x,y in all_pos:
        pos = x % 10000
        pos_line = int(x/10000)+1
        max_bp = 0
        base=pos_ref[pos_line].split()[3].split('-')[pos]
        print(base)
readysam = '/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/03.vscode/M1.filter.sam'
ref = '/hwfssz1/ST_HEALTH/Population_Genomics/User/dengqiuyang/03.vscode/chrM.pos'
compare_ref(readysam,ref)
