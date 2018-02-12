"""
Tracing in MEIT
"""
import math
from tqdm import tqdm
import numpy as np
import skfmm
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage.morphology import binary_dilation
from filtering.morphology import ssm
from skimage.filters import threshold_otsu
from .soma import Soma
from .swc import SWC
from .tip import Tip
from .utils.io import *


class Tracer(object):

    def __init__(self):
        pass

    def reset(self):
        pass

    def trace(self):
        pass


class R2Tracer(Tracer):

    def __init__(self, quality=False, silent=True, speed='dt', clean=False, img=None, cropx=None, cropy=None, threshold=None):
        self._quality = quality
        self._img = img
        self._bimg = None
        self._cropx = cropx
        self._cropy = cropy
        self._dilated_bimg = None
        self._bsum = 0  # For counting the covered foreground
        self._bb = None  # For making the erasing contour
        self._t = None  # Original timemap
        self._tt = None  # The copy of the timemap
        self._grad = None
        self._coverage = 0.
        self._soma = None  # Soma
        self.somainfo = None
        self._silent = silent  # Disable all console outputs
        # Tracing stops when 98% of the foreground has been covered
        self._target_coverage = 0.98
        self._cover_ctr_old = 0.
        self._cover_ctr_new = 0.
        # The type of speed image to use. Options are ['dt', 'ssm']
        self._speed = speed
        self._erase_ratio = 1.7 if self._speed == 'ssm' else 1.5
        # Whether the unconnected branches will be discarded
        self._clean = clean
        self._eps = 1e-5

        self._starting_pt = None # Source point of a block in each tracing iteration

        self._empty_face = None  # Check when no tip on boundary
        self._tforboundary = None # For setting t-value of non-boundary-tip tips

        self._threshold = threshold # For filtering foreground and background

        # Set traceability of each block
        self._check = None
        if img is not None:
            self._check = np.zeros((img.shape[0], img.shape[1], img.shape[2])) # Initially 0

    def trace(self, starting_pt):
        '''
        The main entry for MEIT. Tracing of a block (cropx*cropy).
        Input: Source point of this block
        Return source points of neighbouring blocks and reconstruction of this block
        '''
        self._empty_face = [True, True, True, True] # All 4 faces initially not touched
        self._tforboundary = [
            starting_pt.tvalue(), starting_pt.tvalue(), starting_pt.tvalue(), starting_pt.tvalue()]

        # Check the traceability of this block
        whole = (starting_pt.xmax() - starting_pt.xmin()) * \
            (starting_pt.ymax() - starting_pt.ymin()) * self._img.shape[2]
        sub = self._check[starting_pt.xmin():starting_pt.xmax(
        ), starting_pt.ymin():starting_pt.ymax(), :].sum()
        if sub / whole > 0.99:
            return None, None
        else:
            self._check[starting_pt.xmin():starting_pt.xmax(
            ), starting_pt.ymin():starting_pt.ymax(), :] = 1

        img = self._img[starting_pt.xmin():starting_pt.xmax(),
                        starting_pt.ymin():starting_pt.ymax(), :]

        self._bimg = (img > self._threshold).astype('int')  # Segment image
        # Check the percentage of foreground points in this block
        if self._bimg.sum() / img.shape[0] * img.shape[1] * img.shape[2] < 0.00005:
            return None, None

        self.somainfo = np.asarray(
            [starting_pt.xyz()[0], starting_pt.xyz()[1], starting_pt.xyz()[2], starting_pt.radius()])

        if not self._silent:
            print('(1) --Detecting Soma...', end='')
        self._soma = Soma()
        self._soma.detect(self._bimg, self.somainfo,
                          not self._quality, self._silent)
        self._prep()


        self._starting_pt = starting_pt
        if not self._silent:
            print('(5) --Start Backtracking...')
        swc, tips = self._iterative_backtrack()

        # Check for boundary face which has not been touched
        for i in range(0, 4):
            my_boundary = np.asarray([0, 0, 0, 0])
            if i == 0 and self._empty_face[i]:
                my_boundary[0] = max(0, starting_pt.xmin() - self._cropx + 1)
                my_boundary[1] = starting_pt.xmin() + 1
                my_boundary[2] = starting_pt.ymin()
                my_boundary[3] = starting_pt.ymax()
            elif i == 1 and self._empty_face[i]:
                my_boundary[0] = starting_pt.xmax() - 1
                my_boundary[1] = min(self._img.shape[0],
                                     starting_pt.xmax() + self._cropx - 1)
                my_boundary[2] = starting_pt.ymin()
                my_boundary[3] = starting_pt.ymax()
            elif i == 2 and self._empty_face[i]:
                my_boundary[0] = starting_pt.xmin()
                my_boundary[1] = starting_pt.xmax()
                my_boundary[2] = max(0, starting_pt.ymin() - self._cropy + 1)
                my_boundary[3] = starting_pt.ymin() + 1
            elif i == 3 and self._empty_face[i]:
                my_boundary[0] = starting_pt.xmin()
                my_boundary[1] = starting_pt.xmax()
                my_boundary[2] = starting_pt.ymax() - 1
                my_boundary[3] = min(self._img.shape[1],
                                     starting_pt.ymax() + self._cropy - 1)
            else:
                continue
            tip = self._final_check(my_boundary, i)
            if tip is not None:
                tips.append(tip)

        if self._clean: # Always false since we do not provide any function to prune branches
            swc.prune()

        self._restore()
        return swc, tips

    def _final_check(self, block, pos):
        '''
        Check whether this block worth tracing or not
        Input: block coordinates and the position of it
        Return the found tip which is closest to the boundary face of this block's predecessor
        '''

        bimg = (self._img[block[0]:block[1], block[2]
                :block[3], :] > self._threshold).astype('int')

        if bimg.sum() / bimg.shape[0] * bimg.shape[1] * bimg.shape[2] < 0.00005:
            return None
        whole = bimg.shape[0] * bimg.shape[1] * bimg.shape[2]
        sub = self._check[block[0]:block[1], block[2]:block[3], :].sum()
        if sub / whole > 0.99:
            return None
        bimg = (self._img[block[0]:block[1], block[2]:block[3], :]
                > self._threshold).astype('int')  # Segment image
        soma_pos = None
        flag = 0
        # Figure out the point closest to the boundary face
        if pos == 0:
            for x in range(0, bimg.shape[0]):
                if flag == 1:
                    break
                x_t = bimg.shape[0] - x - 1
                for y in range(0, bimg.shape[1]):
                    if flag == 1:
                        break
                    for z in range(0, bimg.shape[2]):
                        if bimg[x_t][y][z] == 1:
                            soma_pos = np.asarray([x_t, y, z])
                            flag = 1
                            break
        elif pos == 1:
            for x in range(0, bimg.shape[0]):
                if flag == 1:
                    break
                for y in range(0, bimg.shape[1]):
                    if flag == 1:
                        break
                    for z in range(0, bimg.shape[2]):
                        if bimg[x][y][z] == 1:
                            soma_pos = np.asarray([x, y, z])
                            flag = 1
                            break
        elif pos == 3:
            for y in range(0, bimg.shape[1]):
                if flag == 1:
                    break
                for x in range(0, bimg.shape[0]):
                    if flag == 1:
                        break
                    for z in range(0, bimg.shape[2]):
                        if bimg[x][y][z] == 1:
                            soma_pos = np.asarray([x, y, z])
                            flag = 1
                            break
        elif pos == 2:
            for y in range(0, bimg.shape[1]):
                if flag == 1:
                    break
                y_t = bimg.shape[1] - 1 - y
                for x in range(0, bimg.shape[0]):
                    if flag == 1:
                        break
                    for z in range(0, bimg.shape[2]):
                        if bimg[x][y_t][z] == 1:
                            soma_pos = np.asarray([x, y_t, z])
                            flag = 1
                            break

        self._tforboundary[pos] = max(self._tforboundary) + 1
        r = estimate_radius(
            soma_pos, (self._img[block[0]:block[1], block[2]:block[3], :] > self._threshold).astype('int'))
        tip = Tip(self._tforboundary[pos], block, r, soma_pos, pos)

        return tip

    def _prep(self):
        self._nforeground = self._bimg.sum()
        # Dilate bimg to make it less strict for the big gap criteria
        # It is needed since sometimes the tracing goes along the
        # boundary of the thin fibre in the binary img
        self._dilated_bimg = binary_dilation(self._bimg)

        if not self._silent:
            print('(2) --Boundary DT...')
        self._make_dt()
        if not self._silent:
            print('(3) --Fast Marching with %s quality...' %
                  ('high' if self._quality else 'low'))
        self._fast_marching()
        if not self._silent:
            print('(4) --Compute Gradients...')
        self._make_grad()

        # Make copy of the timemap
        self._tt = self._t.copy()
        self._tt[self._bimg <= 0] = -2

        # Label all voxels of soma with -3
        self._tt[self._soma.mask > 0] = -3

        # For making a large tube to contain the last traced branch
        self._bb = np.zeros(shape=self._tt.shape)

    def _update_coverage(self):
        self._cover_ctr_new = np.logical_and(
            self._tt < 0, self._bimg > 0).sum()

        self._coverage = self._cover_ctr_new / self._nforeground
        if not self._silent:
            self._pbar.update(self._cover_ctr_new - self._cover_ctr_old)
        self._cover_ctr_old = self._cover_ctr_new

    def _make_grad(self):
        # Get the gradient of the Time-crossing map
        dx, dy, dz = self._dist_gradient()
        standard_grid = (np.arange(self._t.shape[0]), np.arange(self._t.shape[1]),
                         np.arange(self._t.shape[2]))
        self._grad = (RegularGridInterpolator(standard_grid, dx),
                      RegularGridInterpolator(standard_grid, dy),
                      RegularGridInterpolator(standard_grid, dz))

    def _make_dt(self):
        '''
        Make the distance transform according to the speed type
        '''
        self._dt = skfmm.distance(self._bimg, dx=5e-2)  # Boundary DT
        if self._speed == 'ssm':
            if not self._silence:
                print('--SSM with GVF...')
            self._dt = ssm(self._dt, anisotropic=True, iterations=40)
            img = self._dt > threshold_otsu(self._dt)
            self._dt = skfmm.distance(img, dx=5e-2)
            self._dt = skfmm.distance(np.logical_not(self._dt), dx=5e-3)
            self._dt[self._dt > 0.04] = 0.04
            self._dt = self._dt.max() - self._dt

    def _fast_marching(self):
        speed = self._make_speed(self._dt)
        # # Fast Marching
        if self._quality:
            #if not self._silent: print('--MSFM...')
            self._t = msfm.run(speed, self._bimg.copy().astype(
                'int64'), self._soma.centroid, True, True)
        else:
            #if not self._silent: print('--FM...')
            marchmap = np.ones(self._bimg.shape)
            marchmap[self._soma.centroid[0],
                     self._soma.centroid[1], self._soma.centroid[2]] = -1
            self._t = skfmm.travel_time(marchmap, speed, dx=5e-3)

    def _make_speed(self, dt):
        F = dt**4
        F[F <= 0] = 1e-10
        return F

    def _get_timemap(self, x, y, z):
        return self._t[x, y, z]

    def _dist_gradient(self):
        fx = np.zeros(shape=self._t.shape)
        fy = np.zeros(shape=self._t.shape)
        fz = np.zeros(shape=self._t.shape)

        J = np.zeros(shape=[s + 2 for s in self._t.shape])  # Padded Image
        J[:, :, :] = self._t.max()
        J[1:-1, 1:-1, 1:-1] = self._t
        Ne = [[-1, -1, -1], [-1, -1, 0], [-1, -1, 1], [-1, 0, -1], [-1, 0, 0],
              [-1, 0, 1], [-1, 1, -1], [-1, 1, 0], [-1, 1, 1], [0, -1, -1],
              [0, -1, 0], [0, -1, 1], [0, 0, -1], [0, 0, 1], [0, 1, -1],
              [0, 1, 0], [0, 1, 1], [1, -1, -1], [1, -1, 0], [1, -1, 1],
              [1, 0, -1], [1, 0, 0], [1, 0, 1], [1, 1, -1], [1, 1, 0], [1, 1, 1]]

        for n in Ne:
            In = J[1 + n[0]:J.shape[0] - 1 + n[0], 1 + n[1]:J.shape[1] - 1 + n[1],
                   1 + n[2]:J.shape[2] - 1 + n[2]]
            check = In < self._t
            self._t[check] = In[check]
            D = np.divide(n, np.linalg.norm(n))
            fx[check] = D[0]
            fy[check] = D[1]
            fz[check] = D[2]
        return -fx, -fy, -fz

    def _step(self, branch):
        # RK4 Walk for one step
        p = rk4(branch.pts[-1], self._grad, self._t, 1)
        branch.update(p, self._bimg, self._dilated_bimg)

    def _erase(self, branch):
        # Erase it from the timemap
        for i in range(len(branch.pts)):
            n = [math.floor(n) for n in branch.pts[i]]
            r = 1 if branch.radius[i] < 1 else branch.radius[i]

            # To make sure all the foreground voxels are included in bb
            r = math.ceil(r * self._erase_ratio)
            X, Y, Z = np.meshgrid(
                constrain_range(n[0] - r, n[0] + r + 1, 0, self._tt.shape[0]),
                constrain_range(n[1] - r, n[1] + r + 1, 0, self._tt.shape[1]),
                constrain_range(n[2] - r, n[2] + r + 1, 0, self._tt.shape[2]))
            self._bb[X, Y, Z] = 1

        startidx, endidx = [math.floor(p) for p in branch.pts[0]], [
            math.floor(p) for p in branch.pts[-1]]

        if len(branch.pts) > 5 and self._t[endidx[0], endidx[1], endidx[2]] < self._t[
                startidx[0], startidx[1], startidx[2]]:
            erase_region = np.logical_and(
                self._t[endidx[0], endidx[1], endidx[2]] <= self._t,
                self._t <= self._t[startidx[0], startidx[1], startidx[2]])
            erase_region = np.logical_and(self._bb, erase_region)
        else:
            erase_region = self._bb.astype('bool')

        if np.count_nonzero(erase_region) > 0:
            self._tt[erase_region] = -2 if branch.low_conf else -1
        self._bb.fill(0)

    def _iterative_backtrack(self):

        # Initialise swc with the soma centroid
        swc = SWC(self._soma, self._starting_pt, self._t, self._cropx,
                  self._cropy, self._img.shape[0:2])

        if not self._silent:
            self._pbar = tqdm(total=math.floor(
                self._nforeground * self._target_coverage))

        # Loop for all branches
        found_tips = []
        prev_srcpt = None
        count = 0
        prev_coverage = -1
        while self._coverage < self._target_coverage:

            self._update_coverage()
            if prev_coverage != -1:
                if self._coverage == prev_coverage:
                    return swc, found_tips
            prev_coverage = self._coverage
           
            srcpt = np.asarray(np.unravel_index(
                self._tt.argmax(), self._tt.shape)).astype('float64')
            if prev_srcpt is not None:
                if srcpt[0] == prev_srcpt[0] and srcpt[1] == prev_srcpt[1] and srcpt[2] == prev_srcpt[2]:
                    return swc, found_tips
            prev_srcpt = srcpt
           

            branch = R2Branch()
            branch.add(srcpt, 1., 1.)

            # Erase the source point just in case
            self._tt[math.floor(srcpt[0]), math.floor(
                srcpt[1]), math.floor(srcpt[2])] = -2
            
            keep = True

            # Loop for 1 back-tracking iteration
            while True:
                self._step(branch)
                head = branch.pts[-1]
                tt_head = self._tt[math.floor(head[0]), math.floor(
                    head[1]), math.floor(head[2])]

                # 1. Check out of bound
                if not inbound(head, self._bimg.shape):
                    branch.slice(0, -1)
                    break

                # 2. Check for the large gap criterion
                if branch.gap > np.asarray(branch.radius).mean() * 8:
                    break
                else:
                    branch.reset_gap()

                # 3. Check if Soma has been reached
                if tt_head == -3:
                    keep = True if branch.branchlen > self._soma.radius * 3 else False
                    branch.reached_soma = True
                    break

                # 4. Check if not moved for 15 iterations
                if branch.is_stucked():
                    break

                # 5. Check for low online confidence
                if branch.low_conf:
                    keep = False
                    break

                # 6. Check for branch merge
                # Consider reaches previous explored area traced with branch
                # Note: when the area was traced due to noise points
                # (erased with -2), not considered as 'reached'
                if tt_head == -1:
                    branch.touched = True
                    if swc.size() == 1:
                        break

                    matched, matched_idx = swc.match(head, branch.radius[-1])
                    if matched > 0:
                        branch.touch_idx = matched_idx
                        break

                    if branch.steps_after_reach > 200:
                        break

            self._erase(branch)
    
            # Add to SWC if it was decided to be kept
            if keep:
                pidx = None
                if branch.reached_soma:
                    pidx = 0
                elif branch.touch_idx >= 0:
                    pidx = branch.touch_idx
                tips = swc.add_branch(branch, pidx)

                for tip in tips:
                    if self._empty_face[tip.pos()] is True:
                        found_tips.append(tip)
                        count += 1
                        self._empty_face[tip.pos()] = False
                        self._tforboundary[tip.pos()] = tip.tvalue()

        return swc, found_tips

    def _restore(self):
        self._bimg = None
        self._dilated_bimg = None
        self._bsum = 0  # For counting the covered foreground
        self._bb = None  # For making the erasing contour
        self._t = None  # Original timemap
        self._tt = None  # The copy of the timemap
        self._grad = None
        self._coverage = 0.
        self._soma = None  # soma
        self.somainfo = None
        # Tracing stops when 98% of the foreground has been covered
        self._target_coverage = 0.98
        self._cover_ctr_old = 0.
        self._cover_ctr_new = 0.
        self._eps = 1e-5

        self._starting_pt = None


