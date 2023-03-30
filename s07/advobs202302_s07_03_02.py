#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 22:36:12 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Calculating statistical values of pixel data'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files = args.files

# printing header
print (f'{"-" * 80}')
print (f'{"file":17s} {"n_pix":>7s}', \
       f'{"mean":>8s} {"median":>8s} {"stddev":>7s}', \
       f'{"min":>5s} {"max":>5s}', \
       f'{"skew":>6s} {"kurtosis":>9s}')
print (f'{"=" * 80}')

# processing files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    
    # if the extension of the file is not '.fits', then skip
    if (path_fits.suffix != '.fits'):
        continue

    # if the file does not exist, then skip
    if not (path_fits.exists ()):
        continue

    # file name without extension
    filename = path_fits.stem

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
    
        # header of primary HDU
        header0 = hdu0.header

        # image data of primary HDU
        data0 = hdu0.data

    # calculation of statistical values
    n_pix    = data0.size
    mean     = numpy.nanmean (data0)
    median   = numpy.nanmedian (data0)
    stddev   = numpy.nanstd (data0)
    vmin     = numpy.nanmin (data0)
    vmax     = numpy.nanmax (data0)
    skew     = scipy.stats.skew (data0, axis=None)
    kurtosis = scipy.stats.kurtosis (data0, axis=None)
    
    # printing results
    print (f'{filename:17s} {n_pix:7d}', \
           f'{mean:8.2f} {median:8.2f} {stddev:7.2f}', \
           f'{vmin:5.0f} {vmax:5.0f} {skew:6.2f} {kurtosis:9.2f}')

# printing footer
print (f'{"-" * 80}')
