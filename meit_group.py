from rivuletpy.utils.io import *
from rivuletpy.utils.folderinfo import *
from rivuletpy.utils.readjson import *
import multiprocessing as mp
import time
from pathlib import Path
import traceback
from scipy.ndimage.interpolation import zoom
import argparse


parser = argparse.ArgumentParser(description='Arguments to perform the MEIT tracing algorithm on a group of images.')
parser.add_argument(
        '--dataset',
        type=str,
        default=None,
        required=True,
        help='The absolute path of the dataset on processing. All images are categorised by species.')
parser.add_argument(
        '-cx',
        '--cropx',
        type=float,
        default=100,
        help='The cropping parameter cropx to crop the image. Default 100')
parser.add_argument(
        '-cy',
        '--cropy',
        type=float,
        default=100,
        help='The cropping parameter cropy to crop the image. Default 100')
parser.add_argument(
        '-z',
        '--zoom_factor',
        type=float,
        default=0.25,
        help='The factor to zoom the image to speed up the whole thing. Default 0.25')
parser.add_argument(
        '-b',
        '--boundary',
        action="store_true",
        help='Construct boundary around each block')

parser.add_argument('--clean', dest='clean', action='store_true',
    help="Remove the unconnected segments. It is relatively safe to do with the Rivulet2 algorithm")
parser.add_argument('--no-clean', dest='clean', action='store_false',
    help="Keep the unconnected segments (default)")
parser.set_defaults(clean=False)

# Arguments for soma detection
parser.add_argument('--save-soma', dest='save_soma', action='store_true',
    help="Save the automatically reconstructed soma volume along with the SWC.")
parser.add_argument('--no-save-soma', dest='save_soma', action='store_false',
    help="Don't save the automatically reconstructed soma volume along with the SWC (default)")
parser.set_defaults(save_soma=False)

parser.add_argument('--soma', dest='soma_detection', action='store_true',
    help="Use the morphological operator based soma detection")
parser.add_argument('--no-soma', dest='soma_detection', action='store_false',
    help="Don't use the morphological operator based soma detection (default)")
parser.set_defaults(soma_detection=False)
# Args for tracing
parser.add_argument(
    '--speed',
    type=str,
    default='dt',
    help='The type of speed image to use (dt, ssm). dt(default) would work for most of the cases. ssm provides slightly better curves with extra computing time')

parser.add_argument('--quality', dest='quality', action='store_true',
    help="Reconstruct the neuron with higher quality and slightly more computing time")
parser.add_argument('--no-quality', dest='quality', action='store_false',
    help="Reconstruct the neuron with lower quality and slightly more computing time (default)")
parser.set_defaults(quality=False)
# MISC
parser.add_argument('--silent', dest='silent', action='store_true', help="Omit the terminal outputs")
parser.add_argument('--no-silent', dest='silent', action='store_false', help="Show the terminal outputs & the nice logo (default)")
parser.set_defaults(silent=False)
args = parser.parse_args()

def boundary_constructor(x0, x1, y0, y1, z0, z1, f):

    swc_stack = np.zeros((1, 7))
    # upwards
    swc_stack[0, :] = np.asarray(
        [0, 7, x0, y0, z0, 1, 3])  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [1, 7, x1, y0, z0, 1, 0])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [2, 7, x1, y0, z1, 1, 1])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [3, 7, x0, y0, z1, 1, 2])))  
    # downwards
    swc_stack = np.vstack((swc_stack, np.asarray(
        [4, 7, x0, y1, z0, 1, 7])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [5, 7, x1, y1, z0, 1, 4])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [6, 7, x1, y1, z1, 1, 5])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [7, 7, x0, y1, z1, 1, 6]))) 
    # outwards 
    swc_stack = np.vstack((swc_stack, np.asarray(
        [8, 7, x1, y1, z0, 1, 1])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [9, 7, x0, y1, z0, 1, 0])))  
    # inwards
    swc_stack = np.vstack((swc_stack, np.asarray(
        [10, 7, x1, y1, z1, 1, 2])))  
    swc_stack = np.vstack((swc_stack, np.asarray(
        [11, 7, x0, y1, z1, 1, 3])))  
    saveswc(f, swc_stack)
