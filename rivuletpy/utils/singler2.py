from rivuletpy.utils.io import *
from rivuletpy.soma_r2 import Soma
from rivuletpy.trace_r2 import R2Tracer_r2
import numpy as np
import os

from scipy.ndimage.interpolation import zoom
from rivuletpy.utils.cropswc import *


folder = '/Users/wonh/Desktop/debug/'
filename = '4.tif'
threshold = 9
matrix_3d = loadimg(folder + filename)
bimg = (matrix_3d>threshold).astype('int')
numbers = bimg.ravel()
print(bimg.shape[0]*bimg.shape[1]*bimg.shape[2])
with open('/Users/wonh/Desktop/debug/4.tif.txt', 'w') as f:
    f.write(str(numbers.sum()))
print('img shape: ' + str(matrix_3d.shape))
tracer = R2Tracer_r2()
swc, soma = tracer.trace(matrix_3d, threshold)
tswc = swc._data.copy()
saveswc(folder + filename + '.swc', tswc)