class Branch(object):
    def __init__(self):
        self.pts = []
        self.radius = []


class R2Branch(Branch):
    def __init__(self):
        self.pts = []
        self.conf = []
        self.radius = []
        self.steps_after_reach = 0
        self.low_conf = False
        self.touch_idx = -2
        self.reached_soma = False
        self.branchlen = 0
        self.gap = 0
        self.online_voxsum = 0
        self.stepsz = 0
        self.touched = False

        self.ma_short = -1
        self.ma_long = -1
        self.ma_short_window = 4
        self.ma_long_window = 10
        self.in_valley = False

    def add(self, pt, conf, radius):
        self.pts.append(pt)
        self.conf.append(conf)
        self.radius.append(radius)

    def is_stucked(self):
        if self.stepsz == 0:
            return True

        if len(self.pts) > 15:
            if np.linalg.norm(np.asarray(self.pts[-1]) - np.asarray(self.pts[-15])) < 1:
                return True
            else:
                return False
        else:
            return False

    def reset_gap(self):
        self.gap = 0

    def update(self, pt, bimg, dilated_bimg):
        # pt is the new point found
        eps = 1e-5
        head = self.pts[-1]
        velocity = np.asarray(pt) - np.asarray(head)
        # the distance between the new pt and the current head
        self.stepsz = np.linalg.norm(velocity)
        self.branchlen += self.stepsz
        b = dilated_bimg[math.floor(pt[0]), math.floor(
            pt[1]), math.floor(pt[2])]
        if b > 0:  # then this pt is on foreground
            self.gap += self.stepsz

        self.online_voxsum += b
        oc = self.online_voxsum / (len(self.pts) + 1)
        self.update_ma(oc)

        # We are stepping in a valley
        if (self.ma_short < self.ma_long - eps and
                oc < 0.5 and not self.in_valley):
            self.in_valley = True

        # Cut at the valley
        if self.in_valley and self.ma_short > self.ma_long:
            valleyidx = np.asarray(self.conf).argmin()
            # Only cut if the valley confidence is below 0.5
            if self.conf[valleyidx] < 0.5:
                self.slice(0, valleyidx)
                self.low_conf = True
            else:
                in_valley = False

        if oc <= 0.2:
            self.low_conf = True

        if self.touched:
            self.steps_after_reach += 1

        r = estimate_radius(pt, bimg)
        self.add(pt, oc, r)

    def update_ma(self, oc):
        if len(self.pts) > self.ma_long_window:
            if self.ma_short == -1:
                self.ma_short = oc
            else:
                self.ma_short = exponential_moving_average(
                    oc, self.ma_short, self.ma_short_window
                    if len(self.pts) >= self.ma_short_window else len(self.pts))
            if self.ma_long == -1:
                self.ma_long = oc
            else:
                self.ma_long = exponential_moving_average(
                    oc, self.ma_long, self.ma_long_window
                    if len(self.pts) >= self.ma_long_window else len(self.pts))

    def slice(self, start, end):
        self.pts = self.pts[start: end]
        self.radius = self.radius[start: end]
        self.conf = self.conf[start: end]


