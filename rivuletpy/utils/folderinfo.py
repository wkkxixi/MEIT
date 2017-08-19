from rivuletpy.utils.io import *
import os, math
#This is for croping origin tif into pieces of size(cropx*cropy*z)

def cropimg(cropx,cropy,origintif):
    #The savefile consists of cropx_cropy eg: 2_3.tif
    img=loadimg(origintif)
    savepath = origintif.split(".")[0] + "_"+str(cropx)+"_"+str(cropy)+"/"
    os.mkdir(savepath)
    os.mkdir(savepath + "txt")
    locinfo=""
    locfile = open(savepath + "txt/"+"nameinfo.txt", "w")
    shapex,shapey,shapez=img.shape
    # print(shapex,shapey,shapez)
    for i in range(cropy,shapey,cropy):
        #The output of every item which matches the size(cropx*cropy) perfectly.
        for j in range(cropx,shapex,cropx):
            oneitem=img[j-cropx:j,i-cropy:i,:]
            loc=str(int(i/cropy))+"_"+str(int(j/cropx))
            locinfo=locinfo+"\n"+loc
            writetiff3d(savepath+loc+".tif", oneitem)
        #if shapex has a remainder (rx)of cropx, the item with the size(rx*cropy) appears at the end of a line.
        if(shapex%cropx!=0):
            linelast=img[shapex-shapex%cropx:shapex,i-cropy:i,:]
            loc=str(int(i/cropy)) +"_"+ str(int(j/cropx+1))
            locinfo=locinfo+"\n"+loc
            writetiff3d(savepath + loc +
                        ".tif", linelast)
    # if cropy cannot be perfectly divided by shapey,then this remainder(ry) is the y coordinate of the last line
    if(shapey%cropy!=0):
        for k in range(cropx,shapex,cropx):
            lastline=img[k-cropx:k,shapey-shapey%cropy:shapey,:]
            loc=str(int(i/cropy+1)) + "_"+str(int(k/cropx))
            locinfo = locinfo+"\n"+loc
            writetiff3d(savepath + loc +
                        ".tif", lastline)
    #if both shapex and shapey have their remainders(rx,ry),the lastone with size(rx*ry) is shown
    # print("lucky last one")
    if((shapey%cropy!=0)and(shapex%cropx!=0)):
        lastone=(img[shapex-shapex%cropx:shapex,shapey-shapey%cropy:shapey,:])
        loc=str(int(i/cropy+1)) +"_"+ str(int(j/cropx+1))
        locinfo = locinfo+"\n"+loc
        writetiff3d(savepath + loc
                    +".tif", lastone)
    locfile.write(locinfo)
    locfile.close()

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


