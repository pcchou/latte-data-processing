#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
import numpy as np
from glob import glob
import re


exposures = set(map(lambda x: re.match(r'\d{8}_Dark_(.+?)-\d+?\.fit', x).group(1), glob("*.fit*")))
for exposure in exposures:
    data = []
    print(f'Processing exposure {exposure}...')

    for filename in glob(f"20220630_Dark_{exposure}.fit*"):
        last = filename

        print(f'Opening file: {filename}')
        fd = pyfits.getdata(filename)
        data.append(fd)

    with open(last, 'rb') as f:
        lastf = pyfits.open(f)[0]

    master_data = np.mean(data, axis=0)

    h = pyfits.PrimaryHDU(master_data, header=lastf.header, scale_back=False)
    h.scale('uint16')
    h.header['BZERO'] = 32768
    h.header['BSCALE'] = 1
    print(f'Saving image... master_dark_{exposure}.fit')
    h.writeto(f'master_dark_{exposure}.fit', overwrite=True)
