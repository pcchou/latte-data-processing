import astropy.io.fits as pyfits
import numpy as np

bands = ['L', 'B', 'V', 'R', 'Ha', 'OIII']
for band in bands:
    try:
        with open(f'../flat_nofix/master_flat_{band}.fit', 'rb') as f:
            fits = pyfits.open(f)[0]
            data = fits.data
    except FileNotFoundError:
        print(f'Band {band} no file!')
        continue

    print(f'Processing band {band}...')

    data = data.astype('int')
    shape = data.shape
    for y in range(shape[0]):
        for x in range(shape[1]):
            if data[y][x] < 1000 and x == 2271:
                data[y][x] = np.mean([data[y][x-1], data[y][x+1]])
    
    h = pyfits.PrimaryHDU(data, header=fits.header, scale_back=False)
    h.scale('uint16')
    h.header['BZERO'] = 32768
    h.header['BSCALE'] = 1
    print(f'Saving image... master_flat_{band}.fit')
    h.writeto(f'master_flat_{band}.fit', overwrite=True)