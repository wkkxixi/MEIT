<!--
 Copyright (c) 2016, RivuletStudio, The University of Sydney, AU
 All rights reserved.

 This file is part of Rivuletpy <https://github.com/RivuletStudio/rivuletpy>

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
     2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
     3. Neither the name of the copyright holder nor the names of
        its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
 DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 -->

# MEIT

Large scale 3D Neuron Tracing/Neuron reconstruction in Python for 3D microscopic images powered by the Rivulet2 algorithm. Pain-free Install & Use in 5 mins.

Rivuletpy is a Python3 toolkit for automatically reconstructing single neuron models from 3D microscopic image stacks. It is actively maintained by the RivuletStudio @ University of Sydney, AU. The project was initiated in the [BigNeuron project](https://alleninstitute.org/bigneuron/about/)


## Installation

Before 0, you should firstly install Anaconda on your computer
### 0. Setup the Anaconda environment (Easy)
```
$ conda create -n riv python=3.4
$ source activate riv
```


### 1. Setup the dependencies
To run MEIT, you need to install the following packages manually beforehand

* `pip-9.0.1`
* `tqdm-4.19.5-py`
* `scikit-image-0.12.3`
* `scikit-fmm-0.0.9`
* `tifffile-0.9.0`
* `PyWavelets-0.5.2`
* `pyglet-1.3.1`
* `cython-0.27.3`
```
(riv)$ pip install --upgrade pip==9.0.1
(riv)$ conda install -c conda-forge tqdm=4.19.5
(riv)$ conda install scikit-image=0.12.3
(riv)$ pip install scikit-fmm==0.0.9
(riv)$ conda install -c conda-forge tifffile=0.9.0 
(riv)$ pip install PyWavelets==0.5.2
(riv)$ pip install pyglet==1.3.1
(riv)$ pip install cython==0.27.3
```


### 2. Clone the repository for MEIT

```
(riv)$ git clone https://github.com/wkkxixi/rivuletpy.git
(riv)$ cd rivuletpy
```


## Test Installation
In ./rivuletpy/
`sh quicktest.sh`

This will download a simple neuron image and perform a neuron tracing with rivulet2 algorithm. If you encountered any issues while installing Rivuletpy, you are welcome to raise an issue for the developers in the [issue tracker](https://github.com/wkkxixi/rivuletpy/issues)

## Usage
- Reconstruct single neuron file.

Go into rivuletpy

Run meit_single.py to start tracing of a single image file
```bash
$ python3 meit_single.py --help
usage: meit_single.py [-h] -f FILE [-o OUT] [-t THRESHOLD] [-z ZOOM_FACTOR]
                      [-cx CROPX] [-cy CROPY] [-b] [--clean] [--no-clean]
                      [--save-soma] [--no-save-soma] [--soma] [--no-soma]
                      [--speed SPEED] [--quality] [--no-quality] [--silent]
                      [--no-silent] [-v] [--no-view]

Arguments to perform the MEIT tracing algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The input file. An image file (*.tif, *.nii, *.mat).
  -o OUT, --out OUT     The name of the output file. ie. file123.swc
  -t THRESHOLD, --threshold THRESHOLD
                        threshold to distinguish the foreground and
                        background. Defulat 0. If threshold<0, otsu will be
                        used.
  -z ZOOM_FACTOR, --zoom_factor ZOOM_FACTOR
                        The factor to zoom the image to speed up the whole
                        thing. Default 0.25
  -cx CROPX, --cropx CROPX
                        The cropping parameter cropx to crop the image.
                        Default 100
  -cy CROPY, --cropy CROPY
                        The cropping parameter cropy to crop the image.
                        Default 100
  -b, --boundary        Construct boundary around each block
  --clean               Remove the unconnected segments. It is relatively safe
                        to do with the Rivulet2 algorithm
  --no-clean            Keep the unconnected segments (default)
  --save-soma           Save the automatically reconstructed soma volume along
                        with the SWC.
  --no-save-soma        Don't save the automatically reconstructed soma volume
                        along with the SWC (default)
  --soma                Use the morphological operator based soma detection
  --no-soma             Don't use the morphological operator based soma
                        detection (default)
  --speed SPEED         The type of speed image to use (dt, ssm). dt(default)
                        would work for most of the cases. ssm provides
                        slightly better curves with extra computing time
  --quality             Reconstruct the neuron with higher quality and
                        slightly more computing time
  --no-quality          Reconstruct the neuron with lower quality and slightly
                        more computing time (default)
  --silent              Omit the terminal outputs
  --no-silent           Show the terminal outputs & the nice logo (default)
  -v, --view            View the reconstructed neuron when tracing finishes
  --no-view             Does not display the reconstructed neuron when tracing
                        finishes (default)


$ python3 meit_single.py -f example.tif -t 10 # Simple like this. Reconstruct a neuron in example.tif with a background threshold of 10
$ python3 meit_single.py -f example.tif -b # Reconstruct a neuron in example.tif with the boundary frames also constructed
$ python3 meit_single.py -f example.tif -t 10 -cx 200 -cy 200 -z 0.3 # Reconstruct a neuron in example.tif with a background threshold of 10, a cropping parameter of x axis of 200, a cropping parameter of y axis of 200, a zoom factor of 0.3
$ python3 meit_single.py -f example.tif -t 10 --silent # No text will be displayed to the terminal
$ python3 meit_single.py -f example.tif -t 10 -o "myswc.swc" # The output file name would be "myswc.swc"
$ python3 meit_single.py -f example.tif -t 10 -o "myswc.swc" -v # Open a 3D swc viewer after reconstruction 
```

Please note that MEIT is powerful of tracing large-scale image with significantly less memory consumed.


- Compare a swc reconstruction against the manual ground truth.

Go into rivuletpy

Run comparesingle.py to start comparing 2 swc files
```
$ python3 comparesingle.py  --help
usage: comparesingle.py [-h] --target TARGET --groundtruth GROUNDTRUTH

Arguments for comparing two swc files.

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET       The input target swc file.
  --groundtruth GROUNDTRUTH
                        The input ground truth swc file.

$ python3 comparesingle.py --target meit_tracing.swc --groundtruth hand_tracing.swc
(0.95986696230598667, 0.99448656099241906, 0.97687013426604985)
```
The `python3 comparesingle.py` command outputs three numbers which are in order: 

precision, recall, f1-score

and saves the comparison swc file.

- Reconstruct a group of neuron files.

Go into rivuletpy

Run meit_group.py to start tracing a group of neuron files

```bash
$ python3 meit_group.py --help
usage: meit_group.py [-h] --dataset DATASET [-cx CROPX] [-cy CROPY]
                     [-z ZOOM_FACTOR] [-b] [--clean] [--no-clean]
                     [--save-soma] [--no-save-soma] [--soma] [--no-soma]
                     [--speed SPEED] [--quality] [--no-quality] [--silent]
                     [--no-silent]

Arguments to perform the MEIT tracing algorithm on a group of images.

optional arguments:
  -h, --help            show this help message and exit
  --dataset DATASET     The absolute path of the dataset on processing. All
                        images are categorised by species.
  -cx CROPX, --cropx CROPX
                        The cropping parameter cropx to crop the image.
                        Default 100
  -cy CROPY, --cropy CROPY
                        The cropping parameter cropy to crop the image.
                        Default 100
  -z ZOOM_FACTOR, --zoom_factor ZOOM_FACTOR
                        The factor to zoom the image to speed up the whole
                        thing. Default 0.25
  -b, --boundary        Construct boundary around each block
  --clean               Remove the unconnected segments. It is relatively safe
                        to do with the Rivulet2 algorithm
  --no-clean            Keep the unconnected segments (default)
  --save-soma           Save the automatically reconstructed soma volume along
                        with the SWC.
  --no-save-soma        Don't save the automatically reconstructed soma volume
                        along with the SWC (default)
  --soma                Use the morphological operator based soma detection
  --no-soma             Don't use the morphological operator based soma
                        detection (default)
  --speed SPEED         The type of speed image to use (dt, ssm). dt(default)
                        would work for most of the cases. ssm provides
                        slightly better curves with extra computing time
  --quality             Reconstruct the neuron with higher quality and
                        slightly more computing time
  --no-quality          Reconstruct the neuron with lower quality and slightly
                        more computing time (default)
  --silent              Omit the terminal outputs
  --no-silent           Show the terminal outputs & the nice logo (default)
  
$ python3 meit_group.py --dataset Gold166-JSON  # Simple like this. Reconstruct a group of neuron files in dataset Gold166-JSON
```

Please note that the group operation is quite similar to the single operation except you have to defining the absolute path of your dataset rather than that of a single file.

## FAQ
### What if I see ```...version `GLIBCXX_3.4.21' not found...``` when I run `rtrace` under Anaconda?
Try
```
(riv)$ conda install libgcc # Upgrades the gcc in your conda environment to the newest
```

### What if I see ```Intel MKL FATAL ERROR: Cannot load libmkl_avx2.so or libmkl_def.so.```?
Try to get rid of the mkl in your conda, it has been reported to cause many issues
```
(riv)$ conda install nomkl numpy scipy scikit-learn numexpr
(riv)$ conda remove mkl mkl-service
```

## Dependencies

The build-time and runtime dependencies of MEIT are:


* [Cython](http://cython.org/)
* [scikit-fmm](https://github.com/scikit-fmm)
* [scikit-image](https://github.com/scikit-image)
* [tqdm](https://github.com/noamraph/tqdm)
* [pyglet](https://pypi.python.org/pypi/pyglet/)
* [PyWavelets](https://pypi.python.org/pypi/PyWavelets/)
* [tifffile](https://pypi.python.org/pypi/tifffile/)


## Issues / questions / pull requests

Issues should be reported to the
[MEIT github repository issue tracker](https://github.com/wkkxixi/rivuletpy/issues).
The ability and speed with which issues can be resolved depends on how complete and
succinct the report is. For this reason, it is recommended that reports be accompanied
with a minimal but self-contained code sample that reproduces the issue, the observed and
expected output, and if possible, the commit ID of the version used. If reporting a
regression, the commit ID of the change that introduced the problem is also extremely valuable
information.

Questions are also welcomed in the [MEIT github repository issue tracker](https://github.com/wkkxixi/rivuletpy/issues).
If you put on a `question` label. We consider every question as an issue since it means we should have made things clearer/easier for the users.

Pull requests are definitely welcomed! Before you make a pull requests, please kindly create an issue first to discuss the optimal solution.


## Rivulet2


The `rtrace` command is powered by the latest neuron tracing algorithm Rivulet2 (Preprint hosted on BioArxiv):

Siqi Liu, Donghao Zhang, Yang Song, Hanchuan Peng, Weidong Cai, "Automated 3D Neuron Tracing with Precise Branch Erasing and Confidence Controlled Back-Tracking", bioRxiv 109892; doi: https://doi.org/10.1101/109892

The predecessor Rivulet1 was published on Neuroinformatics:

Siqi Liu, Donghao Zhang, Sidong Liu, Dagan Feng, Hanchuan Peng, Weidong Cai, 
"Rivulet: 3D Neuron Morphology Tracing with Iterative Back-Tracking", 
Neuroinformatics, Vol.14, Issue 4, pp387-401, 2016.

