#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 14:24:21 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc   = 'opening FITS files, reading image data, and printing a pixel value'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='name of FITS file')
parser.add_argument ('-x', type=int, default=1, help='pixel value along X-axis')
parser.add_argument ('-y', type=int, default=1, help='pixel value along Y-axis')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.file
x         = args.x
y         = args.y

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header
    
    # data of primary HDU
    data0 = hdu0.data

    # printing image data
    print (f'filename = {file_fits}')
    print (f'  pixel value at (x, y)=({x}, {y}): {data0[x,y]} ADU')
