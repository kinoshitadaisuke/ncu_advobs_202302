#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 15:43:38 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

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
print (f'# {"filename":20s} {"mean":>8s} {"median":>8s}', \
       f'{"stddev":>8s} {"min":>8s} {"max":>8s}')

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
    mean   = numpy.mean (data0)
    median = numpy.median (data0)
    stddev = numpy.std (data0)
    v_min  = numpy.amin (data0)
    v_max  = numpy.amax (data0)

    # printing results of calculations
    print (f'{path_file_input.name:22s} {mean:8.2f} {median:8.2f}', \
           f'{stddev:8.2f} {v_min:8.2f} {v_max:8.2f}')
