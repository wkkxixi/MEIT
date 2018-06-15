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
			threshold = int(item.split('\t')[1])
			img_path = goldenfolderpath + filename
			neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path
			counter_im = counter_im + 1
			snakecmd = vaa3dpath + " -x snake -f snake_trace -i " + img_path
			TreMapcmd = vaa3dpath + " -x TReMap -f trace_mip -i " + img_path + " -p 0 1 " + str(threshold) + " 0 1 0 5"
			# os.system(neutubecmd)
			# os.system(snakecmd)
			# os.system(TreMapcmd)
			gtswcpath = goldenfolderpath + os.path.splitext(filename)[0] + '.swc'
			neutubeswcpath = goldenfolderpath + filename + '_neutube.swc'
			gtswc = loadswc(gtswcpath)
			neutubeswc = loadswc(neutubeswcpath)
			prf_accuracy, swc_compare_3_2 = precision_recall(neutubeswc, gtswc)
			print(filename, prf_accuracy[0], prf_accuracy[1], prf_accuracy[2])
