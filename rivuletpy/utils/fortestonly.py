from rivuletpy.utils.io import *
import numpy as np
import os, math
inputpath="/home/vv/Desktop/new/1"
# img=loadimg(inputpath)
# import numpy as np
# stack = []
# sample1=np.arange(-1,-13,-1).reshape((3,4))
# sample2=np.arange(1,13).reshape((3,4))
# print(sample1)
# print(sample2)
# stack.append(np.rot90(np.fliplr(np.flipud(sample1))))
# print(stack)
# stack.append(np.rot90(np.fliplr(np.flipud(sample2))))
# print(stack)
# out = np.dstack(stack)
# print("out begins")
# print(out)

# def combined(directory):
#     combined[]=loadtiff3d(directory)
# a=str(math.ceil(9.3))
# print(a)

# print("xmax:"+str(xmax))
# ymax=ys[-1]
# for file in list:  # 遍历文件夹
#     if not os.path.isdir(file):
#         print(file)
# a=loadimg(inputpath+"/"+"1_1"+".tif")
# print(a)
# print(a.dtype)
# list = os.listdir(inputpath)# 得到文件夹下的所有文件名称
# coordilist=[]
# for l in list:
#     location = l.split(".")[0]
#     x = int(location.split("_")[0])
#     y = int(location.split("_")[1])
#     coordilist.append([x,y])
# coordilist.sort(key=lambda k: [k[0], k[1]])
# print(coordilist[-1])
list = os.listdir(directory) # dir is your directory path
xs=[]
ys=[]
for l in list:
    location=l.split(".")[0]
    x=location.split("_")[0]
    y=location.split("_")[1]
    xs.append(int(x))
    ys.append(int(y))
xs.sort()
ys.sort()
xmax=xs[-1]
ymax=ys[-1]
for ylocation in range(1,ymax+1):
    #every line combined
    line=loadimg(directory+"/1_"+str(ylocation)+".tif")
    for xlocation in range(2,xmax+1):
        debris=loadimg(directory+"/"+str(xlocation)+"_"+str(ylocation)+".tif")
        # print(str(xlocation)+"_"+str(ylocation),debris.shape)
        line=np.concatenate((line, debris), axis=1)
    if(ylocation==1):
        wholepart=line
        print(wholepart)
    else:
        wholepart=np.concatenate((wholepart,line),axis=0)
writetiff3d(directory+"/wholepart.tif",wholepart)

# kong=[[[]]]
# a=np.ones((2,3,2))
# c=np.concatenate((kong,a),axis=2)
# print(c)


