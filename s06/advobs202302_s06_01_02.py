#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 20:36:34 (CST) daisuke>
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
desc   = 'Checking keywords IMAGETYP and EXPTIME of multiple FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input FITS files
list_fits = args.files

# processing FITS files one-by-one
for file_fits in list_fits:
    # making pathlib object
    path_file_fits = pathlib.Path (file_fits)
    
    # if input file is not a FITS file, then skip
    if not (path_file_fits.suffix == '.fits'):
        # printing a message
        print (f'The file "{file_fits}" is not a FITS file!')
        # moving to next file
        continue
    
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        
        # reading header
        header0 = hdu0.header

    # check of existence of IMAGETYP keyword
    if not ('IMAGETYP' in header0):
        # printing a message
        print (f'A keyword IMAGETYP does not exist in the file "{file_fits}".')
        # moving to next file
        continue

    # check of existence of EXPTIME keyword
    if not ('EXPTIME' in header0):
        # printing a message
        print (f'A keyword EXPTIME does not exist in the file "{file_fits}".')
        # moving to next file
        continue

    # printing values of IMAGETYP and EXPTIME keywords
    print (f'{file_fits} : {header0["IMAGETYP"]} ({header0["EXPTIME"]} sec)')
