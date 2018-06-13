import os
vaa3dpath = '/home/donghao/Desktop/wangheng/Vaa3D_Ubuntu_64bit_v3.200/vaa3d'
goldenfolderpath = '/home/donghao/Desktop/wangheng/Gold166-JSON-meit/'
for x in range(1, 8):
	# img path
	stri = str(x)
	img_path = goldenfolderpath + 'chickuw/' + stri + '.tif'
    # rivulet command
	rivulet_prefix = 'python3 main.py --file /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/'
	suffix = '.tif --threshold 5 --iter 5 --out'
	rivuletcmd = rivulet_prefix + stri + suffix + " /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/zihaoswc/" + stri + ".swc"
	# neutube command
	neutubecmd = vaa3dpath + " -x neuTube -f neutube_trace -i " + img_path
	os.system(neutubecmd)










    # # neutube_prefix = vaa3dpth + " -x neuTube -f neutube_trace -i"
    # img_path = 'chickuw/'+ stri + '.tif'
    # neutubecmd = neutube_prefix + img_path
    # print(neutubecmd)
    # # print(rivuletcmd)
	# # os.system(rivuletcmd)