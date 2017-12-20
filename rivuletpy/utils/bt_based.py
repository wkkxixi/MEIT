from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
from rivuletpy.utils.io import *
import fnmatch
import os


def tip_detecting(targetfolderpath, xno, yno, swc_name):
    dirs = os.listdir(targetfolderpath)
    boundary_name = str(yno).split('.')[0] + '_' + str(xno).split('.')[0]
    print('boundary_name: ' + boundary_name)
    for f in dirs:
        if fnmatch.fnmatch(f, boundary_name + '_boundary.swc'):
            boundary_swc = loadswc(targetfolderpath + '/' + f)
            max_set = np.amax(boundary_swc, axis=0)
            min_set = np.amin(boundary_swc, axis=0)
            max_x = max_set[2]
            max_y = max_set[3]
            max_z = max_set[4]
            min_x = min_set[2]
            min_y = min_set[3]
            min_z = min_set[4]
            print('swc_name is : ' + targetfolderpath + '/' + swc_name)
            bt = np.zeros((1, 7))
            for g in dirs:
                if g == swc_name:
                    tswc = loadswc(targetfolderpath + '/' + swc_name)
                    print('loaded!!')
                    j = 0
                    flag = 0
                    print('tswc.shape[0]:' + str(tswc.shape[0]))
                    while j < tswc.shape[0]:
                        if tswc[j, 2] == max_x or tswc[j, 2] == min_x or tswc[j, 3] == max_y or tswc[j, 3] == min_y:
                            if(tswc[j, 1] != 6):
                                j += 1
                                continue
                            # print('found endpoint')
                            tswc[j, 0] = xno
                            tswc[j, 1] = yno
                            if tswc[j, 3] == min_y:
                                tswc[j, -1] = 0
                            elif tswc[j, 3] == max_y:
                                tswc[j, -1] = 1
                            elif tswc[j, 2] == min_x:
                                tswc[j, -1] = 2
                            else:
                                tswc[j, -1] = 3
                            if flag == 0:
                                bt[0, :] = tswc[j, :]
                                flag = 1
                            else:
                                bt = np.vstack((bt, tswc[j, :]))
                        j += 1
                    if flag != 0:
                        print('not empy')
                        if bt is None:
                            print('bt none')
                        else:
                         print('bt not none: ' + str(bt.shape[0]))
                        return bt
                    else:
                        print('return empty')
                        return np.asarray([])
                
            print('no need to trace')
            return np.asarray([])

def tif_tracing(folder, f, next_xno, next_yno, thresholdt, percentage, somainfo, order):
    line = f.split('.')[0]
    line = getinfo(folder, line, thresholdt, percentage)
    line.get3d_mat()
    line.tsatisfied()
    line.traceornot()
    new_swc, swc_name = line.gettrace_from_tips(somainfo, order)
    print('swc_name is : ' + swc_name)
    tips = tip_detecting(folder, next_xno, next_yno, swc_name)
    os.rename(folder + '/' + f,
              folder + '/' + f + '_traced.tif')
    return tips

origintif = '/Users/wonh/test/6.tif'
cropx = 100
cropy = 100
thresholdt = 55
percentage = 0.00005
folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)
# cropimg(cropx,cropy,origintif)  #crop the original tif

# get the first swc file using detecting soma
line = '8_3'
# line = getinfo(folder, line, thresholdt, percentage)
# line.get3d_mat()
# line.tsatisfied()
# line.traceornot()
# line.gettrace(np.asarray([]))
os.rename(folder + '/' + line + '.tif', folder + '/' + line + '_traced.tif')  
xno = 3
yno = 8
boundary_name = str(yno) + '_' + str(xno)
total = 0
tip_stack = tip_detecting(folder, xno, yno, boundary_name + '.swc')

total += tip_stack.shape[0]
print('total at beginning is: ' + str(total))
count = 0
order = 1
while count < total:
    print('count: ' + str(count) + ' total: ' + str(total))
    current_tip = tip_stack[count,:]
    current_tip[2] -= cropx * (current_tip[0] - 1)
    current_tip[3] -= cropy * (current_tip[1] - 1)
    print('current tip:' + str(current_tip))
    if current_tip[6] == 0:
        # ymin
        next_xno = current_tip[0]
        next_yno = current_tip[1]-1
        
    elif current_tip[6] == 1:
        # ymax
        next_xno = current_tip[0] 
        next_yno = current_tip[1] + 1
        
    elif current_tip[6] == 2:
        # xmin
        next_xno = current_tip[0] - 1
        next_yno = current_tip[1] 
    else:
        # xmax
        next_xno = current_tip[0] + 1
        next_yno = current_tip[1]
    tif_found = False
    print('next: ' + str(next_yno).split('.')
          [0] + '_' + str(next_xno).split('.')[0] + '.tif')
    dirs = os.listdir(folder)
    for f in dirs:
        if f == str(next_yno).split('.')[0] + '_' + str(next_xno).split('.')[0] + '.tif':
            tif_found = True
            print('tif_found is true')
            somainfo = np.array([current_tip[2], current_tip[3], current_tip[4], current_tip[-2]])
            tips = tif_tracing(folder,f, next_xno, next_yno, thresholdt, percentage, somainfo, order)
            i = 0
            print('tips_new: ' + str(tips))
            while i < tips.shape[0]:
                j = 0
                put = True
                while j < tip_stack.shape[0]:
                    if tips[i, 2] == tip_stack[j, 2] and tips[i, 3] == tip_stack[j, 3] and tips[i, 4] == tip_stack[j, 4]:
                        print('this tip is not new, we do not put it into the stack:')
                        put = False
                        break
                    j += 1
                if put is True:
                    tip_stack = np.vstack((tip_stack, tips[i, :]))
                    total += 1
                i += 1
            order += 1
            break

    if tif_found is False:
        print('tif not found')
        count += 1
        continue
        
    count += 1

