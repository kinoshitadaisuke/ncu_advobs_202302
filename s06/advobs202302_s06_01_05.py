#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 11:28:03 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'listing all the keywords in a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_fits = args.file

# if input file is not a FITS file, then skip
if not (file_fits[-5:] == '.fits'):
    # printing a message
    print (f'The file "{file_fits}" is not a FITS file!')
    # stopping the script
    sys.exit (1)
    
# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

# obtaining a list of all the keywords in a FITS file
list_keywords = header0.keys ()

# printing the list of all the keywords in a FITS file
print (f'Keywords in a FITS file "{file_fits}":')
for keyword in sorted (list_keywords):
    # if empty keyword, then skip
    if (keyword == ''):
        continue
    # printing keyword
    print (f'  {keyword}')
