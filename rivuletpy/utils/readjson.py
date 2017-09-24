
import json
from collections import defaultdict
import multiprocessing as mp
import shutil
import csv
from rivuletpy.utils.io import *
jsonfilepath='/home/rong/Desktop/Gold166-JSON/'




def readtif(jsonfilepath):
    container = 'filename\tthreshold\tdimx\tdimy\tdimz\tsize(x*y*z)'#the first line of file to indicate the type of the content
    if os.path.exists(jsonfilepath + "jsoninfo"):#if there is a folder, rewrite it. If not, create it.
        shutil.rmtree(jsonfilepath + "jsoninfo")
    os.makedirs(jsonfilepath + "jsoninfo")
    d = defaultdict(int)  # set original dictionary
    list = os.listdir(jsonfilepath)
    for l in list:
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
    #output files sorted by its size
    for item in sorted(d,key=d.get,reverse=True):
        container=container+'\n'+item+"\t"+str(d[item])
    outputfile = open(jsonfilepath + "jsoninfo/"+"detailedinfo.txt", "w")
    outputfile.write(container)
    outputfile.close()


    with open( jsonfilepath + "jsoninfo/"+"detailedinfo.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        lines = container.split('\n')
        for line in lines:
            writer.writerow([line])
readtif(jsonfilepath)