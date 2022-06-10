# make mosaics of S-PLUS tiles
# 2022-06-09 herpich@usp.br

from astropy.io import fits
from reproject.mosaicking import find_optimal_celestial_wcs
from reproject import reproject_interp
from reproject.mosaicking import reproject_and_coadd
import numpy as np

filters = ['G', 'R', 'F660']

for f in filters:
    print('reading images for filter', f)
    f1 = fits.open('MC0065/MC0065_%s_swp.fz' % f)
    f1[1].data[f1[1].data == 0] = np.nan
    f2 = fits.open('MC0066/MC0066_%s_swp.fz' % f)
    f2[1].data[f2[1].data == 0] = np.nan
    f3 = fits.open('MC0040/MC0040_%s_swp.fz' % f)
    f3[1].data[f3[1].data == 0] = np.nan
    f4 = fits.open('MC0041/MC0041_%s_swp.fz' % f)
    f4[1].data[f4[1].data == 0] = np.nan

    hdus = [f1[1], f2[1], f3[1], f4[1]]

    print('calculating wcs frame')
    wcs_out, shape_out = find_optimal_celestial_wcs(hdus)

    print('calculating new array')
    array, footprint = reproject_and_coadd(hdus,
                                           wcs_out, shape_out=shape_out,
                                           reproject_function=reproject_interp,
                                           match_background=True)

    print('building new image')
    hdu = fits.PrimaryHDU(array)
    for c in wcs_out.to_header().cards:
        hdu.header[c[0]] = (c[1], c[2])

    print('saving image')
    hdu.writeto('tarantula_mosaic_%s.fits' % f, overwrite=True)