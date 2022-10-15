# latte-data-processing
CCD calibration frames preprocessing and data reduction scripts used for NTHUAC's LATTE observations

The LICENSE only applies to .py scripts.

Please `pip install astropy astroalign scikit-image` if you want to use it.

## Pixel math formulas

The following are the details of pixel math operations that is done on the calibration frames and data by the processing script.

### Dark (and bias)

Let $D_R[i]$ denote the raw frames and $D_M$ be the resulting (combined) master frame.

$D_M = \text{mean}(D_R)$

#### Downsampled dark

Additionally, the 5min dark frame is downscaled (downsampled) from 4096x4096 to 2048x2048 for use in the bin 2x2 images by local mean downscaling.

### Flat (Regular flats)

These are for the flat frames that does not require special handling (band Ha/OIII).

Let $F_R[i]$ denote the raw flat frames, $D_F$ be the master dark with the corresponding exposure time, and $F_M$ be the resulting (combined) master flat frame.

$F_R^\prime[i] = F_R[i] - D_F$

$F_M = \text{mean}(F_R^\prime)$

Since the bias is included in the flat dark frames, it is not removed additionally.


### Flat (Long-short flats)

These are flat frames that are captured with an exposure less than 10 seconds (band L/B/V/R), which may leave a artifact on images due to a slow-moving shutter curtain.

Let $F_L[i]$ denote the long flat frames, $F_S[i]$ denote the short flat frames, and $F_M$ be the resulting (combined) master flat frame.

$F_M = \text{mean}(F_L) - \text{mean}(F_S)$

The flat dark is neglated due to a rather short exposure time. Since the bias is included in the short flat frames, it is not removed additionally.

#### Downsampled flat

Additionally, the flat frame for B, V, R is downscaled (downsampled) from 4096x4096 to 2048x2048 for use in the bin 2x2 images by local mean downscaling.

### Light

Let $L_R[i]$ denote the raw light frames, $F$ denote the corresponding master flat frame, $D$ denote the corresponding master dark frame, and $L_M$ be the resulting (combined) master flat frame.

<!--$\begin{equation*}
F^\prime = \left\{
        \begin{array}{ll}
            \cfrac{F}{\color{red}{\text{median}(F)}} & \text{, if } F > 0 \\
            1 & \text{, if } F = 0
        \end{array}
    \right.
\end{equation*}$-->
<img src="https://user-images.githubusercontent.com/5615415/195959141-f7e86c40-ad32-4b9b-89ee-00bdb0f36c17.png" height="80">
Note that the $\color{red}{\text{red}}$ part is a single number!

$L_R^\prime[i] = \text{align}(L_R[i] - D)$

<!--$L_M = \cfrac{\text{median}(L_R^\prime)}{F^\prime}$-->
<img src="https://user-images.githubusercontent.com/5615415/195959500-5486ce8d-407b-494c-a8f2-6f5f75b756b4.png" height="45">

Since the bias is included in the dark frames, it is not removed additionally. Also, each light frame is registered (aligned) using [astroalign](https://astroalign.quatrope.org/en/latest/) in prior to being combined.
