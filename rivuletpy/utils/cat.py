
import numpy as np
import os
import fnmatch
import multiprocessing as mp

def loadimg(file):
    if file.endswith('.mat'):
        filecont = sio.loadmat(file)
        img = filecont['img']
        for z in range(img.shape[-1]): # Flip the image upside down
            img[:,:,z] = np.flipud(img[:,:,z])
        img = np.swapaxes(img, 0, 1)
    elif file.endswith('.tif'):
        img = loadtiff3d(file)
    elif file.endswith('.nii') or file.endswith('.nii.gz'):
        import nibabel as nib
        img = nib.load(file)
        img = img.get_data()
    else:
        raise IOError("The extension of " + file + 'is not supported. File extension supported are: *.tif, *.mat, *.nii')

    return img

def loadtiff3d(filepath):
    """Load a tiff file into 3D numpy array"""
    # from libtiff import TIFF
    # tiff = TIFF.open(filepath, mode='r')

    import tifffile as tiff
    a = tiff.imread(filepath)

    stack = []
    for sample in a:
        stack.append(np.rot90(np.fliplr(np.flipud(sample))))
    out = np.dstack(stack)
    #a.close()

    return out

def writetiff3d(filepath, block):
    # from libtiff import TIFF
    import tifffile as tiff
    try:
        os.remove(filepath)
    except OSError:
        pass
    # tiff = TIFF.open(filepath, mode='w')
    # block = np.swapaxes(block, 0, 1)
    with tiff.TiffWriter(filepath, bigtiff=False) as tif:
        for z in range(block.shape[2]):
            # tif.save(np.flipud(block[:,:,z]), compress = 0)
            tif.save((np.rot90(block[:, :, z])), compress=0)
    # for z in range(block.shape[2]):
    #     tiff.write_image(np.flipud(block[:, :, z]), compression=None)
    # tiff.close()

'''
img = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/409600/1_2_3_combine.tif')
img = img[:,212:213,:]
print(str(img.shape))
writetiff3d('/Volumes/dh/heng_wang/RES(853x537x153)/409600/ymax_piece.tif', img)
'''


'''
with open('/Volumes/dh/heng_wang/RES(853x537x153)/409600/info.txt', 'a') as f:
    img1 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/409600/409600_000000/409600_000000_000000.tif')
    f.write(str(img1.shape) + '\n')
    img2 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/409600/409600_114560/409600_114560_000000.tif')
    f.write(str(img2.shape) + '\n')
    img3 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/409600/409600_229120/409600_229120_000000.tif')
    f.write(str(img3.shape) + '\n')
    f.write('------' + '\n')
    img1 = np.vstack((img1, img2)) 
    img1 = np.vstack((img1, img3)) 
    f.write(str(img1.shape) + '\n')

    # print(str(img1.shape))
    writetiff3d('/Volumes/dh/heng_wang/RES(853x537x153)/409600/1_2_3_combine.tif', img1)
'''

