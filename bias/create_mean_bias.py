#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
import numpy as np
from glob import glob


for filename in glob("*.fit*"):
    last = filename
with open(last, 'rb') as f:
    lastf = pyfits.open(f)[0]

data = []
for filename in glob("*.fit*"):
    data.append(pyfits.getdata(filename))

master_data = np.mean(data, axis=0)


h = pyfits.PrimaryHDU(master_data, header=lastf.header, scale_back=False)
h.scale('uint16')
h.header['BZERO'] = 32768
h.header['BSCALE'] = 1
h.writeto('master_bias.fit', overwrite=True)
