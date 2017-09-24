from rivuletpy.utils.io import *
from rivuletpy.trace import *
import numpy as np
import os, math

# crop_region=np.shape()
# inputpath="/home/vv/Desktop/new/1"
# img=loadimg(inputpath)
# import numpy as np
# stack = []
# sample1=np.arange(-1,-17,-1).reshape(4,4)
# print(sample1)
# print(sample1[-1,-1])
# print(sample1[-1,-2])
# sample2=np.arange(1,37).reshape((3,4,3))
# bis = sample1 > 3
# y =x > 2
# z=y.astype(int)
# print("int",z)
#
# print(sample1[2,2,2])
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
# list = os.listdir(directory) # dir is your directory path
# xs=[]
# ys=[]
# for l in list:
#     location=l.split(".")[0]
#     x=location.split("_")[0]
#     y=location.split("_")[1]
#     xs.append(int(x))
#     ys.append(int(y))
# xs.sort()
# ys.sort()
# xmax=xs[-1]
# ymax=ys[-1]
# for ylocation in range(1,ymax+1):
#     #every line combined
#     line=loadimg(directory+"/1_"+str(ylocation)+".tif")
#     for xlocation in range(2,xmax+1):
#         debris=loadimg(directory+"/"+str(xlocation)+"_"+str(ylocation)+".tif")
#         # print(str(xlocation)+"_"+str(ylocation),debris.shape)
#         line=np.concatenate((line, debris), axis=1)
#     if(ylocation==1):
#         wholepart=line
#         print(wholepart)
#     else:
#         wholepart=np.concatenate((wholepart,line),axis=0)
# writetiff3d(directory+"/wholepart.tif",wholepart)
# kong=[[[]]]
# a=np.ones((2,3,2))
# c=np.concatenate((kong,a),axis=2)
# print(c)
# def ratio(threshold,darray):
#     x,y,z=darray.shape
#     binsum=(darray>threshold).sum()
#     ratio=binsum/(x*y*z)
# def am_i_wrong(answer):
#     if answer == 'yes':
#         return True
#     else:
#         return False
# a=am_i_wrong('yes')
# print(a)
# class getinfo:
#     def __init__(self,name,thresholdt,pctg,crop_region=None,bi_matrix=None,thresholdbi=None,swc=None):
#         self.name=name
#         self.matrix_3d=None
#         self.pctg=pctg
#         self.bi_ratio=0
#         self.bi_matrix=None
#         self.threshodbi=0
#         self.thresholdt=thresholdt
#         self.tracelabel=False
#         self.swc = None
#     def get3d_mat(self):
#         self.matrix_3d=loadimg('/home/vv/Desktop/new/1/'+self.name+'.tif')
#         return self.matrix_3d
#     def cellsatisfied(self):
#         oneitem=loadimg('/home/vv/Desktop/new/1/'+self.name+'.tif')
#         self.bi_matrix=(oneitem>self.thresholdt).astype(int)
#         self.bi_ratio=float((oneitem > self.thresholdt).sum()/(oneitem.shape[0]*oneitem.shape[1]*oneitem.shape[2]))
#         return self.thresholdt, self.bi_matrix, self.bi_ratio
#     def traceornot(self):
#         if self.bi_ratio>self.pctg:
#             self.tracelabel=True
#         return self.tracelabel
#     def gettrace(self):
#         if self.tracelabel:
#             # Run rivulet2 for the first time
#             tracer = R2Tracer()
#             self.swc, soma = tracer.trace(self.matrix_3d, self.thresholdt)
#
#             tswc=self.swc._data.copy()
#             # print(self.swc._data.shape)
#             tswc[:, 2] += self.cropy  以2_3举例，横坐标加上cropx×截取的y-1（3），纵坐标加上cropy×截取的x-1(2）
#             tswc[:, 3] +=
#             self.swc._data = tswc
#             self.swc.save('/home/vv/Desktop/new/1/'+self.name+'.swc')
#         return self.swc._data
#     # def doall(self):
#
#
#
#
#
#
#
# xxx = getinfo('1_1_40_50',10,0.000000005)
# print(xxx.get3d_mat())
# print(xxx.cellsatisfied())
# print(xxx.traceornot())
# print(xxx.pctg,xxx.bi_ratio)
# print(xxx.gettrace())