folderpath = args.dataset + '/' if args.dataset[-1] != '/' else args.dataset
readtif(folderpath)  # read json files to get location information
index = 0
with open(folderpath + 'jsoninfo/detailedinfo.txt') as f:
    lines = f.readlines()  # read every line
    for item in lines:
        if item.__contains__('.'):  # escape the first line and recognize the path
            filename = item.split('\t')[0]
            threshold = int(item.split('\t')[1])
            if not args.silent:
                print(str(index) + ': ' + filename + ' is on processing.')
            index += 1

            shapex = int(item.split('\t')[2])
            shapey = int(item.split('\t')[3])
            shapez = int(item.split('\t')[4])
            sizexyz = int(item.split('\t')[5])
            cropx = args.cropx
            cropy = args.cropy

            origintif = folderpath + filename

            zoom_factor = args.zoom_factor  # minimize the original image to detect soma
            directory = folderpath + \
                filename.split('.')[0] + '_' + str(cropx) + '_' + \
                str(cropy) + '_' + str(zoom_factor) + '_MEIT'

            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                continue
            if args.boundary:
                if not os.path.exists(directory + '_boundary/'):
                    os.makedirs(directory + '_boundary/')
            
            img = loadimg(origintif)
            if not args.silent:
                print('original img shape is: ' + str(img.shape))
            if not args.silent:
                print('------step 1: Initial Soma Detecting-------')
            zoomed_img = zoom(img, zoom_factor) # minimize the original image to detect soma
            bimg = (zoomed_img > threshold).astype('int')  # Segment image
            soma = Soma()
            soma.detect(bimg, simple=True, silent=False)
            for i in range(0, 3):
                soma.centroid[i] = min((soma.centroid[i] + 1) /
                           zoom_factor - 1, img.shape[i] - 1)
            centroid = soma.centroid
            # Define Soma area (maximum: cropx*cropy)
            subx_min = max(centroid[0] - cropx / 2, 0)
            subx_max = min(centroid[0] + cropx / 2, img.shape[0])
            suby_min = max(centroid[1] - cropy / 2, 0)
            suby_max = min(centroid[1] + cropy / 2, img.shape[1])
            soma_area = np.asarray([subx_min, subx_max, suby_min, suby_max])
            centroid_in_subarea = np.asarray(
                [centroid[0] - subx_min, centroid[1] - suby_min, centroid[2]])
            q = [Tip(0, soma_area, soma.radius, centroid_in_subarea)] # Set tvalue for soma to be 0
            index = 0
            total = 1
            tracer = R2Tracer(quality=args.quality, silent=args.silent, speed=args.speed, clean=args.clean, img=img, cropx=cropx, cropy=cropy, threshold=threshold)
            if not args.silent:
                print('-------step 2: Large-scale Neuron Reconstruction')
            while index < total:
                tip = q[0]
                index += 1
                q = q[1:]
                swc, tips = tracer.trace(tip)
                if swc is None:
                    continue
                swc.save(directory + '/' + str(index) + '.swc')
                if len(tips) == 0:
                    continue
                # Construct boundary frame for this block which has boundary tips 
                if args.boundary:
                    boundary_constructor(tip.xmin(), tip.xmax() - 1, tip.ymin(), tip.ymax() - 1, 0,
                                        img.shape[2] - 1, directory + '_boundary/'  + str(index) + '_boundary' + '.swc')
                    
                for tip in tips:
                    if tip.xyz() is None:
                        continue
                    q.append(tip)
                    total += 1
                q.sort(key=lambda x: x._tvalue, reverse=False)

            if not args.silent:
                print('small swcs are being combined')
            combinedswc(directory, None)
            if not args.silent:
                print('combined successfully!')
                    
