#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 11:57:19 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Reading image data from a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input = args.file

# if input file is not a FITS file, then skip
if not (file_input[-5:] == '.fits'):
    # printing a message
    print (f'ERROR: input file must be a FITS file!')
    # exit
    sys.exit (1)

# file existence check using pathlib module
path_file_input = pathlib.Path (file_input)
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

# printing basic information of data
print (f'{file_input}')
print (f'  object type             = {type (data0)}')
print (f'  dimensions of data      = {data0.ndim}')
print (f'  shape of data           = {data0.shape}')
print (f'  number of pixels        = {data0.size} pixels')
print (f'  data type of pixel data = {data0.dtype}')
