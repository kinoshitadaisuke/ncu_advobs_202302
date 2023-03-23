#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 14:36:42 (CST) daisuke>
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
desc   = 'Calculating a simple mean of a FITS file'
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

# a variable for calculation of a sum of all the pixel values
total = 0.0

# total number of pixels
n = data0.size

# adding all the pixel values
for i in range (len (data0) ):
    for j in range (len (data0[i]) ):
        # adding pixel value data0[i,j] to the total
        total += data0[i,j]

# calculation of a simple mean
mean = total / n

# printing result
print (f'{file_input}')
print (f'  sum of all the pixel values = {total:g}')
print (f'  number of pixels            = {n:11d}')
print (f'  mean                        = {mean:11.3f}')
