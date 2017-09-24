from rivuletpy.trace import *
from rivuletpy.swc import *
from rivuletpy.utils.io import *
def smallswc(origintif,threshold,savepath):
    img=loadimg(origintif)
    tracer = R2Tracer()
    swc, soma = tracer.trace(img, threshold)
    tswc = swc._data.copy()
    saveswc(savepath + '.swc', tswc)