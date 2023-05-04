#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/04 16:34:49 (CST) daisuke>
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

# importing photutils module
import photutils.datasets

# constructing parser object
desc   = 'generating a synthetic FITS image of sky background and a star'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-b', '--background', type=float, default=1000.0, \
                     help='background level (default: 1000)')
parser.add_argument ('-s', '--sigma', type=float, default=10.0, \
                     help='noise level (default: 10)')
parser.add_argument ('-x', '--xsize', type=int, default=1024, \
                     help='image size in x-axis (default: 1024 pixel)')
parser.add_argument ('-y', '--ysize', type=int, default=1024, \
                     help='image size in y-axis (default: 1024 pixel)')
parser.add_argument ('-p', '--starx', type=float, default=512, \
                     help='location of a star on X-axis (default: 512 pixel)')
parser.add_argument ('-q', '--stary', type=float, default=512, \
                     help='location of a star on Y-axis (default: 512 pixel)')
parser.add_argument ('-f', '--flux', type=float, default=100000, \
                     help='flux of a synthetic star (default: 100000 ADU)')
parser.add_argument ('-w', '--fwhm', type=float, default=5.0, \
                     help='FWHM of a synthetic star (default: 5 pixel)')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
sky_background_level = args.background
noise_level          = args.sigma
image_size_x         = args.xsize
image_size_y         = args.ysize
star_x               = args.starx
star_y               = args.stary
star_flux            = args.flux
star_fwhm            = args.fwhm
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
print (f'#  noise level (stddev)      = {noise_level} ADU')
print (f'#  star position in X        = {star_x} pixel')
print (f'#  star position in Y        = {star_y} pixel')
print (f'#  star flux                 = {star_flux} ADU')
print (f'#  star FWHM                 = {star_fwhm} pixel')
print (f'#')

# printing status
print (f'# now, generating sky background...')

# generating sky background data
skybg = photutils.datasets.make_noise_image (image_size, \
                                            distribution='gaussian', \
                                            mean=sky_background_level, \
                                            stddev=noise_level)

# printing status
print (f'# finished generating sky background!')
print (f'#')

# printing status
print (f'# now, generating a synthetic star...')

# making a source table
fwhm_sigma = 2.0 * numpy.sqrt (2.0 * numpy.log (2.0) )
source_table = astropy.table.Table ()
source_table['x_0']   = [star_x]
source_table['y_0']   = [star_y]
source_table['flux']  = [star_flux]
source_table['sigma'] = [star_fwhm / fwhm_sigma]

# generating a synthetic star
star = photutils.datasets.make_gaussian_prf_sources_image (image_size, \
                                                           source_table)

# printing status
print (f'# finished generating a synthetic star!')
print (f'#')

# printing status
print (f'# now, generating synthetic image...')

# image data = sky background + star
data = skybg + star

# printing status
print (f'# finished generating synthetic image!')
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
header['comment'] = f'  image size          = {image_size_x} x {image_size_y}'
header['comment'] = f'  mean sky background = {sky_background_level} ADU'
header['comment'] = f'  noise level         = {noise_level} ADU'
header['comment'] = f'  star position in X  = {star_x} pixel'
header['comment'] = f'  star position in Y  = {star_y} pixel'
header['comment'] = f'  star flux           = {star_flux} ADU'
header['comment'] = f'  star FWHM           = {star_fwhm} pixel'

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
