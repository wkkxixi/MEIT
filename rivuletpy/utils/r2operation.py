from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.toswc import *
import multiprocessing as mp
import time
from pathlib import Path
import traceback
folderpath = '/Users/wonh/Gold166-JSON/'


with open(folderpath + 'jsoninfo/detailedinfo.txt') as f:
    lines = f.readlines()  # read every line
    for item in lines:
        if item.__contains__('.'):  # escape the first line and recognize the path
            # print(item)
            filename = item.split('\t')[0]
            threshold = int(item.split('\t')[1])
            sizexyz = int(item.split('\t')[5])
            origintif = folderpath + filename
            r2path = folderpath + \
                filename.split('/')[0] + '/r2/' + \
                filename.split('/')[1] + '.r2.swc'
            # only when (the color value / whole background value)>percentage, it will be recorded, otherwise, it will be discarded when producing swc
            percentage = 0.00005
            
            try:
                checkfile = Path(r2path)
                if checkfile.is_file():
                    continue
                else:
                    print(filename, "is on processing")
                    line = getinfo(folderpath, filename,
                                   threshold, percentage, sizexyz)
                    line.get3d_mat()
                    line.tsatisfied()
                    line.traceornot()
                    line.gettrace()
            except (Exception):
                print('Exception!!!!! ' + origintif)
                traceback.print_exc()