'''

with open('/Volumes/dh/heng_wang/RES(853x537x153)/info.txt', 'a') as f:
    f.write('second try: append from block 3')
    img1 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/000000/1_2_3_combine.tif')
    f.write(str(img1.shape) + '\n')
    img2 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/136960/1_2_3_combine.tif')
    f.write(str(img2.shape) + '\n')
    img3 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/273280/1_2_3_combine.tif')
    f.write(str(img3.shape) + '\n')
    img4 = loadimg('/Volumes/dh/heng_wang/RES(853x537x153)/409600/1_2_3_combine.tif')
    f.write(str(img4.shape) + '\n')
    f.write('------' + '\n')

    img4 = np.append(img4,img3,axis=1)
    img4 = np.append(img4,img2,axis=1)
    img4 = np.append(img4,img1,axis=1)
    f.write(str(img1.shape) + '\n')

    # print(str(img1.shape))
    writetiff3d('/Volumes/dh/heng_wang/RES(853x537x153)/0_1_2_3_combine.tif', img4)

'''
'''
def cropz_worker(folder, y, x):
    crop_z = os.listdir(folder+y+'/'+x)
    img_z = None
    
    with open(folder+y+'/'+x+'/' + x + '_info.txt', 'w') as f:
        for z in crop_z:
            if not (fnmatch.fnmatch(z, '*.tif') and len(z) == 24):
                continue
            if img_z is None:
                img_z = loadimg(folder+y+'/'+x+'/' + z)
                f.write(str(img_z.shape)+'\n')
            else:
                tmp = loadimg(folder+y+'/'+x+'/' + z)
                f.write(str(tmp.shape)+'\n'+'-----\n')
                img_z = np.append(img_z,tmp,axis=2)
                f.write(str(img_z.shape)+'\n')
    writetiff3d(folder+y+'/'+x+'/' + x + '_z.tif',img_z)
    # if img_z.shape[2] != 4923:
    #     with open (folder + 'check_abnormal_tif.txt', 'a') as f:
    #         f.write(folder+y+'/'+x+'/' + x + '_z.tif\n')
    print(folder+y+'/'+x+'/' + x + '_z.tif Done!' )

def cropz(resolution):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    for y in crop_y:
        if len(y) != 6:
            continue
        crop_x = os.listdir(folder+y)
        pool = mp.Pool()
        for x in crop_x:
            print(str(x))
            if len(x) != 13:
                continue
            # if os.path.exists(folder+y+'/'+x+'/' + x + '_z.tif'):
            #     continue
            print('constructing: '+folder+y+'/'+x+'/' + x + '_z.tif')
            pool.apply_async(cropz_worker, args=(folder, y, x))
        pool.close()
        pool.join()
'''     
def cropz(resolution):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    for y in crop_y:
        if len(y) != 6:
            continue
        crop_x = os.listdir(folder+y)
        for x in crop_x:
            print(str(x))
            if len(x) != 13:
                continue
            crop_z = os.listdir(folder+y+'/'+x)
            img_z = None
            with open(folder+y+'/'+x+'/' + x + '_info.txt', 'w') as f:
                for z in crop_z:
                    if not (fnmatch.fnmatch(z, '*.tif') and len(z) == 24):
                        continue
                    print(str(z))
                    if img_z is None:
                        img_z = loadimg(folder+y+'/'+x+'/' + z)
                        f.write(str(img_z.shape)+'\n')
                    else:
                        tmp = loadimg(folder+y+'/'+x+'/' + z)
                        f.write(str(tmp.shape)+'\n'+'-----\n')
                        img_z = np.append(img_z,tmp,axis=2)
                        f.write(str(img_z.shape)+'\n')
            if img_z.shape[2] != 4923:
                with open (folder + 'check_abnormal_tif.txt', 'a') as f:
                    f.write(folder+y+'/'+x+'\n')
            else:
                writetiff3d(folder+y+'/'+x+'/' + x + '_z.tif',img_z)

'''     
def cropx_worker(folder, y):
    crop_x = os.listdir(folder+y)
    img_x = None
    with open(folder+y+'/' + y + '_info.txt', 'w') as f:
        for x in crop_x:
            if len(x) != 13:
                continue
            crop_z = os.listdir(folder+y+'/'+x)
            for z in crop_z:
                if not fnmatch.fnmatch(z, x + '_z.tif'):
                    continue  
                # print(str(z))
                if img_x is None:
                    img_x = loadimg(folder+y+'/'+x+'/' + x + '_z.tif')
                    f.write(str(img_x.shape) + '\n')
                else:
                    tmp = loadimg(folder+y+'/'+x+'/' + x + '_z.tif')
                    f.write(str(tmp.shape) + '\n')
                    img_x = np.append(img_x, tmp, axis=0)
        f.write('-------\n'+str(img_x.shape) + '\n')
    writetiff3d(folder+y+'/'+ y + '_x.tif',img_x) 
    print(folder+y+'/'+ y + '_x.tif')  

def cropx(resolution):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    pool = mp.Pool()
    for y in crop_y:
        if len(y) != 6:
            continue
        if os.path.exists(folder+y+'/'+ y + '_x.tif'):
            print('continue')
            continue
        print(str(y))
        pool.apply_async(cropx_worker, args=(folder, y))
    pool.close()
    pool.join()

'''
def cropx(resolution):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    for y in crop_y:
        if len(y) != 6:
            continue
        if os.path.exists(folder+y+'/'+ y + '_x.tif'):
            print('continue')
            continue
        print(y)
        crop_x = os.listdir(folder+y)
        img_x = None
        with open(folder+y+'/' + y + '_info.txt', 'w') as f:
            for x in crop_x:
                if len(x) != 13:
                    continue
                crop_z = os.listdir(folder+y+'/'+x)
                for z in crop_z:
                    if not fnmatch.fnmatch(z, x + '_z.tif'):
                        continue  
                    print(str(z))
                    if img_x is None:
                        img_x = loadimg(folder+y+'/'+x+'/' + x + '_z.tif')
                        f.write(str(img_x.shape) + '\n')
                    else:
                        tmp = loadimg(folder+y+'/'+x+'/' + x + '_z.tif')
                        f.write(str(tmp.shape) + '\n')
                        img_x = np.append(img_x, tmp, axis=0)
            f.write('-------\n'+str(img_x.shape) + '\n')
        writetiff3d(folder+y+'/'+ y + '_x.tif',img_x)

        

