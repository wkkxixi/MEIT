from rivuletpy.utils.io import *
import numpy as np
import glob
count=0
container=np.zeros(shape=(1,7))
for swc in glob.glob(os.path.join("/home/vv/Desktop/new/1_80_70", '*.swc')):
    a=loadswc(swc)
    tswc = a.copy()
    tswc[:, 0] += count  # change the order
    tswc[:, -1] += count
    count = a.shape[0] + count+3
    saveswc(swc.split('.')[0]+'copy.swc',tswc)
    print(swc,tswc[0, 0],tswc[0,-1])
    print(swc,tswc[-1,0],tswc[-1,-1])
    if container[0,2]==0:
        container=tswc
    else:
        container=np.vstack((container,tswc))
saveswc("/home/vv/Desktop/new/1_80_70/abc.swc",container)
