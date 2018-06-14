import os

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
			print(filename)
			neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path
			print(neutubecmd)
			counter_im = counter_im + 1
			snakecmd = vaa3dpath + " -x snake -f snake_trace -i " + img_path
			TreMapcmd = vaa3dpath + " -x TReMap -f snake_trace -i " + img_path + " -p 0 1 " + str(threshold) + " 0 1 0 5"
			# os.system(neutubecmd)
			# os.system(snakecmd)
			os.system(TreMapcmd)
print('the total image number is ', counter_im)
