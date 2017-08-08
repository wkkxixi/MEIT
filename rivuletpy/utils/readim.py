from rivuletpy.utils.io import *
import os, math
inputpath="/home/vv/Desktop/new/1.tif"
img=loadimg(inputpath)
dirpath=inputpath.split(".")[0]
os.mkdir(dirpath)
savepath=dirpath+"/"
def cropimg(cropx,cropy,img):
    x,y,z=img.shape
    print(x,y,z)
    for i in range(cropy,y,cropy):
        #每一横行的输出
        for j in range(cropx,x,cropx):
            oneitem=img[j-cropx:j,i-cropy:i,:]
            writetiff3d(savepath+str(i/cropy)+"_"+str(j/cropx)+"_"+str(oneitem.shape[0])+"_"+str(oneitem.shape[1])+".tif"
, oneitem)
        #每一横行如果有剩的最后一个输出
        if(x%cropx!=0):
            linelast=img[x-x%cropx:x,i-cropy:i,:]
            writetiff3d(savepath + str(i/cropy) +"_"+ str(j/cropx+1) + "_"+str(linelast.shape[0])+"_"+str(linelast.shape[1])+".tif"
                        , linelast)
            print("one single line ended")
    #最后一行开始
    print("final line begins")
    if(y%cropy!=0):
        for k in range(cropx,x,cropx):
            lastline=img[k-cropx:k,y-y%cropy:y,:]
            writetiff3d(savepath + str(i/cropy+1) + "_"+str(j/cropx) + "_"+str(lastline.shape[0])+"_"+str(lastline.shape[1])+".tif"
                    , lastline)
    #行列均有剩的最后一个
    print("lucky last one")
    if((y%cropy!=0)and(x%cropx!=0)):
        lastone=(img[x-x%cropx:x,y-y%cropy:y,:])
        writetiff3d(savepath + str(i/cropy+1) +"_"+ str(j/cropx+1) + "_"+str(lastone.shape[0])+"_"+str(lastone.shape[1])+".tif"
                    , lastone)
cropimg(50,50,img)

