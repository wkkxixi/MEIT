from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.cropswc import *
from rivuletpy.utils.readjson import *
from rivuletpy.utils.outputSmallSwc import *
from rivuletpy.utils.compareswc import *
import multiprocessing as mp
import time
folderpath = '/Users/wonh/Gold166-JSON/'
def operationcombine(folder, line, thresholdt, percentage):
    if "_" in line:
        # print(line, "is on processing")
        line = line.split('\n')[0]
        line = getinfo(folder, line, thresholdt, percentage)
        line.get3d_mat()
        line.tsatisfied()
        line.traceornot()
        line.gettrace()

readtif(folderpath)#read json files to get location information
content = 'Path\tPrecision\tRecall\tF1'#content format of the compareswc
with open(folderpath+'jsoninfo/detailedinfo.txt') as f:
    lines = f.readlines()#read every line
    for item in lines:
        if item.__contains__('.'):#escape the first line and recognize the path
            # print(item)
            filename=item.split('\t')[0]
            threshold=int(item.split('\t')[1])
            shapex=int(item.split('\t')[2])#the shape of tif in x dimension
            shapey=int(item.split('\t')[3])#the shape of tif in y dimension
            origintif=folderpath+filename
            cropx=100#the crop size of x dimension
            cropy=100#the crop size of y dimension
            percentage=0.00005#only when (the color value / whole background value)>percentage, it will be recorded, otherwise, it will be discarded when producing swc
            folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)#name of the folder and swc
            if(shapex<cropx and shapey<cropy):#if the size of tif is too small to be croped, it will be processed in smallswc function
                smallswc(origintif,threshold,folder)
            else:
                cropimg(cropx,cropy,origintif)
                print(item,"Now it is in cropimg processing")
                # combined(folder)

                file = open(folder+"/txt/"+"nameinfo.txt", 'r')
                begin_time=time.time()
                pool=mp.Pool()
                for line in file:
                    pool.apply_async(operationcombine, args=(folder, line, threshold, percentage))
                pool.close()
                pool.join()
                end_time=time.time()
                print(end_time-begin_time)
                # print('small swcs are being combined')
                combinedswc(folder)
                print('small swcs are combined successfully!')
            try:

                swc1 = loadswc(origintif.split('.')[0] + '.swc')
                swc2 = loadswc(origintif.split('.')[0] + '_'+str(cropx)+'_'+str(cropy)+'.swc')
                print(origintif.split('.')[0] + '_'+str(cropx)+'_'+str(cropy)+'.swc')# name of the folder and swc
                # precision_recall(swc1, swc2)
                prf, swc_compare = precision_recall(swc1, swc2)
                saveswc(origintif.split('.')[0] + '_gao_compare.swc', swc_compare)
                content = content + '\n' + origintif + '\t%.2f\t%.2f\t%.2f' % prf
            except (Exception):
                print(origintif)
lines = content.split('\n')

with open(folderpath + 'gao_compare.csv', "w") as csv_file:
    writer = csv.writer(csv_file)
    for line in lines:
        writer.writerow([line])