# def reset(self, crop_region, zoom_factor):
#     '''
#     Pad and rescale swc back to the original space
#     '''
#
#     tswc = self._data.copy()
#     if zoom_factor != 1.:  # Pad the swc back to original space
#         tswc[:, 2:5] *= 1. / zoom_factor
#
#     # Pad the swc back
#     tswc[:, 2] += crop_region[0, 0]
#     tswc[:, 3] += crop_region[1, 0]
#     tswc[:, 4] += crop_region[2, 0]
#     self._data = tswc
# a=loadswc('/home/vv/Desktop/new/1.r2.swc')
# b=loadswc('/home/vv/Desktop/new/1/1_1.swc')
# print(a.shape)
# # print(a[1333,0:5]) 从1333开始出现断点,把所有小的swc文件拼合在一起数量大于大文件的行数
# print(b.shape)
# # print(b[44:66,2:5])

# all = os.listdir('/home/vv/Desktop/new/1_100_90')
# for a in all:
#     if "_" in a:
#         print(a)
# print(all)

# file=open('/home/vv/Desktop/new/1_100_90/txt/100_90.txt','r')
# for line in file:
#     if "_" in line:
#         print(line)
#0818 this version is for fileinfo first version
# from rivuletpy.utils.io import *
# import os, glob
# inputpath="/home/vv/Desktop/new/1.tif"
# img=loadimg(inputpath)
# dirpath=inputpath.split(".")[0]
#
#
# def cropimg(cropx,cropy,threshold,img):
#     #The savefile consists of cropx_cropy eg: 2_3.tif
#     savepath = dirpath + "_"+str(cropx)+"_"+str(cropy)+"/"
#     os.mkdir(savepath)
#     os.mkdir(savepath + "txt")
#     locinfo=""
#     locfile = open(savepath + "txt/"+str(cropx)+"_"+str(cropy)+".txt", "w")
#     x,y,z=img.shape
#     # print(x,y,z)
#     for i in range(cropy,y,cropy):
#         #The output of every line
#         for j in range(cropx,x,cropx):
#             oneitem=img[j-cropx:j,i-cropy:i,:]
#             loc=str(int(i/cropy))+"_"+str(int(j/cropx))
#             locinfo=locinfo+"\n"+loc
#             writetiff3d(savepath+loc+".tif", oneitem)
#         #if there is one left at the end of the line, here it is
#         if(x%cropx!=0):
#             linelast=img[x-x%cropx:x,i-cropy:i,:]
#             loc=str(int(i/cropy)) +"_"+ str(int(j/cropx+1))
#             locinfo=locinfo+"\n"+loc
#             writetiff3d(savepath + loc +
#                         ".tif", linelast)
#     # print("final line begins")
#     if(y%cropy!=0):
#         for k in range(cropx,x,cropx):
#             lastline=img[k-cropx:k,y-y%cropy:y,:]
#             loc=str(int(i/cropy+1)) + "_"+str(int(k/cropx))
#             locinfo = locinfo+"\n"+loc
#             writetiff3d(savepath + loc +
#                         ".tif", lastline)
#     #行列均有剩的最后一个
#     # print("lucky last one")
#     if((y%cropy!=0)and(x%cropx!=0)):
#         lastone=(img[x-x%cropx:x,y-y%cropy:y,:])
#         loc=str(int(i/cropy+1)) +"_"+ str(int(j/cropx+1))
#         locinfo = locinfo+"\n"+loc
#         writetiff3d(savepath + loc
#                     +".tif", lastone)
#     locfile.write(locinfo)
#     locfile.close()
#
# def combined(directory):
#     file = open(directory+"/txt/", 'r')
#     for line in file:
#         if "_" in line:
#             line = line.split('\n')[0]
#     xmax=int(line.split('_')[0])
#     ymax=int(line.split('_')[1])
#     rest=".tif"
#
#     for ylocation in range(1, ymax + 1):
#         # every same x in y direction combined
#         liney = loadimg(directory + "/1_" + str(ylocation) + rest)
#         for xlocation in range(2, xmax + 1):
#             debris = loadimg(directory + "/" + str(xlocation) + "_" + str(ylocation) + rest)
#             liney = np.concatenate((liney, debris), axis=1)
#         #every x direction combined to get the final one part
#         if (ylocation == 1):
#             wholepart = liney
#             print(wholepart)
#         else:
#             wholepart = np.concatenate((wholepart, liney), axis=0)
#     writetiff3d(directory + "/wholepart.tif",wholepart)
# cropimg(100,90,10,img)
# combined("/home/vv/Desktop/new/1_100_90")
# import glob
# for swc in glob.glob(os.path.join("/home/vv/Desktop/new/1_80_70", '*.swc')):
#     a=loadswc(swc)
#     print(a.shape)
# # int(''.split("_")[-2])
# a=loadswc("/home/vv/Desktop/new/1_80_70/1_1.swc")
# counta=a.shape[0]
# b=loadswc("/home/vv/Desktop/new/1_80_70/6_3.swc")
# b[:, 0] += counta  # change the order
# b[1:, -1] += counta
# saveswc('/home/vv/Desktop/1_1.swc',a)
# saveswc('/home/vv/Desktop/6_3.swc',b)
# print(min(a[:,0]),max(a[:,0]))
# print(min(a[1:,-1]),max(a[1:,-1]))
# print(min(b[:,0]),max(b[:,0]))
# print(min(b[1:,-1]),max(b[1:,-1]))
# c=np.vstack((a,b))
# np.full()
# path='/home/vv/Desktop/1_1-6_3.swc'
# print(os.path.join(path, os.pardir))
# savepath=os.path.abspath(os.path.join(path, os.pardir))
# from numpy import *
# import numpy
# sample1=np.arange(-1,-5,-1).reshape(1,4)
# sample2=np.arange(1,5,1).reshape(4,1)
# sample3=np.arange(1,5,1).reshape(1,4)
# print((sample1*sample3).sum())
# a1=mat(sample1);
# a2=mat(sample2);
# a3=a1*a2;
# print(a3)
# import threading
# def thread_job():
#     print('THis is an added Thread, number is %s' % threading.current_thread())
# def main():
#     add_thread=threading.Thread(target=thread_job)
#
#
#     add_thread.start()
#     print(threading.active_count())
#     print(threading.enumerate())
#     print(threading.current_thread())
# if __name__=='__main__':
#     main()
# from rivuletpy.utils.cropswc import *
# import threading
# from queue import Queue
# def job(l,q):
#     for i in range(len(l)):
#         for j in range(100000000):
#             l[i]=l[i]+2
#     q.put(l)
#
# def multithreading():
#     q=Queue()
#     threads=[]
#     data=[[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
#     for i in range(4):
#         t=threading.Thread(target=getinfo,args=(data[i],q))
#         t.start()
#         threads.append(t)
#     for thread in threads:
#         thread.join()
#     results=[]
#     for _ in range(4):
#         results.append(q.get())
#     print(results)
# if __name__=='__main__':
#     multithreading()
# import json
# import operator
# from collections import defaultdict
# import multiprocessing as mp
# from pprint import pprint
# from rivuletpy.utils.io import *
# jsonfilepath='/home/rong/Documents/Gold166-JSON/'
# # os.mkdir(jsonfilepath + "jsoninfo")
# container='filename\tthreshold\tdimx\tdimy\tdimz\tsize(x*y*z)'
# d=defaultdict(int)
# list = os.listdir(jsonfilepath)
# def readtif(l):
#     if l.split(".")[-1]=='json':
#         if l.split(".")[-2]!='pp':
#             print(file)
#             with open(jsonfilepath+l) as data_file:
#                 data = json.load(data_file)
#             Keys=data['data'].keys()
#             for Key in Keys:
#                 keys=data['data'][Key].keys()
#             for key in keys:
#                 filename=data['data'][Key][key]['imagepath']
#                 threshold=data['data'][Key][key]['misc']['threshold']
#                 # print(jsonfilepath+filename)
#                 img = loadimg(jsonfilepath+filename)
#                 x,y,z=img.shape
#                 print(img.shape)
#                 d[filename+'\t'+str(threshold)+'\t'+str(x)+'\t'+str(y)+'\t'+str(z)]=x*y*z
# # pool=mp.Pool(5)
# # for file in list:
# #     pool.apply_async(readtif, file)
# # pool.close()
# # pool.join()
# p=mp.Pool(5)
# for file in list:
#     p.apply_async(readtif,file)
# p.close()
# p.join()
# for item in sorted(d,key=d.get,reverse=True):
#     container=container+'\n'+item+"\t"+str(d[item])
# outputfile = open(jsonfilepath + "jsoninfo/"+"detailedinfo.txt", "w")
# print(container)
# outputfile.write(container)
# outputfile.close()
from rivuletpy.utils.io import *
# from rivuletpy.utils.folderinfo import *
# from rivuletpy.utils.cropswc import *
# import multiprocessing as mp
# import time
# folderpath='/home/rong/Documents/Gold166-JSON/'
#
# with open(folderpath+'jsoninfo/detailedinfo.txt') as f:
#     lines = f.readlines()
#     for item in lines:
#         if item.__contains__('.'):
#             print(item)
#             filename=item.split('\t')[0]
#             threshold=item.split('\t')[1]
#             origintif=folderpath+filename
#             cropx=100
#             cropy=100
#             thresholdt=int(threshold)
#             percentage=0.00005
#             folder=origintif.split('.')[0]+'_'+str(cropx)+'_'+str(cropy)
#             cropimg(cropx,cropy,origintif)
#             # combined(folder)
#
#             file = open(folder+"/txt/"+"nameinfo.txt", 'r')
#
#
#             def operationcombine(folder, line, thresholdt, percentage):
#                 if "_" in line:
#                     # print(line, "is on processing")
#                     line = line.split('\n')[0]
#                     line = getinfo(folder, line, thresholdt, percentage)
#                     line.get3d_mat()
#                     line.tsatisfied()
#                     line.traceornot()
#                     line.gettrace()
#             begin_time=time.time()
#             pool=mp.Pool()
#             for line in file:
#                 pool.apply_async(operationcombine, args=(folder, line, thresholdt, percentage))
#             pool.close()
#             pool.join()
#             end_time=time.time()
#             print(end_time-begin_time)
#             print('small swcs are being combined')
#             combinedswc(folder)
#             print('combined successfully!')
from collections import deque
import numpy as np
from scipy.spatial.distance import cdist
from rivuletpy.utils.io import *


