from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
from rivuletpy.utils.readjson import *
from rivuletpy.utils.outputSmallSwc import *
from rivuletpy.utils.compareswc import *
import multiprocessing as mp
import time
from pathlib import Path
import traceback
from scipy.ndimage.interpolation import zoom
folderpath = '/Users/wonh/Gold166-JSON/'


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

# readtif(folderpath)  # read json files to get location information
# content format of the compareswc
content = 'path\tthreshold\tdimx\tdimy\tdimz\tsize(x*y*z)\tcrop2VSgt_precision\tcrop2VSgt_recall\tcrop2VSgt_f1\tcropVSgt_precision\tcropVSgt_recall\tcropVSgt_f1\tr2VSgt_precision\tr2VSgt_recall\tr2VSgt_f1\tf1:crop-r2\tf1:crop2-r2'
with open(folderpath + 'jsoninfo/detailedinfo.txt') as f:
    lines = f.readlines()  # read every line
    for item in lines:
        if item.__contains__('.'):  # escape the first line and recognize the path
            # print(item)
            filename = item.split('\t')[0]
            threshold = int(item.split('\t')[1])
            

            # the shape of tif in x dimension
            shapex = int(item.split('\t')[2])
            # the shape of tif in y dimension
            # if shapex > 1000:
            #     continue
            shapey = int(item.split('\t')[3])
            # if shapey > 1000:
            #     continue
            shapez = int(item.split('\t')[4])
            sizexyz = int(item.split('\t')[5])
            cropx = 100
            cropy = 100

            # cropx = 400  # the crop size of x dimension
            # cropy = 400  # the crop size of y dimension
            origintif = folderpath + filename

            zoom_factor = 0.25  # minimize the original image to detect soma
            directory = folderpath + \
                filename.split('.')[0] + '_' + str(cropx) + '_' + \
                str(cropy) + '_' + str(zoom_factor) + '_demo4'
            if not os.path.exists(directory):
                print(filename + ' is on processing')
                os.makedirs(directory)
            else:
                # print(directory + ' exists already')
                continue
            if not os.path.exists(directory + '_boundary/'):
                os.makedirs(directory + '_boundary/')
            if not os.path.exists(folderpath+filename.split('/')[0] + '/crop_v2/'):
                os.makedirs(folderpath + filename.split('/')[0] + '/crop_v2/')
            img = loadimg(origintif)
            print('img shape is: ' + str(img.shape))
            print('threshold is: ' + str(threshold))
            zoomed_img = zoom(img, zoom_factor)
            bimg = (zoomed_img > threshold).astype('int')  # Segment image
            soma = Soma()
            soma.detect(bimg, simple=True, silent=False)
            for i in range(0, 3):
                soma.centroid[i] = min((soma.centroid[i] + 1) /
                           zoom_factor - 1, img.shape[i] - 1)
            centroid = soma.centroid
            subx_min = max(centroid[0] - cropx / 2, 0)
            subx_max = min(centroid[0] + cropx / 2, img.shape[0])
            suby_min = max(centroid[1] - cropy / 2, 0)
            suby_max = min(centroid[1] + cropy / 2, img.shape[1])
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
                tip = q[0]
                print('>>>index: ' + str(index) + ' total: ' + str(total))
                index += 1
                q = q[1:]
                swc, tips = tracer.trace(tip, threshold)
                if swc is None:
                    continue
                swc.save(directory + '/' + filename.split('.')
                         [0].split('/')[1] + '_' + str(cropx) + '_' + str(cropy) + '_' + str(zoom_factor) + '_demo3_' + str(index) + '.swc')
                if len(tips) == 0:
                    continue
                # Construct boundary
                boundary_constructor(tip.xmin(), tip.xmax() - 1, tip.ymin(), tip.ymax() - 1, 0,
                                     img.shape[2] - 1, directory +
                                     '_boundary/' + filename.split('.')
                                     [0].split('/')[1] + '_boundary_' + str(index) + '.swc')
                
                for tip in tips:
                    if tip.xyz() is None:
                        continue
                    q.append(tip)
                    total += 1
                q.sort(key=lambda x: x._tvalue, reverse=False)

            print('-------step 3: small swcs are being combined')
            combinedswc(directory)
            print('combined successfully!')
            
            
            '''
            r2path = folderpath + \
                filename.split('/')[0] + '/r2/' + \
                filename.split('/')[1] + '.r2.swc'
            crp2path = folderpath + filename.split('/')[0] + '/crop_v2/' + filename.split('.')[0].split('/')[1] + '_' + str(cropx) + '_' + str(cropy) + '_' + str(zoom_factor) + '_demo3.swc'
            crp1path = folderpath + \
                filename.split('/')[0] + '/crop_v1/' + filename.split('/')[1].split('.')[
                    0] + '_100_100.swc'
            
            
            
            # compare 3 methods
            try:
                swc2 = loadswc(origintif.split('.')[0] + '.swc')  # ground true
                swc1 = None
                swc4 = None
                if Path(crp1path).is_file():
                    swc1 = loadswc(crp1path)  # crop1 method
                    print('loading ' + crp1path)
                else:
                    continue
                if Path(crp2path).is_file():
                    swc4 = loadswc(crp2path)  # crop2 method
                    print('loading  ' + crp2path)
                else:
                    continue
                checkfile = Path(r2path)
                prf_1_2, swc_compare_1_2 = precision_recall(swc1, swc2)
                prf_4_2, swc_compare_4_2 = precision_recall(swc4, swc2)
                
                if checkfile.is_file():
                    swc3 = loadswc(r2path)  # r2 method
                    prf_3_2, swc_compare_3_2 = precision_recall(swc3, swc2)
                    saveswc(origintif.split('.')[
                            0] + '_r2_compare_gt.swc', swc_compare_3_2)

                    content = content + '\n' + filename + \
                        '\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f' % (
                            threshold, shapex, shapey, shapez, sizexyz)
                    content = content + '\t%.2f\t%.2f\t%.2f' % prf_4_2 #crop2
                    content = content + '\t%.2f\t%.2f\t%.2f' % prf_1_2 #crop1
                    content = content + '\t%.2f\t%.2f\t%.2f' % prf_3_2 #r2
                    diff_f1 = prf_1_2[2] - prf_3_2[2]
                    content = content + '\t%.2f' % diff_f1
                    diff2_f1 = prf_4_2[2] - prf_3_2[2]
                    content = content + '\t%.2f' % diff2_f1
                else:
                    content = content + '\n' + filename + '\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f' % (
                        threshold, shapex, shapey, shapez, sizexyz) + '\t%.2f\t%.2f\t%.2f' % prf_4_2 + '\t%.2f\t%.2f\t%.2f' % prf_1_2 + '\tnull\tnull\tnull\tnull\tnull'
                if not Path(origintif.split('.')[
                    0] + '_crop1_compare_gt.swc').is_file():
                    saveswc(origintif.split('.')[
                        0] + '_crop1_compare_gt.swc', swc_compare_1_2)
                    print('saving crop1_compare_gt.swc')
                if not Path(origintif.split('.')[
                        0] + '_crop22_compare_gt.swc').is_file():
                    saveswc(origintif.split('.')[
                        0] + '_crop22_compare_gt.swc', swc_compare_4_2)
                    print('saving crop22_compare_gt.swc')
            except (Exception):
                print('Exception!!!!! ' + origintif)
                traceback.print_exc()
           
lines = content.split('\n')

with open(folderpath + '_5_methods_compare.csv', "w") as csv_file:
    writer = csv.writer(csv_file)
    for line in lines:
        writer.writerow([line])

         '''
