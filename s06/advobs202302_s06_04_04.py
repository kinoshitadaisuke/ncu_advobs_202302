#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 15:54:59 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc   = 'Calculating statistical values of FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_fits  = args.files

# printing header
print (f'# {"filename":20s} {"mean":>7s} {"median":>7s}', \
       f'{"stddev":>7s} {"min":>7s} {"max":>7s}', \
       f'{"skew":>7s} {"kurt":>7s}')

# processing FITS files one-by-one
for file_input in list_fits:
    # making a pathlib object
    path_file_input = pathlib.Path (file_input)

    # if input file is not a FITS file, then skip
    if not (path_file_input.suffix == '.fits'):
        # printing a message
        print (f'ERROR: input file "{file_input}" is NOT a FITS file!')
        # skip
        continue

    # file existence check using pathlib module
    if not (path_file_input.exists ()):
        # printing a message
        print (f'ERROR: input file "{file_input}" does not exist!')
        # skip
        continue

    # opening FITS file
    with astropy.io.fits.open (file_input) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        
        # reading header
        header0 = hdu0.header
        
        # reading data
        data0 = hdu0.data

    # calculating statistical values
    mean     = numpy.mean (data0)
    median   = numpy.median (data0)
    stddev   = numpy.std (data0)
    v_min    = numpy.amin (data0)
    v_max    = numpy.amax (data0)
    skew     = scipy.stats.skew (data0, axis=None)
    kurtosis = scipy.stats.kurtosis (data0, axis=None)

    # printing results of calculations
    print (f'{path_file_input.name:22s} {mean:7.2f} {median:7.2f}', \
           f'{stddev:7.2f} {v_min:7.2f} {v_max:7.2f}', \
           f'{skew:7.2f} {kurtosis:7.2f}')
