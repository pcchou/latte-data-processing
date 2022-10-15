import astropy.io.fits as pyfits
import numpy as np
from glob import glob


for filename in glob("2022*-long.fit*"):
    last = filename
with open(last, 'rb') as f:
    lastf = pyfits.open(f)[0]

short = []
for filename in glob("2022*-short.fit*"):
    short.append(pyfits.getdata(filename))

long = []
for filename in glob("2022*-long.fit*"):
    long.append(pyfits.getdata(filename))

master_short = np.mean(short, axis=0)
master_long = np.mean(long, axis=0)

master_data = (master_long - master_short).clip(min=0)
h = pyfits.PrimaryHDU(master_data, header=lastf.header, scale_back=False)
h.scale('uint16')
h.header['BZERO'] = 32768
h.header['BSCALE'] = 1
h.writeto('master_flat.fit', overwrite=True)
