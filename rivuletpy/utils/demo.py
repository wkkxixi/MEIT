from rivuletpy.utils.io import *
from rivuletpy.soma import Soma
from rivuletpy.trace import R2Tracer
import numpy as np
import os
from rivuletpy.tip import Tip
from rivuletpy.utils.folderinfo import *
from scipy.ndimage.interpolation import zoom


def boundary_constructor(x0, x1, y0, y1, z0, z1, f):

    swc_stack = np.zeros((1, 7))
    swc_stack[0, :] = np.asarray(
        [0, 7, x0, y0, z0, 1, 3])  # 1
    swc_stack = np.vstack((swc_stack, np.asarray(
        [1, 7, x1, y0, z0, 1, 0])))  # 2
    swc_stack = np.vstack((swc_stack, np.asarray(
        [2, 7, x1, y0, z1, 1, 1])))  # 3
    swc_stack = np.vstack((swc_stack, np.asarray(
        [3, 7, x0, y0, z1, 1, 2])))  # 4
    swc_stack = np.vstack((swc_stack, np.asarray(
        [4, 7, x0, y1, z0, 1, 7])))  # 1
    swc_stack = np.vstack((swc_stack, np.asarray(
        [5, 7, x1, y1, z0, 1, 4])))  # 2
    swc_stack = np.vstack((swc_stack, np.asarray(
        [6, 7, x1, y1, z1, 1, 5])))  # 3
    swc_stack = np.vstack((swc_stack, np.asarray(
        [7, 7, x0, y1, z1, 1, 6])))  # 4
    swc_stack = np.vstack((swc_stack, np.asarray(
        [8, 7, x1, y1, z0, 1, 1])))  # 2
    swc_stack = np.vstack((swc_stack, np.asarray(
        [9, 7, x0, y1, z0, 1, 0])))  # 1
    swc_stack = np.vstack((swc_stack, np.asarray(
        [10, 7, x1, y1, z1, 1, 2])))  # 3
    swc_stack = np.vstack((swc_stack, np.asarray(
        [11, 7, x0, y1, z1, 1, 3])))  # 4
    saveswc(f, swc_stack)


folder = '/Users/wonh/Gold166-JSON/mousergc/'
filename = '1.tif'
threshold = 9
cropx = 100
cropy = 100
zoom_factor = 0.25  # minimize the original image to detect soma
directory = folder + \
    filename.split('.')[0] + '_' + str(cropx) + '_' + \
    str(cropy) + '_' + str(zoom_factor) + '_demo4'
if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(directory + '_boundary/'):
    os.makedirs(directory + '_boundary/')
img = loadimg(folder + filename)

print('img shape is: ' + str(img.shape))
# img, crop_region = crop(img, 0)  No need to crop by default?

# Soma detecting
print('------step 1: Soma detecting-------')
print('Zoom factor is ' + str(zoom_factor))
zoomed_img = zoom(img, zoom_factor)
# print('zoomed_img shape: ' + str(zoomed_img.shape))
# bimg=(img > threshold).astype('int')  # Segment image
bimg = (zoomed_img > threshold).astype('int')  # Segment image 
soma = Soma()
soma.detect(bimg, simple=True, silent=False)
for i in range(0,3):
    soma.centroid[i] = min((soma.centroid[i] + 1) / zoom_factor - 1, img.shape[i]-1)



centroid = soma.centroid
print('Soma info is: ' + str(centroid) + ' radius is: ' + str(soma.radius))
# Define Soma area (maximum: cropx*cropy)
subx_min = max(centroid[0] - cropx/2, 0)
subx_max = min(centroid[0] + cropx/2, img.shape[0])
suby_min = max(centroid[1] - cropy/2, 0)
suby_max = min(centroid[1] + cropy/2, img.shape[1])
soma_area = np.asarray([subx_min, subx_max, suby_min, suby_max])
centroid_in_subarea = np.asarray(
    [centroid[0] - subx_min, centroid[1] - suby_min, centroid[2]])
print('Soma area is (xmin xmax ymin ymax) ' + str(soma_area))
print('centroid_in_subarea: ' + str(centroid_in_subarea))

q = [Tip(0, soma_area, soma.radius, centroid_in_subarea)]
index = 0
total = 1

tracer = R2Tracer(img=img, cropx=cropx, cropy=cropy)
print('-------step 2: tracing from tips')
while index < total:
    print('>>>index: ' + str(index) + ' total: ' + str(total))
    # for e in q:
    #     print(e.tvalue())
    tip = q[0]
    print('dequeue one tip: '+str([tip.xmin(), tip.xmax(), tip.ymin(), tip.ymax()]) + ' pos: ' + str(tip.pos()) + ' tvalue: ' + str(tip.tvalue()) + ' xyz: ' + str(tip.xyz()))
    index += 1
    q = q[1:]
    
    
    swc, tips=tracer.trace(tip, threshold) 

    if swc is None:
        continue
    # print('swc, tips returned by trace() ' + str(swc._data.shape))
    swc.save(directory +'/'+ filename.split('.')[0] + '_demo3_' + str(index) + '.swc')
    if len(tips) == 0:
        print('no tip need to be added')
        continue
    # Construct boundary
    boundary_constructor(tip.xmin(), tip.xmax() - 1, tip.ymin(), tip.ymax() - 1, 0,
                         img.shape[2] - 1, directory + '_boundary/' + filename.split('.')[0] + '_boundary_' + str(index) + '.swc')

    for tip in tips:
        if tip.xyz() is None:
            continue
        q.append(tip)
        total += 1
    
    q.sort(key=lambda x: x._tvalue, reverse=False)



print('small swcs are being combined')
combinedswc(directory)
print('combined successfully!')
    

