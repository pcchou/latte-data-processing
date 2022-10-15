#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
from skimage import transform as skt

exposures = ['5min']
for exposure in exposures:
    try:
        with open(f'master_dark_{exposure}.fit', 'rb') as f:
            fits = pyfits.open(f)[0]
            data = fits.data
    except FileNotFoundError:
        print(f'Exposure {exposure} no file!')
        continue

    print(f'Processing exposure {exposure}...')

    data_scaled = skt.downscale_local_mean(data, (2, 2))

    h = pyfits.PrimaryHDU(data_scaled, header=fits.header, scale_back=False)
    h.scale('uint16')
    h.header['BZERO'] = 32768
    h.header['BSCALE'] = 1
    print(f'Saving image... master_dark_{exposure}_downscaled.fit')
    h.writeto(f'master_dark_{exposure}_downscaled.fit', overwrite=True)
