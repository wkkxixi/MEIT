from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
import multiprocessing as mp
import time

origintif="/home/rong/Downloads/1.tif"
cropx=100
cropy=100
thresholdt=40
percentage=0.00005
folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)
cropimg(cropx,cropy,origintif)
combined(folder)

file = open(folder+"/txt/"+"nameinfo.txt", 'r')


def operationcombine(folder, line, thresholdt, percentage):
    if "_" in line:
        print(line, "is on processing")
        line = line.split('\n')[0]
        line = getinfo(folder, line, thresholdt, percentage)
        line.get3d_mat()
        line.tsatisfied()
        line.traceornot()
        line.gettrace()
begin_time=time.time()
print(time.ctime())
pool=mp.Pool()
for line in file:
    pool.apply_async(operationcombine, args=(folder, line, thresholdt, percentage))
pool.close()
pool.join()
    # t = threading.Thread(target=operationcombine, args=(folder, line, thresholdt, percentage))
    # t.start()
    # threads.append(t)
# for thread in threads:
#     thread.join()
print(time.ctime())
end_time=time.time()
print(end_time-begin_time)
print('small swcs are being combined')
# combinedswc(folder)
print('combined successfully!')