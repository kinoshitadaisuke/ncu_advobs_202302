#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 22:40:34 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Image subtraction'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('minuend', help='minuend (FITS file)')
parser.add_argument ('-s', '--subtrahend', help='subtrahend (FITS file)')
parser.add_argument ('-o', '--output', help='output file (FITS file)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_minuend    = args.minuend
file_subtrahend = args.subtrahend
file_output     = args.output

# command name
command = sys.argv[0]

# checking input FITS files
for file_fits in (file_minuend, file_subtrahend):
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    # if input file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print (f'ERROR: input file must be FITS files!')
        print (f'ERROR: the file "{file_fits}" is not a FITS file!')
        # exit the script
        sys.exit ()
    # if input FITS file does not exist, then stop the script
    if not (path_fits.exists ()):
        # printing error message
        print (f'ERROR: input file does not exist!')
        print (f'ERROR: input file = "{file_fits}"')
        # exit the script
        sys.exit ()

# checking output FITS files
# making pathlib object
path_fits = pathlib.Path (file_output)
# if output file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing error message
    print (f'ERROR: output file must be FITS files!')
    print (f'ERROR: the file "{file_fits}" is not a FITS file!')
    # exit the script
    sys.exit ()
# if input FITS file does not exist, then stop the script
if (path_fits.exists ()):
    # printing error message
    print (f'ERROR: output file exists!')
    print (f'ERROR: output file = "{file_fits}"')
    # exit the script
    sys.exit ()

#
# function to open a FITS file
#
def read_fits (file_fits):
    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        # header
        header0 = hdu0.header
        # data
        data0 = hdu0.data
    # returning header and data
    return (header0, data0)

# date/time
now = datetime.datetime.now ().isoformat ()

# printing information
print (f'# Arithmetic operation being done:')
print (f'#   {file_minuend} - {file_subtrahend}')
print (f'#        ==> {file_output}')

#
# reading minuend FITS file
#

# printing status
print (f'# now, reading the file "{file_minuend}"...')

# opening FITS file
(header_minuend, data_minuend) = read_fits (file_minuend)

# printing status
print (f'# finished reading the file "{file_minuend}"!')

#
# reading subtrahend FITS file
#

# printing status
print (f'# now, reading the file "{file_subtrahend}"...')

# opening FITS file
(header_subtrahend, data_subtrahend) = read_fits (file_subtrahend)

# printing status
print (f'# finished reading the file "{file_subtrahend}"!')

#
# image subtraction
#

# printing status
print (f'# now, subtracting {file_subtrahend} from {file_minuend}...')

# calculation for image subtraction
data_subtracted = data_minuend - data_subtrahend

# printing status
print (f'# finished subtracting {file_subtrahend} from {file_minuend}!')

#
# writing output FITS file
#

# printing status
print (f'# now, writing a FITS file "{file_output}"...')

# adding comments to the header
header_minuend['history'] = f'FITS file created by the command "{command}"'
header_minuend['history'] = f'Updated on {now}'
header_minuend['comment'] = f'Image subtraction:'
header_minuend['comment'] = f'  minuend    = {file_minuend}'
header_minuend['comment'] = f'  subtrahend = {file_subtrahend}'
header_minuend['comment'] = f'  output     = {file_output}'

# writing a new FITS file
astropy.io.fits.writeto (file_output, data_subtracted, header=header_minuend)

# printing status
print (f'# finished writing a FITS file {file_output}!')
