#!python3
from filtering.anisotropic import * 
from rivuletpy.utils.io import * 
from rivuletpy.utils.preprocessing import crop
from scipy import io as sio
import skfmm
from skimage.morphology import skeletonize_3d
from rivuletpy.trace import trace
try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters


def recon(file, threshold, filter='bg', radii=np.arange(1,1.2,0.2)):
    print('Trying to read ', file)

    if file.endswith('.tif'):
        img = loadtiff3d(file)
    else:
        filecont = sio.loadmat(file)
        img = filecont['img']

    # Crop image
    img, cropregion = crop(img, threshold)

    if filter is not 'original':
        rps, _, _ = response(img.astype('float'), rsptype=filter,
                             radii=np.asarray(radii), rho=0.2, memory_save=False)
        img = rps > 1

    swc = trace(img, threshold=0, render=False, 
                length=4, ignore_radius=True,
                skedt=True, coverage=.99)
    toswcfile=''.join([file, '.swc'])

    # Pad swc according to the crop region
    swc[:, 2] += cropregion[0, 0]
    swc[:, 3] += cropregion[1, 0]
    swc[:, 4] += cropregion[2, 0]
    swc_x = swc[:, 2].copy()
    swc_y = swc[:, 3].copy()
    swc[:, 2] = swc_y
    swc[:, 3] = swc_x
    # if config['ignore_radius']:
    swc[:, 5] = 1
    saveswc(toswcfile, swc)
