#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 18:12:42 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing scipy module
import scipy.stats

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
print (f'{"-" * 78}')
print (f'{"file":24s} {"max":>8s} {"min":>8s}', \
       f'{"mean":>8s} {"stddev":>8s} {"skew":>8s} {"kurtosis":>8s}')
print (f'{"=" * 78}')

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
    
    # calculations of statistical values using scipy
    data_max      = scipy.stats.tmax (data0, axis=None)
    data_min      = scipy.stats.tmin (data0, axis=None)
    data_mean     = scipy.stats.tmean (data0, axis=None)
    data_stddev   = scipy.stats.tstd (data0, axis=None)
    data_skew     = scipy.stats.skew (data0, axis=None)
    data_kurtosis = scipy.stats.kurtosis (data0, axis=None)

    # printing results of calculation
    print (f'{filename:24s} {data_max:8.2f} {data_min:8.2f}', \
           f'{data_mean:8.2f} {data_stddev:8.2f}', \
           f'{data_skew:8.2f} {data_kurtosis:8.2f}')

# printing footer
print (f'{"-" * 78}')
