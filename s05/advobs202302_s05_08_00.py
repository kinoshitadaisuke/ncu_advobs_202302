#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 19:50:16 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = 'generating a synthetic image simulating sky background'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-b', '--background', type=float, default=1000.0, \
                     help='background level (default: 1000)')
parser.add_argument ('-s', '--sigma', type=float, default=10.0, \
                     help='noise level (default: 10)')
parser.add_argument ('-x', '--xsize', type=int, default=512, \
                     help='image size in x-axis (default: 512)')
parser.add_argument ('-y', '--ysize', type=int, default=512, \
                     help='image size in y-axis (default: 512)')
parser.add_argument ('fits', help='output FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
sky_background = args.background
noise          = args.sigma
image_size_x   = args.xsize
image_size_y   = args.ysize
file_output    = args.fits

# if file name is not given, then stop the script
if (file_output == ''):
    print (f'ERROR: file name is not given!')
    sys.exit ()

# image size
image_size = (image_size_x, image_size_y)

# date/time of now
datetime_now = datetime.datetime.utcnow ()
datetime_str = "%04d-%02d-%02dT%02d:%02d:%06.3f" \
    % (datetime_now.year, datetime_now.month, datetime_now.day, \
       datetime_now.hour, datetime_now.minute, \
       datetime_now.second + datetime_now.microsecond * 10**-6)

# initialisation of random number generator
rng = numpy.random.default_rng ()

# generation of numpy array of size (image_size_x, image_size_y)
image0 = rng.normal (loc=sky_background, scale=noise, size=image_size)

# making a new FITS header
header0 = astropy.io.fits.PrimaryHDU ().header

# adding comments and history to header
header0['comment'] = f'synthetic image generated by command {sys.argv[0]}'
header0['comment'] = f'image generation parameters:'
header0['comment'] = f'  image size in X      = {image_size_x}'
header0['comment'] = f'  image size in Y      = {image_size_y}'
header0['comment'] = f'  mean sky background  = {sky_background}'
header0['comment'] = f'  stddev of background = {noise}'
header0['history'] = f'generated on {datetime_str}'

# writing a FITS file
astropy.io.fits.writeto (file_output, data=image0, header=header0)
