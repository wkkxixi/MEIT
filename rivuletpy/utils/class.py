from rivuletpy.utils.io import *
from rivuletpy.trace import *
import numpy as np
import os, math
# inputpath="/home/vv/Desktop/new/1"


class getinfo:
    def __init__(self,name,thresholdt,pctg,bi_matrix=None,thresholdbi=None,swc=None):
        self.name=name
        self.cropx=int(name.split("_")[-2])
        self.cropy=int(name.split("_")[-1])
        self.matrix_3d=None
        self.pctg=pctg
        self.bi_ratio=0
        self.bi_matrix=None
        self.threshodbi=0
        self.thresholdt=thresholdt
        self.tracelabel=False
        self.swc = None
    def get3d_mat(self):
        self.matrix_3d=loadimg('/home/vv/Desktop/new/1_100_90/'+self.name+'.tif')
        return self.matrix_3d
    def cellsatisfied(self):
        oneitem=loadimg('/home/vv/Desktop/new/1_100_90/'+self.name+'.tif')
        self.bi_matrix=(oneitem>self.thresholdt).astype(int)
        self.bi_ratio=float((oneitem > self.thresholdt).sum()/(oneitem.shape[0]*oneitem.shape[1]*oneitem.shape[2]))
        return self.thresholdt, self.bi_matrix, self.bi_ratio
    def traceornot(self):
        if self.bi_ratio>self.pctg:
            self.tracelabel=True
        return self.tracelabel
    def gettrace(self):
        if self.tracelabel:
            # Run rivulet2 for the first time
            tracer = R2Tracer()
            self.swc, soma = tracer.trace(self.matrix_3d, self.thresholdt)

            tswc=self.swc._data.copy()
            # print(self.swc._data.shape)
            x=int(self.name.split("_")[1])-1
            y=int(self.name.split("_")[0])-1
            tswc[:, 2] += 100*x  #以2_3举例，横坐标加上cropx×截取的y-1（3），纵坐标加上cropy×截取的x-1(2）
            tswc[:, 3] +=90*y
            saveswc('/home/vv/Desktop/new/1_100_90/'+self.name+'.swc', tswc)
            # self.swc._data = tswc
            # self.swc.save('/home/vv/Desktop/new/1_100_90/'+self.name+'.swc')
        else:
            tswc=None
        return tswc




file=open('/home/vv/Desktop/new/1_100_90/txt/100_90.txt','r')
for line in file:
    if "_" in line:
        line=line.split('\n')[0]

        line = getinfo(line,10,0.000000005)
        print(line.get3d_mat())
        print(line.cellsatisfied())
        print(line.traceornot())
        print(line.pctg,line.bi_ratio)
        print(line.gettrace())

