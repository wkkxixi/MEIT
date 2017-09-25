from rivuletpy.utils.metrics import *
from rivuletpy.utils.io import *
from os.path import join
from rivuletpy.swc import *

datapath='/home/rong/Desktop/Gold166-JSON/test/'
swc1=loadswc(datapath+'2.swc')
swc2=loadswc(datapath+'2_100_100.swc')

prf, swc_compare = precision_recall(swc1, swc2)
print('Precision: %.2f\tRecall: %.2f\tF1: %.2f\t' % prf)
saveswc(datapath+'2_gao_compare.swc',swc_compare)

# M1, M2 = gaussian_distance(swc1, swc2, 3.0)
# print('M1 MEAN: %.2f\tM2 MEAN: %.2f' % (M1.mean(), M2.mean()))

# midx1, midx2 = connectivity_distance(swc1, swc2)
# for i in midx1:
#     swc1[i, 1] = 2
#     swc1[i, 5] = 4
#
# saveswc(join(datapath, 'test.connect1.swc'), swc1)
# for i in midx2:
#     swc2[i, 1] = 2
#     swc2[i, 5] = 4
# saveswc(join(datapath, 'test.connect2.swc'), swc2)
