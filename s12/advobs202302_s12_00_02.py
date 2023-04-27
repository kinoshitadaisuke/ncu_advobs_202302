#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/27 19:10:10 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy
import scipy.stats
#import scipy.stats

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc   = 'Calculating statistical values of pixel data'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
list_rejection = ['none', 'sigclip']
parser.add_argument ('-r', '--rejection', choices=list_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('-n', '--nmaxiter', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
rejection  = args.rejection
threshold  = args.threshold
nmaxiter   = args.nmaxiter
list_files = args.files

# printing header
print (f'{"-" * 80}')
print (f'{"file":20s} {"n_pix":>7s}', \
       f'{"mean":>8s} {"median":>8s} {"stddev":>7s}', \
       f'{"min":>8s} {"max":>8s}', \
       f'{"skew":>6s}')
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

    # flattening data (2-dim. data --> 1-dim. data)
    data_1d = data0.flatten ()

    # if rejection algorithm is used, then do rejection check
    if (rejection == 'sigclip'):
        clipped = astropy.stats.sigma_clip (data_1d, cenfunc='mean', \
                                            sigma=threshold, \
                                            maxiters=nmaxiter, masked=False)
    elif (rejection == 'none'):
        clipped = data_1d

    # calculation of statistical values
    n_pix    = clipped.size
    mean     = numpy.nanmean (clipped)
    median   = numpy.nanmedian (clipped)
    stddev   = numpy.nanstd (clipped)
    vmin     = numpy.nanmin (clipped)
    vmax     = numpy.nanmax (clipped)
    skew     = scipy.stats.skew (clipped)
    
    # printing results
    print (f'{filename:20s} {n_pix:7d}', \
           f'{mean:8.2f} {median:8.2f} {stddev:7.2f}', \
           f'{vmin:8.2f} {vmax:8.2f} {skew:6.2f}')

# printing footer
print (f'{"-" * 80}')
