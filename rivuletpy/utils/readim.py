from rivuletpy.utils.io import *
img=loadimg("1.tif")

def cropimg(cropx,cropy,img):
    z,y,x=img.shape
    print(z,y,x)
    #我们能取到多少个完整横边
    xpiece=int(x/cropx)
#x的每个边界在x轴上的坐标
    xedges=[0]
    a=0
    while a<xpiece:
        a=a+1
        xedges.append(a*cropx)
    print(xedges)
    #剩下的x多长
    xleave=x%cropx
    #我们能取到多少个完整纵边
    ypiece=int(y/cropy)
 #y的每个边界在y轴上的坐标
    yedges=[0]
    b=0
    while b<ypiece:
        b=b+1
        yedges.append(b*cropy)

    #剩下的y多长
    yleave=y%cropy
    i=0
    #每一横条的输出
    while i<len(yedges):
        i=i+1
        j=0
        #每一个的输出
        while j<len(xedges):
            j=j+1
            onewholepiece=img[3:4,yedges[i-1]:yedges[i],xedges[j-1]:xedges[j]]
            print(onewholepiece)
cropimg(2,2,img)