# from rivuletpy.utils.metrics import *
from collections import deque
import numpy as np
from scipy.spatial.distance import cdist
from rivuletpy.utils.io import *
from os.path import join
import csv
from glob import glob
datapath='/home/rong/Documents/Gold166-JSON/zebrafishlarveRGC/'
swc1=loadswc(datapath+'1.swc')
swc2=loadswc(datapath+'1_100_100_sorted.swc')
def upsample_swc(swc):

    tswc = swc.copy()

    id_idx = {}
    # Build a nodeid->idx hash table
    for nodeidx in range(tswc.shape[0]):
        id_idx[tswc[nodeidx, 0]] = nodeidx

    newid = tswc[:,0].max() + 1
    newnodes = []
    for nodeidx in range(tswc.shape[0]):
        pid = tswc[nodeidx, -1] # parent id

        if pid not in id_idx:
            # raise Exception('Parent with id %d not found' % pid)
            continue

        nodepos = tswc[nodeidx, 2:5]
        parentpos = tswc[id_idx[pid], 2:5]

        if np.linalg.norm(nodepos - parentpos) > 1.: # Add a node in the middle if too far
            mid_pos = nodepos + 0.5 * (parentpos - nodepos)
            newnodes.append( np.asarray([newid, 2, mid_pos[0], mid_pos[1], mid_pos[2], 1, pid]) )
            newid += 1
            tswc[nodeidx, -1] = newid

    # Stack the new nodes to the end of the swc file
    newnodes = np.vstack(newnodes)
    tswc = np.vstack((tswc, newnodes))
    return tswc
