#!/bin/bash
module load python3/3.4.3;
pyvenv meit python=python3;
source meit/bin activate;
pip3 install --upgrade pip==9.0.1;
pip3 install tqdm==4.19.5;
pip3 install scikit-image==0.12.3;
pip3 install scikit-fmm==0.0.9;
pip3 install tifffile==0.9.0;
pip3 install PyWavelets==0.5.2;
pip3 install pyglet==1.3.1;
pip3 install cython==0.27.3;
