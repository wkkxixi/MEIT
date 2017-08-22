from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
origintif="/home/vv/Desktop/new/1.tif"
cropx=80
cropy=70
thresholdt=10
percentage=0.0000005
folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)
cropimg(cropx,cropy,origintif)
combined(folder)

file = open(folder+"/txt/"+"nameinfo.txt", 'r')
for line in file:
    if "_" in line:
        line = line.split('\n')[0]
        line = getinfo(folder,line,thresholdt, percentage)
        line.get3d_mat()
        line.tsatisfied()
        line.traceornot()
        line.gettrace()
combinedswc(folder)