def connectivity_distance(swc1, swc2, sigma=2., ignore_leaf=True):
    '''
    The connectivity metrics of NetMets.
    Returns (midx1, midx2): the indices of nodes in each swc that have connection errors

    D. Mayerich, C. Bjornsson, J. Taylor, and B. Roysam,
    “NetMets: software for quantifying and visualizing errors in biological network segmentation.,”
    BMC Bioinformatics, vol. 13 Suppl 8, no. Suppl 8, p. S7, 2012.
    '''

    # graph Initialisation
    d = cdist(swc1[:, 2:5], swc2[:, 2:5]) # Pairwise distances between 2 swc files
    mindist1, mindist2 = d.min(axis=1), d.min(axis=0)
    minidx1, minidx2 = d.argmin(axis=1), d.argmin(axis=0)

    # Colour nodes - matched nodes have the same colour
    cnodes1, cnodes2 = {}, {}# Coloured Nodes <id, colour>
    for i in range(swc1.shape[0]):
        if mindist1[i] < sigma:
            cnodes1[swc1[i, 0]] = i
            cnodes2[swc2[minidx1[i], 0]] = i

    # Build Initial graphs, Edge: <id_i, id_j>: 1
    g1 = build_graph_from_swc(swc1)
    g2 = build_graph_from_swc(swc2)

    # BFS to build the core graph for both swc, returns the remaining edges not used to build the core graph
    dg1 = build_core_graph(g1, cnodes1)
    dg2 = build_core_graph(g2, cnodes2)

    # Find the diff edges with coloured nodes involved
    mid1 = set()
    for id in dg1:
        for nid in g1[id]:
            if nid in cnodes1: mid1.add(nid)

    mid2 = set()
    for id in dg2:
        for nid in g2[id]:
            if nid in cnodes2: mid2.add(nid)

    id_idx_hash1 = {}
    for i in range(swc1.shape[0]): id_idx_hash1[swc1[i, 0]] = i

    id_idx_hash2 = {}
    for i in range(swc2.shape[0]): id_idx_hash2[swc2[i, 0]] = i

    midx1 = [ int(id_idx_hash1[id]) for id in mid1 ] # Mistake coloured nodes in edges of dg1
    midx2 = [ int(id_idx_hash2[id]) for id in mid2 ] # Mistake coloured nodes in edges of dg2

    # Filter out the midx of nodes on leaf segments
    if ignore_leaf:
        leafidx1 = find_leaf_idx(swc1)
        midx1 = set(midx1) - set(leafidx1)
        leafidx2 = find_leaf_idx(swc2)
        midx2 = set(midx2) - set(leafidx2)

    return midx1, midx2
