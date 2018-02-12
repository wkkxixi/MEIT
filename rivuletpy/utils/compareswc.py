from collections import deque
import numpy as np
from scipy.spatial.distance import cdist
from io import *
from os.path import join
import csv
from glob import glob

def precision_recall(swc1, swc2, dist1=4, dist2=4):
    '''
    Calculate the precision, recall and F1 score between swc1 and swc2 (ground truth)
    It generates a new swc file with node types indicating the agreement between two input swc files
    In the output swc file: node type - 1. the node is in both swc1 agree with swc2
                                                        - 2. the node is in swc1, not in swc2 (over-traced)
                                                        - 3. the node is in swc2, not in swc1 (under-traced)
    target: The swc from the tracing method
    gt: The swc from the ground truth
    dist1: The distance to consider for precision
    dist2: The distance to consider for recall
    '''

    TPCOLOUR, FPCOLOUR, FNCOLOUR  = 3, 2, 180 # COLOUR is the SWC node type defined for visualising in V3D
    swc1lines=swc1.shape[0]
    swc2lines=swc2.shape[0]
    mindist1list=[]
    mindist2list=[]
    for line in range(swc1lines):
        d = cdist(swc1[line:line+1, 2:5], swc2[:, 2:5])
        smindist1 = d.min(axis=1)
        mindist1list.append(smindist1)
    for line2 in range(swc2lines):
        d2=cdist(swc1[:, 2:5], swc2[line2:line2+1, 2:5])
        smindist2 = d2.min(axis=0)
        mindist2list.append(smindist2)
    mindist1s=np.array(mindist1list)#no squeeze numpy
    mindist2s=np.array(mindist2list)#no squeeze numpy
    mindist1=np.squeeze(mindist1s)
    mindist2=np.squeeze(mindist2s)
    tp = (mindist1 < dist1).sum() # number of points similar to ground truth
    fp = swc1.shape[0] - tp
    fn = (mindist2 > dist2).sum()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)

    # Make the swc for visual comparison
    swc1[mindist1 <= dist1, 1] = TPCOLOUR
    swc1[mindist1 > dist1, 1] = FPCOLOUR
    swc2_fn = swc2[mindist2 > dist2, :]
    swc2_fn[:, 0] = swc2_fn[:, 0] + 100000
    swc2_fn[:, -1] = swc2_fn[:, -1] + 100000
    swc2_fn[:, 1] = FNCOLOUR
    swc_compare = np.vstack((swc1, swc2_fn))
    swc_compare[:, -2]  = 1

    return (precision, recall, f1), swc_compare