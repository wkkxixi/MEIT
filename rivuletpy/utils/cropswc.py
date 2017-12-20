from rivuletpy.utils.io import *
from rivuletpy.trace import *
import numpy as np
import os, math



# This class is used to transform small tif into swc.


class getinfo:
    # when using this class, we define the name as filename.
    # thresholdt as the permitted standard of value in np element.
    # pctg as the percentage standard of whether a image should be traced or not
    def __init__(self,dir, name, thresholdt, pctg):
        self.folder=dir+'/'
        self.name = name
        self.cropx = int(dir.split("_")[-2])
        self.cropy = int(dir.split("_")[-1])
        self.matrix_3d = None
        self.pctg = pctg
        self.bi_ratio = 0
        self.bi_matrix = None
        self.threshodbi = 0
        self.thresholdt = thresholdt
        self.tracelabel = False
        self.swc = None

    def get3d_mat(self):
        self.matrix_3d = loadimg(self.folder + self.name + '.tif')
        return self.matrix_3d

    def tsatisfied(self):  # check every element in np meeting the standard of thresholdt or not
        oneitem = loadimg(self.folder + self.name + '.tif')
        self.bi_matrix = (oneitem > self.thresholdt).astype(
            int)  # get all the satisfied np value as 1, unsatisfied as 0
        # bi_ratio is the ratio of number of the item value 1  /The number of the whole np elements
        self.bi_ratio = float(
            (oneitem > self.thresholdt).sum() / (oneitem.shape[0] * oneitem.shape[1] * oneitem.shape[2]))
        return self.thresholdt, self.bi_matrix, self.bi_ratio

    def traceornot(self):
        if self.bi_ratio > self.pctg:
            self.tracelabel = True
        return self.tracelabel

    def gettrace(self, predefined_soma):
        if self.tracelabel:
            # Run rivulet2 for the first time
            tracer = R2Tracer()
            self.swc, soma = tracer.trace(
                self.matrix_3d, self.thresholdt, predefined_soma)
            tswc = self.swc._data.copy()
            x = int(self.name.split("_")[1]) - 1
            y = int(self.name.split("_")[0]) - 1
            tswc[:, 2] += self.cropx * x  # 100 is the cropx we define when croping
            tswc[:, 3] += self.cropy * y  # 100 is the cropy we define when croping
            saveswc(self.folder + self.name + '.swc', tswc)
        else:
            tswc = None
        return tswc

    def gettrace_from_tips(self, predefined_soma, order):
        if self.tracelabel:
            # Run rivulet2 for the first time
            tracer = R2Tracer()
            self.swc, soma = tracer.trace(self.matrix_3d, self.thresholdt, predefined_soma)
            tswc = self.swc._data.copy()
            x = int(self.name.split("_")[1]) - 1
            y = int(self.name.split("_")[0]) - 1
            # 100 is the cropx we define when croping
            tswc[:, 2] += self.cropx * x
            # 100 is the cropy we define when croping
            tswc[:, 3] += self.cropy * y
            saveswc(self.folder + self.name + '_' + str(order) + '.swc', tswc)
        else:
            tswc = np.asarray([])
        return tswc, self.name + '_' + str(order) + '.swc'