def find_leaf_idx(swc):
    # The degree of a node is the number of children + 1 except the root
    degree  = np.zeros(swc.shape[0])
    for i  in range(swc.shape[0]):
        degree[i] = np.count_nonzero(swc[:, -1] == swc[i, 0]) + 1

    # A node is a leaf node if it is parent to no other node
    leaf_segment_idx = []
    leaf_node_idx = np.where(degree == 1)[0]
    for idx in leaf_node_idx:
        # Add its parent to the leaf segment idx list if its parent degree < 3
        nodeidx = idx
        while degree[nodeidx] < 3:
            leaf_segment_idx.append(int(nodeidx))
            if swc[nodeidx, -1] < 0:
                break
            nodeidx = np.where(swc[:, 0] == swc[nodeidx, -1])[0]

    return leaf_segment_idx


def build_graph_from_swc(swc):
    g = {}
    for i in range(swc.shape[0]):
        id, pid = swc[i, 0], swc[i, -1]

        if id in g:
            g[id].append(pid)
        else:
            g[id] = [pid]

        if pid in g:
            g[pid].append(id)
        else:
            g[pid] = [id]

    for key, value in g.items():
        g[key] = set(value)

    return g
def build_core_graph(g, cnodes):
    '''
    Returns the edges not used in building the core graph (topologically matched between two graphs)
    '''

    cnodes = cnodes.copy() # Coloured node list to mark which have not been discovered
    dg = g.copy()

    while cnodes:
        root = next(iter(cnodes))
        core_neighbours = find_core_neighbours_bfs(dg, root, cnodes)  # BFS to discover the neighbour

        nodes_on_path = set()
        if  core_neighbours:
            for id in core_neighbours:
                nodes_on_path = nodes_on_path.union(track_path_nodes_dijstra(dg, id, root))
        else:
            nodes_on_path.add(root)

        cnodes.pop(root) # Remove the discovered coloured nodes
        for n in nodes_on_path:
            dg.pop(n, None)

        for n in dg:
            dg[n] = dg[n].difference(nodes_on_path)

    return dg


