from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
import time

origintif="/home/vv/Desktop/new/1.tif"
cropx=100
cropy=100
thresholdt=40
percentage=0.00005
folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)
cropimg(cropx,cropy,origintif)
combined(folder)

file = open(folder+"/txt/"+"nameinfo.txt", 'r')
start_time=time.time()
for line in file:
    if "_" in line:
        print(line, "is on processing")
        line = line.split('\n')[0]
        line = getinfo(folder,line,thresholdt, percentage)
        line.get3d_mat()
        line.tsatisfied()
        line.traceornot()
        line.gettrace()
print('small swcs are being combined')
end_time=time.time()
print(end_time-start_time)
combinedswc(folder)
print('combined successfully!')
