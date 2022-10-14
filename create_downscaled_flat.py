#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
from skimage import transform as skt
import numpy as np
from glob import glob

bands = ['B', 'V', 'R']
for band in bands:
    try:
        with open(f'master_flat_{band}.fit', 'rb') as f:
            fits = pyfits.open(f)[0]
            data = fits.data
    except FileNotFoundError:
        continue

    data_scaled = skt.downscale_local_mean(data, (2, 2))

    h = pyfits.PrimaryHDU(data_scaled, header=fits.header, scale_back=False)
    h.scale('uint16')
    h.header['BZERO'] = 32768
    h.header['BSCALE'] = 1
    h.writeto(f'master_flat_{band}_downscaled.fit', overwrite=True)