def estimate_radius(pt, bimg):
    r = 0
    x = math.floor(pt[0])
    y = math.floor(pt[1])
    z = math.floor(pt[2])

    while True:
        r += 1
        try:
            if bimg[max(x - r, 0):min(x + r + 1, bimg.shape[0]), max(y - r, 0):
                    min(y + r + 1, bimg.shape[1]), max(z - r, 0):min(
                        z + r + 1, bimg.shape[2])].sum() / (2 * r + 1)**3 < .6:
                break
        except IndexError:
            break

    return r


def exponential_moving_average(p, ema, n):
    '''
    The exponential moving average (EMA) traditionally
    used in analysing stock market.
    EMA_{i+1} = (p * \alpha) + (EMA_{i} * (1 - \alpha))
    where p is the new value; EMA_{i} is the last ema value;
    n is the time period; \alpha=2/(1+n) is the smoothing factor.

    ---------------------------------------------
    Parameters:
    p: The new value in the sequence
    ema: the last EMA value
    n: The period window size
    '''

    alpha = 2 / (1 + n)
    return p * alpha + ema * (1 - alpha)


def rk4(srcpt, ginterp, t, stepsize):
    # Compute K1
    k1 = np.asarray([g(srcpt)[0] for g in ginterp])
    k1 *= stepsize / max(np.linalg.norm(k1), 1.)
    tp = srcpt - 0.5 * k1  # Position of temporary point
    if not inbound(tp, t.shape):
        return srcpt

    # Compute K2
    k2 = np.asarray([g(tp)[0] for g in ginterp])
    k2 *= stepsize / max(np.linalg.norm(k2), 1.)
    tp = srcpt - 0.5 * k2  # Position of temporary point
    if not inbound(tp, t.shape):
        return srcpt

    # Compute K3
    k3 = np.asarray([g(tp)[0] for g in ginterp])
    k3 *= stepsize / max(np.linalg.norm(k3), 1.)
    tp = srcpt - k3  # Position of temporary point
    if not inbound(tp, t.shape):
        return srcpt

    # Compute K4
    k4 = np.asarray([g(tp)[0] for g in ginterp])
    k4 *= stepsize / max(np.linalg.norm(k4), 1.)

    return srcpt - (k1 + k2 * 2 + k3 * 2 + k4) / 6.0  # Compute final point


def inbound(pt, shape):
    return all([True if 0 <= p <= s - 1 else False for p, s in zip(pt, shape)])


def constrain_range(min, max, minlimit, maxlimit):
    return list(
        range(min if min > minlimit else minlimit, max
              if max < maxlimit else maxlimit))
