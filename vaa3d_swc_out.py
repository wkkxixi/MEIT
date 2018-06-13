import os
import shutil
from collections import defaultdict
import json
import numpy as np
import csv

def readtif_swcout(jsonfilepath):
	'''
	Read jsoninfo file inside a dataset to grab information of all images inside this dataset
	Input: Dataset folder name
	Generates .csv and .txt files
	'''
	container = 'filename\tthreshold\tdimx\tdimy\tdimz\tsize(x*y*z)'#the first line of file to indicate the type of the content
	if os.path.exists(jsonfilepath + "jsoninfo"):#if there is a folder, rewrite it. If not, create it.
		# delete a directory and all its contents
		shutil.rmtree(jsonfilepath + "jsoninfo")
	os.makedirs(jsonfilepath + "jsoninfo")
	d = defaultdict(int)  # set original dictionary
	list = os.listdir(jsonfilepath)  # all the file and dirs in Gold166-JSON
	for l in list:
		print(l)
		if l.split(".")[-1]=='json':
			if l.split(".")[-2]!='pp':
				with open(jsonfilepath+l) as data_file:
					data = json.load(data_file)
				Keys=data['data'].keys()
				for Key in Keys:
					keys=data['data'][Key].keys()
				for key in keys:
					filename=data['data'][Key][key]['imagepath']
					threshold=data['data'][Key][key]['misc']['threshold']
					img = loadimg_swcout(jsonfilepath+filename)
					x,y,z=img.shape
					d[filename+'\t'+str(threshold)+'\t'+str(x)+'\t'+str(y)+'\t'+str(z)]=x*y*z
	#output files sorted by its size
	for item in sorted(d,key=d.get,reverse=True):
		container=container+'\n'+item+"\t"+str(d[item])
	outputfile = open(jsonfilepath + "jsoninfo/"+"detailedinfo.txt", "w")
	outputfile.write(container)
	outputfile.close()


	with open(jsonfilepath + "jsoninfo/"+"detailedinfo.csv", "w") as csv_file:
		writer = csv.writer(csv_file)
		lines = container.split('\n')
		for line in lines:
			writer.writerow([line])

def loadimg_swcout(file):
	if file.endswith('.mat'):
		filecont = sio.loadmat(file)
		img = filecont['img']
		for z in range(img.shape[-1]): # Flip the image upside down
			img[:,:,z] = np.flipud(img[:,:,z])
		img = np.swapaxes(img, 0, 1)
	elif file.endswith('.tif'):
		img = loadtiff3d_swcout(file)
	elif file.endswith('.nii') or file.endswith('.nii.gz'):
		import nibabel as nib
		img = nib.load(file)
		img = img.get_data()
	else:
		raise IOError("The extension of " + file + 'is not supported. File extension supported are: *.tif, *.mat, *.nii')
	return img

def loadtiff3d_swcout(filepath):
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

vaa3dpath = '/home/donghao/Desktop/wangheng/Vaa3D_Ubuntu_64bit_v3.200/vaa3d'
goldenfolderpath = '/home/donghao/Desktop/wangheng/Gold166-JSON-meit/'
# for x in range(1, 8):
# 	# img path
# 	stri = str(x)
# 	img_path = goldenfolderpath + '/chickuw/' + stri + '.tif'
#     # rivulet command
# 	rivulet_prefix = 'python3 main.py --file /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/'
# 	suffix = '.tif --threshold 5 --iter 5 --out'
# 	rivuletcmd = rivulet_prefix + stri + suffix + " /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/zihaoswc/" + stri + ".swc"
# 	# neutube command
# 	neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path

# readtif_swcout(goldenfolderpath)  # read json files to get location information
index = 0

with open(goldenfolderpath + 'jsoninfo/detailedinfo.txt') as f:
	lines = f.readlines()  # read every line
	for item in lines:
		if item.__contains__('.'):  # escape the first line and recognize the path
			filename = item.split('\t')[0]
			threshold = int(item.split('\t')[1])
			print(filename)
			neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path
			print(neutubecmd)