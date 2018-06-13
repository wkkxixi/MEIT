import os;
for x in range(1950,1951):
	rivulet_prefix = 'python3 main.py --file /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/'
	stri = str(x)
	suffix = '.tif --threshold 5 --iter 5 --out'
	rivuletcmd = rivulet_prefix + stri + suffix + " /home/donghao/Desktop/zihao_dicta/first2000data/first2000-tif-ordered/zihaoswc/" + stri + ".swc"
	print(rivuletcmd)
	# os.system(rivuletcmd)