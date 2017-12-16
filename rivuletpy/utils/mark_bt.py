import os
from rivuletpy.utils.io import *
import fnmatch

folderpath = '/Users/wonh/Gold166-JSON/bad/'
whichsub = 'utokyofly/'
whichtif = '5'
targetfolderpath = folderpath + whichsub + whichtif + '_100_100'



dirs = os.listdir(targetfolderpath)
i = 1
for f in dirs:
    print(str(i) + ': ' + f + ' is passed')
    if fnmatch.fnmatch(f, '*.swc') and not fnmatch.fnmatch(f, '*boundary.swc'):
        print(str(i) + ': ' + f + ' is on processing')
        bt = np.zeros((1, 7))
        tswc = loadswc(targetfolderpath + '/' + f)
        max_set = np.amax(tswc, axis=0)
        min_set = np.amin(tswc, axis=0)
        max_x = max_set[2]
        max_y = max_set[3]
        max_z = max_set[4]
        min_x = min_set[2]
        min_y = min_set[3]
        min_z = min_set[4]
        j = 0
        flag = 0
        while j < tswc.shape[0]:
            if tswc[j, 2] == max_x or tswc[j,2] == min_x or tswc[j, 3] == max_y or tswc[j, 3] == min_y or tswc[j, 4] == max_z or tswc[j,5] == min_z:
                # print('j ' + str(j) + ': boundary')
                tswc[j,1] = 7
                tswc[j,-1] = -1
                tswc[j, -2] = 0.5
                if flag == 0:
                    bt[0, :] = tswc[j, :]
                    print(str(bt))
                    flag = 1
                else:
                    bt = np.vstack((bt, tswc[j,:]))
                    
            j += 1
        saveswc(targetfolderpath + '/tips/' + f.split('.')[0] + '_tips.swc', bt)
    i += 1

