from rivuletpy.utils.io import *
import os, math
inputpath="/home/vv/Desktop/new/1.tif"
img=loadimg(inputpath)
dirpath=inputpath.split(".")[0]


def cropimg(cropx,cropy,threshold,img):
    savepath = dirpath + "_"+str(cropx)+"_"+str(cropy)+"/"
    os.mkdir(savepath)
    os.mkdir(savepath + "txt")
    ratio=""
    ratiofile = open(savepath + "txt/"+str(cropx)+"_"+str(cropy)+".txt", "w")
    x,y,z=img.shape
    # print(x,y,z)
    for i in range(cropy,y,cropy):
        #每一横行的输出
        for j in range(cropx,x,cropx):
            oneitem=img[j-cropx:j,i-cropy:i,:]
            loc=str(int(i/cropy))+"_"+str(int(j/cropx))
            ratio=ratio+"\n"+loc
            writetiff3d(savepath+loc+".tif", oneitem)
        #每一横行如果有剩的最后一个输出
        if(x%cropx!=0):
            linelast=img[x-x%cropx:x,i-cropy:i,:]
            loc=str(int(i/cropy)) +"_"+ str(int(j/cropx+1))
            ratio=ratio+"\n"+loc
            writetiff3d(savepath + loc +
                        ".tif", linelast)
    # print("final line begins")
    if(y%cropy!=0):
        for k in range(cropx,x,cropx):
            lastline=img[k-cropx:k,y-y%cropy:y,:]
            loc=str(int(i/cropy+1)) + "_"+str(int(k/cropx))
            ratio = ratio+"\n"+loc
            writetiff3d(savepath + loc +
                        ".tif", lastline)
    #行列均有剩的最后一个
    # print("lucky last one")
    if((y%cropy!=0)and(x%cropx!=0)):
        lastone=(img[x-x%cropx:x,y-y%cropy:y,:])
        loc=str(int(i/cropy+1)) +"_"+ str(int(j/cropx+1))
        ratio = ratio+"\n"+loc
        writetiff3d(savepath + loc
                    +".tif", lastone)
    ratiofile.write(ratio)
    ratiofile.close()

def combined(directory):
    list = os.listdir(directory)  # dir is your directory path
    xs = []#use to contain all x
    ys = []#use to contain all y
    for l in list:
        splited = l.split(".")
        if len(splited)>1: #to avoid the txt file
            x = splited[0].split("_")[0]
            y = splited[0].split("_")[1]
            rest=".tif"
            xs.append(int(x))
            ys.append(int(y))
    xs.sort()
    ys.sort()
    xmax = xs[-1]#find the maxmum x
    ymax = ys[-1]#find the maxmum y
    print("xmax:" + str(xmax)+"ymax:" + str(ymax))
    for ylocation in range(1, ymax + 1):
        # every same x in y direction combined
        liney = loadimg(directory + "/1_" + str(ylocation) + rest)
        for xlocation in range(2, xmax + 1):
            debris = loadimg(directory + "/" + str(xlocation) + "_" + str(ylocation) + rest)
            liney = np.concatenate((liney, debris), axis=1)
        #every x direction combined to get the final one part
        if (ylocation == 1):
            wholepart = liney
            print(wholepart)
        else:
            wholepart = np.concatenate((wholepart, liney), axis=0)
    writetiff3d(directory + "/wholepart.tif",wholepart)
cropimg(100,90,10,img)
combined("/home/vv/Desktop/new/1_100_90")

