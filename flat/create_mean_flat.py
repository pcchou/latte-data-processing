#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
import numpy as np
from glob import glob
import re


for filename in glob("2022*.fit*"):
    last = filename
with open(last, 'rb') as f:
    lastf = pyfits.open(f)[0]

exposure = re.search(r'_(\d+sec)', last).group(1)

master_dark = pyfits.getdata(f'../dark/master_dark_{exposure}.fit')

data = []
for filename in glob("*.fit*"):
    data.append(pyfits.getdata(filename).astype('int') - master_dark)

master_data = np.mean(data, axis=0)

master_data = (master_data).clip(min=0)
h = pyfits.PrimaryHDU(master_data, header=lastf.header, scale_back=False)
h.scale('uint16')
h.header['BZERO'] = 32768
h.header['BSCALE'] = 1
h.writeto('master_flat.fit', overwrite=True)
