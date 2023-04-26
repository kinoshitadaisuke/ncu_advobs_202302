#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/26 21:11:30 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# constructing parser object
desc = 'generating a synthetic FITS image of uniform background'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-b', '--background', type=float, default=1000.0, \
                     help='background level (default: 1000)')
parser.add_argument ('-x', '--xsize', type=int, default=1024, \
                     help='image size in x-axis (default: 1024 pixel)')
parser.add_argument ('-y', '--ysize', type=int, default=1024, \
                     help='image size in y-axis (default: 1024 pixel)')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
sky_background_level = args.background
image_size_x         = args.xsize
image_size_y         = args.ysize
file_output          = args.output

# making pathlib object
path_output = pathlib.Path (file_output)

# checking output file name
if (file_output == ''):
    # printing message
    print (f'ERROR: You need to specify output file name.')
    # exit
    sys.exit ()
# output file must be a FITS file
if not (path_output.suffix == '.fits'):
    # printing message
    print (f'ERROR: Output file must be a FITS file.')
    print (f'ERROR: "{file_output}" is not a FITS file.')
    # exit
    sys.exit ()
# existence check of output file
if (path_output.exists ()):
    # printing message
    print (f'Output file "{file_output}" exists.')
    # exit
    sys.exit ()

# image size
image_size = (image_size_x, image_size_y)

# date/time
now = datetime.datetime.now ().isoformat ()

# command name
command = sys.argv[0]

# printing message
print (f'#')
print (f'# input parameters')
print (f'#')
print (f'#  image size                = {image_size_x} x {image_size_y}')
print (f'#  mean sky background level = {sky_background_level} ADU')
print (f'#')

# printing status
print (f'# now, generating image...')

# generating sky background data
data = numpy.full (shape=image_size, fill_value=sky_background_level, \
                   dtype='float64')

# printing status
print (f'# finished generating image!')
print (f'#')

# printing status
print (f'# now, generating FITS header...')

# preparing a FITS header
header = astropy.io.fits.PrimaryHDU ().header

# adding comments to the header
header['history'] = f'FITS file created by the command "{command}"'
header['history'] = f'Updated on {now}'
header['comment'] = f'synthetic astronomical image of uniform background'
header['comment'] = f'Options given:'
header['comment'] = f'  image size = {image_size_x} x {image_size_y}'
header['comment'] = f'  mean sky background level = {sky_background_level} ADU'

# printing status
print (f'# finished generating FITS header!')
print (f'#')

# printing status
print (f'# now, writing output FITS file...')

# writing a FITS file
astropy.io.fits.writeto (file_output, data, header=header)

# printing status
print (f'# finished writing output FITS file!')
print (f'#')