def cropy(resolution):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    img = None
    count = 0
    with open(folder + 'info_02.txt', 'w') as f:
        for y in crop_y:
            if len(y) != 6:
                continue
            
            if count <= 9:
                count += 1
                continue
            print(str(count) + ': ' + y)
            count += 1
            crop_x = os.listdir(folder+y)
            for x in crop_x:
                if not fnmatch.fnmatch(x, y + '_x.tif'):
                    continue
                print(x)
                tmp = loadimg(folder+y+'/'+y + '_x.tif')
                f.write(str(tmp.shape) + '\n')
                if img is not None:
                    img = np.append(tmp,img,axis=1)
                else:
                    img = tmp  
        f.write('-----\n'+ str(img.shape) + '\n')
    writetiff3d(folder  + resolution + '_whole_02.tif',img)
# def worker_x(dir_y, log, val):
#     with open(log, 'a') as f:
#         crop_x = os.listdir(dir_y)
#         for x in crop_x:
#             print(str(x))
#             if len(x) != 13:
#                 continue
#             crop_z = os.listdir(dir_y+'/'+x)
#             for z in crop_z:
#                 if not (fnmatch.fnmatch(z, '*.tif') and len(z) == 24):
#                     continue
#                 print(str(z))
#                 img = loadimg(dir_y+'/'+x+'/' + z)
#                 print(': ' + str(img.shape))
#                 if img.shape[2] != val:
#                     print('abnormal!')
#                     f.write(dir_y+'/'+x+'/' + z + '\n')

# def checkz(resolution, val):
#     folder = '/Volumes/dh/heng_wang/' + resolution + '/'
#     crop_y = os.listdir(folder)
#     pool = mp.Pool()
#     with open(folder + 'check_abnormal_tif_file.txt', 'w') as f:
#         f.write('check tif file for ' + resolution + '\n')
#         for y in crop_y:
#             if len(y) != 6:
#                 continue
#             pool.apply_async(worker_x, args=(folder+y, folder + 'check_abnormal_tif_file.txt', val))
#     pool.close()   
#     pool.join()

def checkz(resolution, val):
    folder = '/Volumes/dh/heng_wang/' + resolution + '/'
    crop_y = os.listdir(folder)
    with open(folder + 'check_abnormal_tif_file2.txt', 'w') as f:
        for y in crop_y:
            if len(y) != 6:
                continue
            print(y)
            crop_x = os.listdir(folder+y)
            for x in crop_x:
                # print(str(x))
                if len(x) != 13:
                    continue
                print(x)
                crop_z = os.listdir(folder+y+'/'+x)
                for z in crop_z:
                    if not (fnmatch.fnmatch(z, '*.tif') and len(z) == 24):
                        continue
                    img = loadimg(folder+y+'/'+x+'/' + z)
                    print(z + ': ' + str(img.shape))
                    if img.shape[2] != val:
                        print('abnormal: ' + str(val))
                        f.write(folder+y+'/'+x+'/' + z + '\n')
cropz('RES(27300x17206x4923)')
# checkz('RES(3412x2150x615)', 205)
# cropx('RES(6825x4301x1230)')