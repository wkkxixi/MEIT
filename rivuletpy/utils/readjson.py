import json
from collections import defaultdict
import multiprocessing as mp
from pprint import pprint
from rivuletpy.utils.io import *
jsonfilepath='/home/rong/Documents/Gold166-JSON/'
# os.mkdir(jsonfilepath + "jsoninfo")
container='filename\tthreshold\tdimx\tdimy\tdimz\tsize(x*y*z)'
d=defaultdict(int)
list = os.listdir(jsonfilepath)
def readtif(l):
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
                img = loadimg(jsonfilepath+filename)
                x,y,z=img.shape
                print(img.shape)
                d[filename+'\t'+str(threshold)+'\t'+str(x)+'\t'+str(y)+'\t'+str(z)]=x*y*z
for file in list:
    readtif(file)
for item in sorted(d,key=d.get,reverse=True):
    container=container+'\n'+item+"\t"+str(d[item])
outputfile = open(jsonfilepath + "jsoninfo/"+"detailedinfo.txt", "w")
outputfile.write(container)
outputfile.close()