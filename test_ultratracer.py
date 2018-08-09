from rivuletpy.soma import Soma
from rivuletpy.utils.folderinfo import *
from scipy.ndimage.interpolation import zoom
import os
from rivuletpy.utils.compareswc import *


vaa3dpath = '/home/heng/Downloads/Vaa3D_CentOS_64bit_v3.458/vaa3d'
goldenfolderpath = '/home/heng/Gold166-JSON-meit/'
# filename = 'mousergc/2.tif'
# threshold = 6
#
# img_path = goldenfolderpath + filename
# v3draw_path = img_path + '.v3draw'
# marker_path = img_path + '_marker.apo'
# v3draw_converter = vaa3dpath + ' -x convert_file_format -f convert_format -i ' + img_path +' -o ' + v3draw_path
# print(v3draw_converter)
# os.system(v3draw_converter)
# print('     converted tif to v3draw')
#
# zoom_factor = 0.25
# img = loadimg(img_path)
# zoomed_img = zoom(img, zoom_factor)
# bimg = (zoomed_img > threshold).astype('int')  # Segment image
#
# soma = Soma()
# soma.detect(bimg, simple=True, silent=False)
# for i in range(0, 3):
#     soma.centroid[i] = min((soma.centroid[i] + 1) /
#                            zoom_factor - 1, img.shape[i] - 1)
# with open(marker_path, 'w') as f:
#     f.write('0, 0, ,, ' + str(soma.centroid[2]) + ', '+ str(soma.centroid[0]) + ', ' + str(soma.centroid[1]) + ', 0,0,0,0,0,,,' )  # z, x, y
#
# print('     markder file created')
# ultratracercmd = vaa3dpath + " -x ultratracer -f trace_APP2_GD -i " + v3draw_path + ' -p ' + marker_path + ' ' + str(
#     512) + ' ' + str(1) + ' ' + str(3) + ' ' + str(threshold)
# print(ultratracercmd)
# os.system(ultratracercmd)
counter_im = 0
with open(goldenfolderpath + 'jsoninfo/detailedinfo.txt') as f:
    lines = f.readlines()
    for item in lines:
        if item.__contains__('.'):
            if counter_im == 0:
                continue
            filename = item.split('\t')[0]
            threshold = int(item.split('\t')[1])
            print(str(counter_im) + ': ' + filename + ' is on processing ' + 'threshold: ' + str(threshold))
            img_path = goldenfolderpath + filename
            output_folder = img_path.split('.tif')[0] + '_ultratracerAPP2/'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            v3draw_path = output_folder + filename.split('/')[-1] + '.v3draw'
            marker_path = img_path + '_marker.apo'
            v3draw_converter = vaa3dpath + ' -x convert_file_format -f convert_format -i ' + img_path +' -o ' + v3draw_path
            print(v3draw_converter)
            os.system(v3draw_converter)
            print('     converted tif to v3draw')
            counter_im = counter_im + 1
            zoom_factor = 0.25
            img = loadimg(img_path)
            zoomed_img = zoom(img, zoom_factor)
            bimg = (zoomed_img > threshold).astype('int')  # Segment image

            soma = Soma()
            soma.detect(bimg, simple=True, silent=False)
            for i in range(0, 3):
                soma.centroid[i] = min((soma.centroid[i] + 1) /
                                       zoom_factor - 1, img.shape[i] - 1)
            with open(marker_path, 'w') as f:
                f.write('0, 0, ,, ' + str(soma.centroid[2]) + ', '+ str(soma.centroid[0]) + ', ' + str(soma.centroid[1]) + ', 0,0,0,0,0,,,' )  # z, x, y

            print('     markder file created')
            ultratracercmd = vaa3dpath + " -x ultratracer -f trace_APP2_GD -i " + v3draw_path + ' -p ' + marker_path + ' ' + str(
                512) + ' ' + str(1) + ' ' + str(3) + ' ' + str(threshold)
            print(ultratracercmd)
            os.system(ultratracercmd)


# # counter of the image
# counter_im = 0
# with open(goldenfolderpath + 'jsoninfo/detailedinfo.txt') as f:
# 	lines = f.readlines()  # read every line
# 	for item in lines:
# 		if item.__contains__('.'):  # escape the first line and recognize the path
# 			filename = item.split('\t')[0]
# 			threshold = int(item.split('\t')[1])
#             print(str(counter_im) +': ' + filename + ' is on processing')
# 			img_path = goldenfolderpath + filename
#             v3draw_path = img_path + '.v3draw'
#             marker_path = img_path + '_marker.apo'
#             v3draw_converter = vaa3dpath + ' -x convert_file_format -f convert_format -i' + img_path +' -o ' + v3draw_path
#             os.system(v3draw_converter)
#             print('     converted tif to v3draw')
# 			counter_im = counter_im + 1
#             zoom_factor = 0.25
#             img = loadimg(img_path)
#             zoomed_img = zoom(img, zoom_factor)
#             bimg = (zoomed_img > threshold).astype('int')  # Segment image
#
#             soma = Soma()
#             soma.detect(bimg, simple=True, silent=False)
#             for i in range(0, 3):
#                 soma.centroid[i] = min((soma.centroid[i] + 1) /
#                                        zoom_factor - 1, img.shape[i] - 1)
#             with open(marker_path, 'w') as f:
#                 f.write('0, 0, ,, ' + str(soma.centroid[2]) + ', '+ str(soma.centroid[0]) + ', ' + str(soma.centroid[1]) + ', 0,0,0,0,0,,,' )  # z, x, y
#             print('     markder file created')
#             ultratracercmd = vaa3dpath + " -x ultratracer -f trace_APP2_GD -i " + v3draw_path + ' -p ' + marker_path + str(512) + ' ' + str(1) + ' ' + str(3) + ' ' + str(threshold)
#             os.system(ultratracercmd)

