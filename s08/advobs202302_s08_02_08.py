#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 23:22:31 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Image subtraction for multiple FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019',
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', help='accepted data type')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=0.0, help='accepted exposure time (default: 0.0)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted data type')
parser.add_argument ('-s', '--subtrahend', help='subtrahend (FITS file)')
parser.add_argument ('minuend', nargs='+', help='minuend (FITS file)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_minuend    = args.minuend
file_subtrahend = args.subtrahend
datatype        = args.datatype
exptime         = args.exptime
filtername      = args.filtername

# command name
command = sys.argv[0]

# making a pathlib object
path_subtrahend = pathlib.Path (file_subtrahend)

# if the extension of the file is not '.fits', then skip
if (path_subtrahend.suffix != '.fits'):
    # printing error message
    print (f'ERROR: subtrahend file must be FITS file!')
    print (f'ERROR: the file "{file_subtrahend}" is not a FITS file!')
    # exiting
    sys.exit ()

# existence check of subtrahend FITS file
if not (path_subtrahend.exists ()):
    # printing error message
    print (f'ERROR: subtrahend file does not exist!')
    print (f'ERROR: file "{file_fits}" does not exist!')
    # exiting
    sys.exit ()

#
# function to open a FITS file and read both header and data
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

#
# function to open a FITS file and read the header
#
def read_fits_header_only (file_fits):
    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        # header
        header0 = hdu0.header
    # returning header and data
    return (header0)

#
# reading subtrahend FITS file
#

# printing status
print (f'# now, reading the file "{file_subtrahend}"...')

# opening FITS file
(header_subtrahend, data_subtrahend) = read_fits (file_subtrahend)

# printing status
print (f'# finished reading the file "{file_subtrahend}"!')
print (f'#')
print (f'#')

# processing files
for file_minuend in list_minuend:
    # making a pathlib object
    path_minuend = pathlib.Path (file_minuend)

    # if the extension of the file is not '.fits', then skip
    if (path_minuend.suffix != '.fits'):
        continue

    # existence check of FITS file
    if not (path_minuend.exists ()):
        # if FITS file does not exist, then skip
        continue

    #
    # reading minuend FITS file
    #

    # opening FITS file and read header and data
    header_minuend = read_fits_header_only (file_minuend)

    # checking image type, exposure time, and filter name
    # if FITS file is not what you want, then skip
    if ('FILTER' in header_minuend):
        if not ( (header_minuend['IMAGETYP'] == datatype) \
                 and (header_minuend['EXPTIME'] == exptime) \
                 and (header_minuend['FILTER'] == filtername) ):
            continue
    else:
        if not ( (header_minuend['IMAGETYP'] == datatype) \
                 and (header_minuend['EXPTIME'] == exptime) ):
            continue
        
    # output file name
    file_output = path_minuend.stem + '_d.fits'

    # date/time
    now = datetime.datetime.now ().isoformat ()

    # printing information
    print (f'# Arithmetic operation being done:')
    print (f'#   {file_minuend} - {file_subtrahend}')
    print (f'#        ==> {file_output}')

    # opening FITS file and read header and data
    (header_minuend, data_minuend) = read_fits (file_minuend)
    
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
    astropy.io.fits.writeto (file_output, data_subtracted, \
                             header=header_minuend)

    # printing status
    print (f'# finished writing a FITS file {file_output}!')
    print (f'#')
    print (f'#')
