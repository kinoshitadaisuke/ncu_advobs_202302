#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 18:47:20 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Creating a new FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits', help='output FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_output = args.fits

# shape of image data
image_size = (256, 256)

# generating image data
data0 = numpy.zeros (image_size, dtype=numpy.float64)

# generating FITS header
header0 = astropy.io.fits.Header ()

# making primary HDU
hdu0 = astropy.io.fits.PrimaryHDU (data=data0, header=header0)

# making HDU list
hdu_list = astropy.io.fits.HDUList (hdus=[hdu0])

# writing a new FITS file
hdu_list.writeto (file_output)