def find_core_neighbours_bfs(g, root, cnodes):
    '''
    Find the coloured neighbours of root node with BFS search
    '''

    visited = {}
    node_queue = deque()
    visited[root] = True
    node_queue.append(root)
    core_neighbours = []

    while node_queue:
        r = node_queue.popleft()

        if r in cnodes and r != root:
            core_neighbours.append(r) # If this node is coloured, bfs stops on it and add it to the core neighbours
        else:
            for n in g[r]: # visit all the neighbours of r
                if n not in visited:
                    visited[n] = True
                    node_queue.append(n)

    return core_neighbours


def track_path_nodes_dijstra(g, target, source):
    path = {}
    visited = {source: 0}
    nodes = g.copy()

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.pop(min_node)
        tweight = visited[min_node]
        for n in g[min_node]:
            weight = tweight + 1
            if n not in visited or weight < visited[n]:
                visited[n] = weight
                path[n]  = min_node

        if min_node == target:
            break

    nodes_on_path, n = set(), target
    while n != source:
        n = path[n]
        nodes_on_path.add(n)

    return nodes_on_path

def gaussian_distance(swc1, swc2, sigma=2.):
    '''
    The geometric metrics of NetMets. The gaussian distances between the closest neighbours
    returns : (M1, M2) where M1 is the gaussian distances from the nodes in swc1 to their closest neighbour in swc2;
    vise versa for M2

    D. Mayerich, C. Bjornsson, J. Taylor, and B. Roysam,
    “NetMets: software for quantifying and visualizing errors in biological network segmentation.,”
    BMC Bioinformatics, vol. 13 Suppl 8, no. Suppl 8, p. S7, 2012.
    '''
    swc1 = upsample_swc(swc1)
    swc2 = upsample_swc(swc2)
    swc1lines = swc1.shape[0]
    swc2lines = swc2.shape[0]
    mindist1list = []
    mindist2list = []
    for line in range(swc1lines):
        d = cdist(swc1[line:line + 1, 2:5], swc2[:, 2:5])
        smindist1 = d.min(axis=1)
        mindist1list.append(smindist1)
    for line2 in range(swc2lines):
        d2 = cdist(swc1[:, 2:5], swc2[line2:line2 + 1, 2:5])
        smindist2 = d2.min(axis=0)
        mindist2list.append(smindist2)
    mindist1s = np.array(mindist1list)  # no squeeze numpy
    mindist2s = np.array(mindist2list)  # no squeeze numpy
    mindist1 = np.squeeze(mindist1s)
    mindist2 = np.squeeze(mindist2s)
    M1 = 1 - np.exp(mindist1 ** 2  / (2 * sigma ** 2))
    M2 = 1 - np.exp(mindist2 ** 2  / (2 * sigma ** 2))
    return M1, M2

# M1, M2 = gaussian_distance(swc1, swc2, 3.0)
# print('M1 MEAN: %.2f\tM2 MEAN: %.2f' % (M1.mean(), M2.mean()))
midx1, midx2 = connectivity_distance(swc1, swc2)
print(midx1,midx2)
# for i in midx1:
#     swc1[i, 1] = 2
#     swc1[i, 5] = 4

