#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 20:09:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Normalising a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits', help='name of a FITS file')
parser.add_argument ('-o', help='output FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_input  = args.fits
file_output = args.o

# if the extension of the file is not '.fits', then skip
if (file_input[-5:] != '.fits'):
    print (f'ERROR: "{file_input}" is not a FITS file!')
    sys.exit (1)

# date/time of now
datetime_now = datetime.datetime.utcnow ()
datetime_str = "%04d-%02d-%02dT%02d:%02d:%06.3f" \
    % (datetime_now.year, datetime_now.month, datetime_now.day, \
       datetime_now.hour, datetime_now.minute, \
       datetime_now.second + datetime_now.microsecond * 10**-6)

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # data of primary HDU
    data0 = hdu0.data

    # calculations of mean
    mean = numpy.mean (data0)

    # normalisation
    normalised = data0 / mean

    # adding comments and history to header
    header0['comment'] = f'image normalised by command {sys.argv[0]}'
    header0['comment'] = f'mean value of original image = {mean} ADU'
    header0['history'] = f'normalised on {datetime_str}'

    # writing a FITS file
    astropy.io.fits.writeto (file_output, data=normalised, header=header0)
