from rivuletpy.utils.metrics import *
from rivuletpy.utils.io import *
from os.path import join
import csv
from glob import glob
content='Precision\tRecall\tF1'
datapath = '/home/rong/Documents/Gold166-JSON/'
list=glob(datapath+"*/")
for folder in list:
    for l in os.listdir(folder):
        if l.split(".")[-1]=='swc':
            if len(l.split("."))==2:
                if '_' not in l:
                    swc1 = loadswc(join(folder, l))
                    swc2 = loadswc(join(folder, l.split('.')[-2]+'_100_100.swc'))
                    precision_recall(swc1,swc2)
                    prf, swc_compare = precision_recall(swc1, swc2)
                    content=content+'\n%.2f\t%.2f\t%.2f' % prf
lines=content.split('\n')

with open( datapath+'gao_compare.csv', "w") as csv_file:
    writer = csv.writer(csv_file)
    for line in lines:
        writer.writerow([line])
# print('Precision: %.2f\tRecall: %.2f\tF1: %.2f\t' % prf)

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