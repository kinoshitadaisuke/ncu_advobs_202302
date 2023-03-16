#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 14:19:31 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc   = 'opening FITS files and reading image data'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='name of FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.file

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
    print (f'{data0}')
