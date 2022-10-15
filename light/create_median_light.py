#!/usr/bin/env python
# coding: utf-8
import astropy.io.fits as pyfits
import numpy as np
import astroalign as aa
from glob import glob
import re

bands = ['L', 'B', 'V', 'R', 'Ha', 'OIII', 'SII']

for band in bands:
    data = []
    if not glob(f"*-{band}.fit*"):
        print(f'Band {band} no file!')
        continue

    print(f'Processing band {band}...')

    exposure = re.search(r'_(\d+sec)', glob(f"*-{band}.fit*")[0]).group(1)
    exposure = re.sub(r'420sec', '7min', exposure)
    exposure = re.sub(r'300sec', '5min', exposure)
    exposure = re.sub(r'600sec', '10min', exposure)

    shape = pyfits.getdata(glob(f"*-{band}.fit*")[0]).shape
    if shape == (2048, 2048):
        master_dark = pyfits.getdata(f'../dark/master_dark_{exposure}_downscaled.fit')
        master_flat = pyfits.getdata(f'../flat/master_flat_{band}_downscaled.fit')
    else:
        master_dark = pyfits.getdata(f'../dark/master_dark_{exposure}.fit')
        master_flat = pyfits.getdata(f'../flat/master_flat_{band}.fit')

    master_flat = master_flat / np.median(master_flat)
    master_flat = np.where(master_flat == 0, 1, master_flat)


    for filename in glob(f"*-{band}.fit*"):
        last = filename

        print(f'Opening file: {filename}')
        fd = pyfits.getdata(filename)

        reduced = (fd.astype('int') - master_dark) / master_flat
        reduced = reduced.clip(min=0, max=65535).astype('uint16')

        if len(data) > 0:
            print(f'Registering image... {filename}')
            image, footprint = aa.register(source=reduced, target=data[0])
        else:
            image = reduced

        data.append(image)

    names = []
    for f in glob(f"*-{band}.fit*"):
        names.append(re.search(r'^(\d{8}_.+?)_', f).group(1))

    if len(set(names)) == 1:
        name = names[0]
    else:
        name = str(list(set(names)))
        raise Exception(f'special files: {name}')

    with open(last, 'rb') as f:
        lastf = pyfits.open(f)[0]

    master_data = np.median(data, axis=0)

    h = pyfits.PrimaryHDU(master_data, header=lastf.header, scale_back=False)
    h.scale('uint16')
    h.header['BZERO'] = 32768
    h.header['BSCALE'] = 1
    print(f'Saving image... {name}_master_{band}.fit')
    h.writeto(f'{name}_master_{band}.fit', overwrite=True)

print('Done!')
