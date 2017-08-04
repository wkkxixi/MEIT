from rivuletpy.utils.io import *
img=loadimg("1.tif")
def cropimg(cropx,cropy,img):
    z,y,x=img.shape
    print(z,y,x)
    for i in range(0,y,cropy):
        #每一横行的输出
        for j in range(cropx,x,cropx):
            print(img[3:4,i-cropy:i,j-cropx:j])
        #每一横行如果有剩的最后一个输出
        if(x%cropx!=0):
            print(img[3:4,i-cropy:i,x-x%cropx:x])
            print("one single line ended")
    #最后一行开始
    print("final line begins")
    if(y%cropy!=0):
        for k in range(cropx,x,cropx):
            print(img[3:4,y-y%cropy:y,k-cropx:k])
#行列均有剩的最后一个
    print("lucky last one")
    if((y%cropy!=0)and(x%cropx!=0)):
        print(img[3:4,y-y%cropy:y,x-x%cropx:x])
cropimg(20,20,img)
