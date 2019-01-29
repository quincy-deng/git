#!/usr/bin/env python
#coding: utf8

import sys,os
import glob
import time
import re
import gzip
import datetime
from collections import defaultdict
from multiprocessing import Pool
try:
    from string import maketrans
except:
    pass
###### Document Decription
'''
    This script is designed for spliting barcode for fq file. It applys to SE and PE mode
'''

###### version & date
prog_version = '0.1.0'
prog_date = '2017.10.24'

###### Usage
usage = '''

     Version %s  by Dongyang-Xu  %s

     Usage: %s <fastqDir> <barcodeFile> <outDir>
''' % (prog_version, prog_date, os.path.basename(sys.argv[0]))

try:
    TransTable = maketrans('ACGT', 'TGCA')
except:
    TransTable = str.maketrans('ACGT', 'TGCA')

class splitBarcodePE(object):
    ''' 
        split barcode for PE data, default mismatch number is 1
        need to reverse barcode during making barcode dict
    '''
    def __init__(self, fq1, fq2, barcodeFile, outDir, prefix, misNum=1, pos=None):
        self.fq1 = fq1
        self.fq2 = fq2
        self.barcodeFile = barcodeFile
        self.outDir = outDir
        self.prefix = prefix
        self.misNum = int(misNum)
        self.pos = pos
        self.sedLen = 10
        self.readsNum = 0
        self.idxs = []
        self.seqSlice = []
        self.statDict = defaultdict(int)
        self.barDict = self.createBarcodeDict()
        self.fhDict = self.createFileHandsDict()

    def createFileHandsDict(self):
        ''' file hand dict for pe fq'''
        if not os.path.exists(self.outDir):
            os.system('mkdir -p %s' % self.outDir)
        ## init barcode file hands
        fhDict = {'r1':{}, 'r2':{}}
        for k in self.barDict:
            fq1 = os.path.join(self.outDir, '%s_%d_1.fq' % (self.prefix, k))
            fq2 = os.path.join(self.outDir, '%s_%d_2.fq' % (self.prefix, k))
            fhDict['r1'][k] = open(fq1, 'w+')
            fhDict['r2'][k] = open(fq2, 'w+')
        ## add unmap fq 
        fhDict['r1']['unmap'] = open(os.path.join(self.outDir, '%s_unmap_1.fq' % self.prefix), 'w+')
        fhDict['r2']['unmap'] = open(os.path.join(self.outDir, '%s_unmap_2.fq' % self.prefix), 'w+')
        return fhDict

    def createBarcodeDict(self):
        ''' create barcode dict according to given mismatch number, must do recverse compliment first'''
        barDict = {}
        ## get raw barcode dict first
        if not os.path.exists(self.barcodeFile):
            print ('There not exists barcode file: %s' % self.barcodeFile)
            sys.exit(1)
        for line in open(self.barcodeFile, 'rb'):
            line = line.strip().split()
            if not line:
                continue
            barId = int(re.findall(r"\d+\.?\d*",line[0])[0])
            barDict[barId] = self.getMisDict(line[1])
            self.sedLen = len(line[1])
        ## get valid barcode dict
        validDict = self.getValidDict(barDict)
        print ('one barcode hash number %d' % len(validDict[validDict.keys()[0]]))
        return validDict

    def getMisDict(self, sed):
        sed = sed[::-1].translate(TransTable)  ##do recverse compliment
        seqDict = {}
        baseList = ('A', 'C', 'G', 'T', 'N')
        if self.misNum == 0:
            seqDict[sed] = 1
            return seqDict
        seeds = set([sed])
        for i in range(self.misNum):
            seeds = self.getSeedsSet(seeds)
        for k in seeds:
            seqDict[k] = 1
        return seqDict

    def getSeedsSet(self, seeds):
        sets = ('A', 'C', 'G', 'T', 'N')
        for k in list(seeds):
            for j in range(len(k)):
                for i in sets:
                    temp = list(k)
                    temp[j] = i
                    seeds.add(''.join(temp))
        return seeds



    def splitBarcode(self):
        t1 = time.time()
        fh1 = gzip.open(self.fq1, 'rb')
        fh2 = gzip.open(self.fq2, 'rb')
        while True:
            rec1 = [fh1.readline() for i in range(4)]
            rec2 = [fh2.readline() for i in range(4)]
            if not rec1[0]:
                break
            self.readsNum += 1
            seq = rec2[1][self.seqSlice[0]:self.seqSlice[1]] + '\n'
            qua = rec2[3][self.seqSlice[0]:self.seqSlice[1]] + '\n'
            seed = rec2[1][self.idxs[0]:self.idxs[1]]
            flag = 0
            for k in self.barDict:
                if seed in self.barDict[k]:
                    #self.fhDict[k].write(''.join([rec[0], seq, rec[2], qua]))
                    flag = 1
                    self.fhDict['r1'][k].write(''.join(rec1))
                    self.fhDict['r2'][k].write(''.join([rec2[0], seq, rec2[2], qua]))
                    self.statDict[k] += 1
                    break
            ## if not match any barcode write into unmap
            if not flag:
                self.fhDict['r1']['unmap'].write(''.join(rec1))
                self.fhDict['r2']['unmap'].write(''.join([rec2[0], seq, rec2[2], qua]))
        fh1.close()
        fh2.close()
        for k in self.fhDict:
            for j in self.fhDict[k]:
                self.fhDict[k][j].close()

def gzipFq(fq):
    os.system('gzip %s' % fq)
    return 0

def runMutiProcess(outDir):
    t1 = time.time()
    fqs = glob.glob(os.path.join(outDir, '*.fq'))
    if len(fqs) < 30:
        p = Pool(len(fqs))
    else:
        p = Pool(30)
    for k in fqs:
        p.apply_async(gzipFq, args=(k,))
    p.close()
    p.join()
    t2 = time.time()
    return 0

def main():
    ######################### Phrase parameters #########################
    import argparse
    (fastqDir, barcodeFile, outDir) = args
    ############################# Main Body #############################
    fqs = sorted(glob.glob(os.path.join(fastqDir, '*.fq.gz')))
    prefix = '_'.join(os.path.basename(fqs[0]).split('_')[:2])
    if not para.PE:
        sb = splitBarcodeSE(fqs[0], barcodeFile, outDir, prefix, para.errNum, para.firstCycle)
        sb.splitBarcode()
    else:
        if len(fqs) != 2:
            print ('There not exists PE fastq !')
            sys.exit(1)
        sb = splitBarcodePE(fqs[0], fqs[1], barcodeFile, outDir, prefix, para.errNum, para.firstCycle)
        sb.splitBarcode()
    ## run muti process to gzip fqs
    runMutiProcess(outDir)

    endTime = datetime.datetime.now()
    print ('End Time: %s\n' % endTime.strftime("%Y-%m-%d %H:%M:%S"))
    print ('Totally spend time %s\n' % (endTime - startTime))

if __name__ == "__main__":
    main()