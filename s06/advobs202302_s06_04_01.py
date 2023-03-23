#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 15:36:13 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc   = 'Calculating statistical values of a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.file

# making a pathlib object
path_file_input = pathlib.Path (file_input)

# if input file is not a FITS file, then skip
if not (path_file_input.suffix == '.fits'):
    # printing a message
    print (f'ERROR: input file must be a FITS file!')
    # exit
    sys.exit (1)

# file existence check using pathlib module
if not (path_file_input.exists ()):
    # printing a message
    print (f'ERROR: input file "{file_input}" does not exist!')
    # exit
    sys.exit (1)

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

# initial value for maximum value
v_max = -9.99 * 10**10
# initial value for minimum value
v_min = +9.99 * 10**10
# a variable for a sum of all the pixel values
total = 0.0
# a variable for a square of sum of all the pixel values
total_sq = 0.0
# total number of pixels
n = data0.size

# total number of pixels
n = data0.size

# flattening Numpy array (2D --> 1D)
data0_1d = data0.flatten ()

# examining all the pixels
for i in range (n):
    # for calculation of a mean
    total += data0_1d[i]
    # for calculation of variance
    total_sq += data0_1d[i]**2
    # maximum value
    if (data0_1d[i] > v_max):
        v_max = data0_1d[i]
    # minimum value
    if (data0_1d[i] < v_min):
        v_min = data0_1d[i]

# calculation of mean
mean   = total / n

# calculation of variance
var    = total_sq / n - mean**2

# calculation of standard deviation
stddev = var**0.5

# sorting
data0_1d_sorted = sorted (data0_1d)
# median
if (n % 2 == 0):
    median = (data0_1d_sorted[int (n/2) -1] + data0_1d_sorted[int (n/2)]) / 2.0
else:
    median = data0_1d_sorted[int (n/2)]

# printing results of calculations
print (f'# {"filename":20s} {"mean":>8s} {"median":>8s} {"stddev":>8s}', \
       f'{"min":>8s} {"max":>8s}')
print (f'{path_file_input.name:22s} {mean:8.2f} {median:8.2f} {stddev:8.2f}', \
       f'{v_min:8.2f} {v_max:8.2f}')
