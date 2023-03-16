#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 20:25:13 (CST) daisuke>
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
desc   = 'Subtraction of one FITS file from another'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits0', help='name of FITS file 0')
parser.add_argument ('fits1', help='name of FITS file 1')
parser.add_argument ('-o', help='output FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_fits0  = args.fits0
file_fits1  = args.fits1
file_output = args.o

# if the extension of the file is not '.fits', then skip
if (file_fits0[-5:] != '.fits'):
    print (f'ERROR: "{file_fits0}" is not a FITS file!')
    sys.exit (1)
if (file_fits1[-5:] != '.fits'):
    print (f'ERROR: "{file_fits1}" is not a FITS file!')
    sys.exit (1)

# date/time of now
datetime_now = datetime.datetime.utcnow ()
datetime_str = "%04d-%02d-%02dT%02d:%02d:%06.3f" \
    % (datetime_now.year, datetime_now.month, datetime_now.day, \
       datetime_now.hour, datetime_now.minute, \
       datetime_now.second + datetime_now.microsecond * 10**-6)

# opening FITS file 0
with astropy.io.fits.open (file_fits0) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]
    
    # header of primary HDU
    header0 = hdu0.header

    # data of primary HDU
    data0 = hdu0.data

# opening FITS file 1
with astropy.io.fits.open (file_fits1) as hdu_list:
    # primary HDU
    hdu1 = hdu_list[0]
    
    # header of primary HDU
    header1 = hdu1.header

    # data of primary HDU
    data1 = hdu1.data
    
# subtraction
diff = data0 - data1

# adding comments and history to header
header0['comment'] = f'image subtracted by command {sys.argv[0]}'
header0['comment'] = f'calculation: {file_fits0} - {file_fits1}'
header0['history'] = f'image subtraction on {datetime_str}'

# writing a FITS file
astropy.io.fits.writeto (file_output, data=diff, header=header0)
