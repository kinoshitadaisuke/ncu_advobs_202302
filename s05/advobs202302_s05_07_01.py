#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 19:17:49 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc   = 'adding a new FITS keyword'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits', help='name of FITS file to read')
parser.add_argument ('-o', help='name of output FITS file')
parser.add_argument ('-k', help='new keyword name')
parser.add_argument ('-v', type=float, help='value of new keyword')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_fits = args.fits
file_new  = args.o
keyword   = args.k
value     = args.v

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header
    
    # data of primary HDU
    data0 = hdu0.data

    # adding a new keyword to header
    header0[keyword] = value

    # writing new FITS file
    astropy.io.fits.writeto (file_new, data=data0, header=header0)
