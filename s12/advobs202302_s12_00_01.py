#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/26 21:21:25 (CST) daisuke>
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
desc   = 'Printing the header of a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', default='', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
file_fits  = args.file

# making pathlib object
path_fits = pathlib.Path (file_fits)

# checking input file
# if the file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing error message
    print (f'ERROR: Input file must be FITS files!')
    # exit the script
    sys.exit ()
# if the file does not exist, then stop the script
if not (path_fits.exists ()):
    # printing error message
    print (f'ERROR: Input file FITS file does not exist!')
    # exit the script
    sys.exit ()

# function to read FITS header
def read_fits_header (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header
    # returning header
    return (header)

# reading FITS header
header = read_fits_header (file_fits)

# printing header
print (repr (header))
