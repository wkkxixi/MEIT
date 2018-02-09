from rivuletpy.utils.io import *
from rivuletpy.utils.outputSmallSwc import *
import os, glob
import shutil
#This is for croping origin tif into pieces of size(cropx*cropy*z)
def boundary(x0, x1, y0, y1, z0, z1, f):
    swc = np.zeros((1, 7))
    swc[0, :] = np.asarray(
        [0, 7, x0, y0, z0, 1, 3])  # 1
    swc = np.vstack((swc, np.asarray(
        [1, 7, x1, y0, z0, 1, 0])))  # 2
    swc = np.vstack((swc, np.asarray(
        [2, 7, x1, y0, z1, 1, 1])))  # 3
    swc = np.vstack((swc, np.asarray(
        [3, 7, x0, y0, z1, 1, 2])))  # 4
    swc = np.vstack((swc, np.asarray(
        [4, 7, x0, y1, z0, 1, 7]))) # 1
    swc = np.vstack((swc, np.asarray(
        [5, 7, x1, y1, z0, 1, 4])))  # 2
    swc = np.vstack((swc, np.asarray(
        [6, 7, x1, y1, z1, 1, 5])))  # 3
    swc = np.vstack((swc, np.asarray(
        [7, 7, x0, y1, z1, 1, 6])))  # 4
    swc = np.vstack((swc, np.asarray(
        [8, 7, x1, y1, z0, 1, 1])))  # 2
    swc = np.vstack((swc, np.asarray(
        [9, 7, x0, y1, z0, 1, 0])))  # 1
    swc = np.vstack((swc, np.asarray(
        [10, 7, x1, y1, z1, 1, 2])))  # 3
    swc = np.vstack((swc, np.asarray(
        [11, 7, x0, y1, z1, 1, 3])))  # 4
    saveswc(f, swc)
