#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 13:07:33 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc   = 'opening FITS files and printing HDU information'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='name of a FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.file

# opening a FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # printing HDU list information
    print (f'{hdu_list.info ()}')
