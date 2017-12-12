from rivuletpy.utils.io import *
from rivuletpy.trace import *
import numpy as np
import os
import math


# This class is used to transform small tif into swc.


class getinfo:
    # when using this class, we define the name as filename.
    # thresholdt as the permitted standard of value in np element.
    # pctg as the percentage standard of whether a image should be traced or not
    def __init__(self, dir, name, thresholdt, pctg, sizexyz):
        self.folder = dir
        self.name = name
        self.matrix_3d = None
        self.pctg = pctg
        self.bi_ratio = 0
        self.bi_matrix = None
        self.threshodbi = 0
        self.thresholdt = thresholdt
        self.tracelabel = False
        self.swc = None
        self.shape = sizexyz

    def get3d_mat(self):
        self.matrix_3d = loadimg(self.folder + self.name)
        return self.matrix_3d

    def tsatisfied(self):  # check every element in np meeting the standard of thresholdt or not
        self.bi_matrix = (self.matrix_3d > self.thresholdt).astype(
            int)  # get all the satisfied np value as 1, unsatisfied as 0
        # bi_ratio is the ratio of number of the item value 1  /The number of the whole np elements
        self.bi_ratio = float(
            (self.matrix_3d > self.thresholdt).sum() / self.shape)
        return self.thresholdt, self.bi_matrix, self.bi_ratio

    def traceornot(self):
        if self.bi_ratio > self.pctg:
            self.tracelabel = True
        return self.tracelabel

    def gettrace(self):
        if self.tracelabel:
            # Run rivulet2 for the first time
            print('Run rivulet2 for the first time')
            tracer = R2Tracer()
            self.swc, soma= tracer.trace(self.matrix_3d, self.thresholdt)
            # tswc = self.swc._data.copy()
            # x = int(self.name.split("_")[1]) - 1
            # y = int(self.name.split("_")[0]) - 1
            # # 100 is the cropx we define when croping
            # tswc[:, 2] += self.cropx * x
            # # 100 is the cropy we define when croping
            # tswc[:, 3] += self.cropy * y
            saveswc(self.folder + self.name.split('/')
                    [0] + '/r2/' + self.name.split('/')[1] + '.r2.swc', self.swc)
        else:
            print('fail to run r2')
        return self.swc
