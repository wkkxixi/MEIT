import os
from rivuletpy.utils.compareswc import *

def loadswc(filepath):
	'''
	Load swc file as a N X 7 numpy array
	'''
	swc = []
	with open(filepath) as f:
		lines = f.read().split("\n")
		for l in lines:
			if not l.startswith('#'):
				cells = l.split(' ')
				if len(cells) ==7:
					cells = [float(c) for c in cells]
					# cells[2:5] = [c-1 for c in cells[2:5]]
					swc.append(cells)
	return np.array(swc)

vaa3dpath = '/home/donghao/Desktop/wangheng/Vaa3D_Ubuntu_64bit_v3.200/vaa3d'
goldenfolderpath = '/home/donghao/Desktop/wangheng/Gold166-JSON-meit/'

# counter of the image
counter_im = 0
with open(goldenfolderpath + 'jsoninfo/detailedinfo.txt') as f:
	lines = f.readlines()  # read every line
	for item in lines:
		if item.__contains__('.'):  # escape the first line and recognize the path
			filename = item.split('\t')[0]
			imgname = os.path.basename(filename)
			imgid = os.path.splitext(imgname)[0]
# 			threshold = int(item.split('\t')[1])
# 			img_path = goldenfolderpath + filename
# 			counter_im = counter_im + 1
			# neutube command generation
# 			neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path
			# os.system(neutubecmd)
			# neutubeswcpath = goldenfolderpath + filename + '_neutube.swc'
			# neutubeswc = loadswc(neutubeswcpath)
			# gtswcpath = goldenfolderpath + os.path.splitext(filename)[0] + '.swc'
			# gtswc = loadswc(gtswcpath)

			# snake comparison is not completed due to large memory consumption
# 			snakecmd = vaa3dpath + " -x snake -f snake_trace -i " + img_path
			# os.system(snakecmd)

# 			TreMapcmd = vaa3dpath + " -x TReMap -f trace_mip -i " + img_path + " -p 0 1 " + str(threshold) + " 0 0 1 2"
# 			MOSTcmd = vaa3dpath + " -x MOST -f MOST_trace -i " + img_path + " -p 1 " + str(threshold)
# 			APP2swcpath = goldenfolderpath + filename + '_APP2.swc'
# 			APP2cmd = vaa3dpath + " -x vn2 -f app2 -i " + img_path + " -p NULL 0 " + str(threshold) + " 1 1 1 0 5" + " -o " + APP2swcpath
# 			APP2rmcmd = "rm " + img_path + ".swc"
# 			APP2rmcmd = "rm " + img_path + "_ini.swc"
# 			# os.system(TreMapcmd)
# 			# os.system(MOSTcmd)
# 			# os.system(APP2cmd)
# 			# os.system(APP2rmcmd)
			gtswcpath = goldenfolderpath + os.path.splitext(filename)[0] + '.swc'
# 			TreMapswcpath = goldenfolderpath + filename + '_XY_3D_TreMap.swc'
# 			MOSTswcpath = goldenfolderpath + filename + '_MOST.swc'
			APP2swcpath_option1 = goldenfolderpath + os.path.dirname(filename) + '/app2/' + imgname +'.app2.swc'
			APP2swcpath_option2 = goldenfolderpath + os.path.dirname(filename) + '/app2/' + imgname + '_APP2.swc'

			if os.path.exists(APP2swcpath_option1):
				APP2swc = loadswc(APP2swcpath_option1)
			elif os.path.exists(APP2swcpath_option2):
				APP2swc = loadswc(APP2swcpath_option2)
			smartswcpath_option1 = goldenfolderpath + os.path.dirname(filename) + '/smart/' + imgname + '.app2.swc'
			smartswcpath_option2 = goldenfolderpath + os.path.dirname(filename) + '/smart/' + imgname + '.app2.swc'

# 			# TreMapswc = loadswc(TreMapswcpath)
# 			# print('the shape of TreMapswc is : ', TreMapswc.shape[0])
# 			# if TreMapswc.shape[0] == 0:
# 			# 	# print('we found the problemed file')
# 			# 	TreMapcmd = vaa3dpath + " -x TReMap -f trace_mip -i " + img_path + " -p 0 1 " + '10' + " 0 0 1 0"
# 			# 	# os.system(TreMapcmd)
# 			# 	TreMapswc = loadswc(TreMapswcpath)
# 			# 	print(TreMapswc.shape)
# 			# if filename == 'fruitflylarvae/7.tif':
# 			# 	print(filename)
# 			# elif filename == 'zebrafishlarveRGC/1.tif':
# 			# 	print(filename)
# 			# else:
# 			# 	MOSTswc = loadswc(MOSTswcpath)
# 			# 	gtswc = loadswc(gtswcpath)
# 			# 	MOST_accuracy, _ = precision_recall(MOSTswc, gtswc)
# 			# 	print(filename, MOST_accuracy[0], MOST_accuracy[1], MOST_accuracy[2])
# 			# print(TreMapswc.shape)
# 			APP2swc = loadswc(APP2swcpath)
# 			# neutube_accuracy, _ = precision_recall(neutubeswc, gtswc)
# 			# TreMap_accuracy, _ = precision_recall(TreMapswc, gtswc)
# 			print(filename)
			APP2_accuracy, _ = precision_recall(APP2swc, gtswc)
			print(filename, APP2_accuracy[0], APP2_accuracy[1], APP2_accuracy[2])
# 			# print(filename, TreMap_accuracy[0], TreMap_accuracy[1], TreMap_accuracy[2])


# friutflylarvae_threshold = [76, 46, 71, 34, 107, 43, 77,  91, 16, 109, 50, 126]
# friutflylarvae_order =     [1,  2,  3,  4,   5,  6,  7,   8,  9,  10, 11, 12]
# janeliafly2 app2
# for i in range(1, 13):
# 	# img_path = goldenfolderpath + 'janeliafly2/' + str(i) +'.tif'
# 	# img_path = goldenfolderpath + 'fruitflylarvae/' + str(i) + '.tif'
# 	img_path = goldenfolderpath + 'fruitflylarvae/' + str(i) + '.tif'
# 	APP2swcpath = img_path + '_app2.swc'
# 	app2_threshold = friutflylarvae_threshold[i-1]
# 	app2cmd = vaa3dpath + " -x vn2 -f app2 -i " + img_path + " -p NULL 0 " + str(app2_threshold) + " 1 1 1 0 2" + " -o " + APP2swcpath
# 	os.system(app2cmd)

#mousetufts app2
# img_path = goldenfolderpath + 'mousetufts/' + str(i) + '.tif'
# APP2swcpath = img_path + '_app2.swc'
# app2cmd = vaa3dpath + " -x vn2 -f app2 -i " + img_path + " -p NULL 0 " + str(app2_threshold) + " 1 1 1 0 2" + " -o " + APP2swcpath
# os.system(app2cmd)

#janeliafly2 smart
# for i in range(3, 13):
# 	# img_path = goldenfolderpath + 'janeliafly2/' + str(i) +'.tif'
# 	img_path = goldenfolderpath + 'fruitflylarvae/' + str(i) + '.tif'
# 	smartcmd = vaa3dpath + " -x smartTrace -f smartTrace -i " + img_path
# 	os.system(smartcmd)