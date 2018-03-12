'''
a = 1
b = 2
with open('output.txt','w') as f:
    print('new txt file')
    f.write(str(a+b))
'''
'''
import numpy as np 

a = np.ones((3,2,2))
# print(str(a))
b = np.zeros((3,2,2))
# print(str(b))
c = np.append(a,b,axis=1)
# a = np.vstack((a, b))  
print(str(c))
'''

import numpy as np
import os
import fnmatch
import multiprocessing as mp
import shutil
import h5py

def loadtiff3d(filepath):
    """Load a tiff file into 3D numpy array"""
    # from libtiff import TIFF
    # tiff = TIFF.open(filepath, mode='r')

    import tifffile as tiff
    a = tiff.imread(filepath)

    stack = []
    for sample in a:
        stack.append(np.rot90(np.fliplr(np.flipud(sample))))
    out = np.dstack(stack)
    #a.close()

    return out
def sober(folder):
    crop_y = os.listdir(folder)
    log_path = folder  +'/combining_log.txt'
    final_img = None
    with open(log_path, 'w') as f:
        f.write('The combining process of ' + folder + ':\n')
        for y in crop_y:
            if len(y) != 18:
                continue
            tmp = loadtiff3d(folder + y)
            if final_img is None:
                final_img = tmp
            else:
                final_img = np.append(tmp, final_img, axis=1)
        f.write('Final image shape is: ' + str(final_img.shape) + '\n')
        f.write('----- Combine successfully -----\n')
        
    h5f = h5py.File(folder +  '/test_hdf5.h5', 'w')
    h5f.create_dataset('dataset_1', data=final_img)
    h5f.close()

sober('/Users/wonh/Desktop/test/')