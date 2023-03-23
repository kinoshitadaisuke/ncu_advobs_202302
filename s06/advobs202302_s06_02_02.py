#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 20:42:12 (CST) daisuke>
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
parser.add_argument ('-x', type=int, default=0, \
                     help='x-coordinate of pixel (default=0)')
parser.add_argument ('-y', type=int, default=0, \
                     help='y-coordinate of pixel (default=0)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input = args.file
x          = args.x
y          = args.y

# making pathlib object
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

# printing pixel value of specified pixel
print (f'{file_input}')
print (f'  value[x={x},y={x}] = {data0[x,y]}')
