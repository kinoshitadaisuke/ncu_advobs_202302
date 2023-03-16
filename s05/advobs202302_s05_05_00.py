#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 17:43:38 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Calculating statistical values of pixel data of an image'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='name of a FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_fits = args.file

# if the extension of the file is not '.fits', then skip
if (file_fits[-5:] != '.fits'):
    print (f'ERROR: "{file_fits}" is not a FITS file!')
    sys.exit (1)

# printing header
print (f'{"-" * 77}')
print (f'{"file":32s} {"max":>8s} {"min":>8s}', \
       f'{"mean":>8s} {"median":>8s} {"stddev":>8s}')
print (f'{"=" * 77}')

# file name
path_fits = file_fits.split ('/')
filename = path_fits[-1]

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # data of primary HDU
    data0 = hdu0.data
    
    # calculations of statistical values using numpy
    data_max      = numpy.amax (data0)
    data_min      = numpy.amin (data0)
    data_mean     = numpy.mean (data0)
    data_median   = numpy.median (data0)
    data_variance = numpy.var (data0)
    data_stddev   = numpy.std (data0)

    # printing results of calculation
    print (f'{filename:32s} {data_max:8.2f} {data_min:8.2f}', \
           f'{data_mean:8.2f} {data_median:8.2f} {data_stddev:8.2f}')

# printing footer
print (f'{"-" * 77}')
