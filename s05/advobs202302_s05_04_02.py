#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 13:57:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc = 'opening a FITS file and printing value of selected header keyword'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-k', '--keyword', default='BITPIX', \
                     help='keyword (e.g. BITPIX, NAXIS1, EXPTIME, FILTER)')
parser.add_argument ('file', help='name of FITS file')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.file
keyword   = args.keyword

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # header of primary HDU
    header0 = hdu0.header

    # printing specific keywords and their values in FITS header
    print (f'{file_fits}')
    print (f'  {keyword:8s} = {header0[keyword]}')