def cropimg(cropx,cropy,origintif):
    #The savefile consists of cropx_cropy eg: 2_3.tif
    img=loadimg(origintif)
    print('img shape is: ' + str(img.shape))
    print('cropx is : ' + str(cropx) + ' cropy is : ' + str(cropy))
    savepath = origintif.split(".")[0] + "_"+str(cropx)+"_"+str(cropy)+"/"
    if os.path.exists(savepath):
        shutil.rmtree(savepath)
    os.makedirs(savepath)
    os.mkdir(savepath + "txt")
    locinfo=""
    locfile = open(savepath + "txt/"+"nameinfo.txt", "w")
    shapex,shapey,shapez=img.shape
    # if(shapex<cropx or shapey<cropy):
    #     smallswc(img,threshold,savepath+'.swc')

    # print(shapex,shapey,shapez)
    if shapey< cropy:
        print('shapey < cropy')
        for j in range(cropx,shapex,cropx):
            oneitem=img[j-cropx:j,:,:]
            
            loc="1_"+str(int(j/cropx))
            locinfo=locinfo+"\n"+loc
            writetiff3d(savepath+loc+".tif", oneitem)
            boundary(j - cropx, j-1, 0, shapey-1, 0,
                     shapez - 1, savepath + loc + "_boundary.swc")
        if (shapex % cropx != 0):
            linelast = img[shapex - shapex % cropx:shapex, :, :]
            loc = "1_" + str(int(shapex / cropx+1))
            locinfo = locinfo + "\n" + loc
            writetiff3d(savepath + loc +
                        ".tif", linelast)
            boundary(shapex - shapex % cropx, shapex-1, 0, shapey - 1, 0,
                     shapez - 1, savepath + loc + "_boundary.swc")
    if shapex<cropx:
        for i in range(cropy,shapey,cropy):
            columns=img[:,i-cropy:i,:]
            loc = str(int(i / cropy)) + "_1"
            locinfo = locinfo + "\n" + loc
            writetiff3d(savepath + loc + ".tif", columns)
            boundary(0, shapex - 1, i - cropy, i-1, 0,
                     shapez - 1, savepath + loc + "_boundary.swc")
        if(shapey%cropy !=0):
            lastone=img[:,shapey-shapey%cropy:shapey,:]
            loc = str(int(shapey / cropy+1)) + "_1"
            locinfo = locinfo + "\n" + loc
            writetiff3d(savepath + loc + ".tif", lastone)
            boundary(0, shapex - 1, shapey - shapey % cropy, shapey-1, 0,
                     shapez - 1, savepath + loc + "_boundary.swc")
    if (shapex>cropx and shapey>cropy):
        for i in range(cropy,shapey,cropy):
            #The output of every item which matches the size(cropx*cropy) perfectly.
            for j in range(cropx,shapex,cropx):
                oneitem=img[j-cropx:j,i-cropy:i,:]
                loc=str(int(i/cropy))+"_"+str(int(j/cropx))
                locinfo=locinfo+"\n"+loc
                writetiff3d(savepath+loc+".tif", oneitem)
                boundary(j - cropx, j-1, i - cropy, i-1, 0,
                         shapez - 1, savepath + loc + "_boundary.swc")
            #if shapex has a remainder (rx)of cropx, the item with the size(rx*cropy) appears at the end of a line.
            if(shapex%cropx!=0):
                linelast=img[shapex-shapex%cropx:shapex,i-cropy:i,:]
                loc=str(int(i/cropy)) +"_"+ str(int(j/cropx+1))
                locinfo=locinfo+"\n"+loc
                writetiff3d(savepath + loc +
                            ".tif", linelast)
                boundary(shapex - shapex % cropx, shapex-1, i - cropy, i-1, 0,
                         shapez - 1, savepath + loc + "_boundary.swc")
        # if cropy cannot be perfectly divided by shapey,then this remainder(ry) is the y coordinate of the last line
        if(shapey%cropy!=0):
            for k in range(cropx,shapex,cropx):
                lastline=img[k-cropx:k,shapey-shapey%cropy:shapey,:]
                loc=str(int(i/cropy+1)) + "_"+str(int(k/cropx))
                locinfo = locinfo+"\n"+loc
                writetiff3d(savepath + loc +
                            ".tif", lastline)
                boundary(k - cropx, k-1, shapey - shapey % cropy, shapey-1, 0,
                         shapez - 1, savepath + loc + "_boundary.swc")
        #if both shapex and shapey have their remainders(rx,ry),the lastone with size(rx*ry) is shown
        # print("lucky last one")
        if((shapey%cropy!=0)and(shapex%cropx!=0)):
            lastone=(img[shapex-shapex%cropx:shapex,shapey-shapey%cropy:shapey,:])
            loc=str(int(i/cropy+1)) +"_"+ str(int(j/cropx+1))
            locinfo = locinfo+"\n"+loc
            writetiff3d(savepath + loc
                        +".tif", lastone)
            boundary(shapex - shapex % cropx, shapex-1, shapey - shapey % cropy, shapey-1, 0,
                     shapez - 1, savepath + loc + "_boundary.swc")
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
    for ylocation in range(1, ymax + 1):
        # every same x in y direction combined
        liney = loadimg(directory + "/1_" + str(ylocation) + rest)
        for xlocation in range(2, xmax + 1):
            debris = loadimg(directory + "/" + str(xlocation) + "_" + str(ylocation) + rest)
            liney = np.concatenate((liney, debris), axis=1)
        #every x direction combined to get the final one part
        if (ylocation == 1):
            wholepart = liney
            # print(wholepart)
        else:
            wholepart = np.concatenate((wholepart, liney), axis=0)
    writetiff3d(directory + "/wholepart.tif",wholepart)

def combinedswc(path, path2):
    savepath = os.path.abspath(os.path.join(path, os.pardir))
    swcname=path.split('/')[-1]
    count = 0
    container = np.zeros(shape=(1, 7))#Initialize the default container
    for swc in glob.glob(os.path.join(path, '*.swc')):
        a = loadswc(swc)
        tswc = a.copy()
        
        tswc[:, 0] += count  # change the order
        tswc[:, -1] += count
        count = a.shape[0] + count + 2#The follow three lines are for checking errors

        if container[0, 2] == 0:
            container = tswc
        else:
            container = np.vstack((container, tswc))
    if path2:
        saveswc(savepath+'/'+path2, container)
    else:
        saveswc(savepath+'/'+swcname+'.swc', container)

def simplecombine(path):
    savepath = os.path.abspath(os.path.join(path, os.pardir))
    swcname = path.split('/')[-1]
    count = 0
    container = np.zeros(shape=(1, 7))  # Initialize the default container
    for swc in glob.glob(os.path.join(path, '*.swc')):
        a = loadswc(swc)
        tswc = a.copy()

        
        if container[0, 2] == 0:
            container = tswc
        else:
            container = np.vstack((container, tswc))
    saveswc(savepath + '/' + swcname + '.swc', container)
