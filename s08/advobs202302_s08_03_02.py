#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/06 14:46:44 (CST) daisuke>
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
desc   = 'Dark subtraction for multiple FITS files of different exposure time'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019',
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--date', default='2000-01-01', \
                     help='accepted date in YYYY-MM-DD (default: 2000-01-01)')
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', help='accepted data type')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=-1.0, help='accepted exposure time (default: -1)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted data type')
parser.add_argument ('-s', '--subtrahend', default='dark_', \
                     help='prefix of subtrahend FITS file (default: "dark_")')
parser.add_argument ('minuend', nargs='+', help='minuend (FITS file)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_minuend     = args.minuend
file_dark_prefix = args.subtrahend
date             = args.date
datatype         = args.datatype
exptime          = args.exptime
filtername       = args.filtername

# command name
command = sys.argv[0]

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

# processing files
for file_minuend in list_minuend:
    # making a pathlib object
    path_minuend = pathlib.Path (file_minuend)

    # if the extension of the file is not '.fits', then skip
    if (path_minuend.suffix != '.fits'):
        # printing message
        print (f'The file "{file_minuend}" is not a FITS file!')
        print (f'Skipping...')
        # if the file is not a FITS file, then skip
        continue

    # existence check of FITS file
    if not (path_minuend.exists ()):
        # printing message
        print (f'The file "{file_minuend}" does not exist!')
        print (f'Skipping...')
        # if FITS file does not exist, then skip
        continue

    #
    # reading minuend FITS file
    #

    # opening FITS file and read header
    header_minuend = read_fits_header_only (file_minuend)

    # if the date of data acquisition is different from what we need, then skip
    if (header_minuend['DATE-OBS'] != date):
        continue

    # if the data type is not what we need, then skip
    if (header_minuend['IMAGETYP'] != datatype):
        continue

    # if the exposure time is not what we need, then skip
    if ( (exptime >= 0.0) and (header_minuend['EXPTIME'] != exptime) ):
        continue

    # if the filter is not what we need, then skip
    if ( ('FILTER' in header_minuend) \
         and (header_minuend['FILTER'] != filtername) \
         and (filtername != '__NONE__') ):
        continue

    # printing message
    print (f'# Now, processing the file "{file_minuend}"...')
    print (f'#   now reading the data from "{file_minuend}"...')
    
    # opening FITS file and read header and data
    (header_minuend, data_minuend) = read_fits (file_minuend)
    
    # printing message
    print (f'#   finished reading the data from "{file_minuend}"!')

    #
    # reading subtrahend FITS file
    #

    # exposure time of the FITS file
    target_exptime = header_minuend['EXPTIME']

    # file name of combined dark frame
    file_subtrahend = f'{file_dark_prefix}{int (target_exptime):04d}.fits'

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

    # printing message
    print (f'#   now reading the data from "{file_subtrahend}"...')

    # opening FITS file
    (header_subtrahend, data_subtrahend) = read_fits (file_subtrahend)

    # printing message
    print (f'#   finished reading the data from "{file_subtrahend}"!')

    #
    # image subtraction
    #

    # output file name
    file_output = path_minuend.stem + '_d.fits'

    # date/time
    now = datetime.datetime.now ().isoformat ()

    # printing information
    print (f'#   arithmetic operation being done:')
    print (f'#     {file_minuend} - {file_subtrahend}')
    print (f'#          ==> {file_output}')

    # printing status
    print (f'#   now, subtracting {file_subtrahend} from {file_minuend}...')

    # calculation for image subtraction
    data_subtracted = data_minuend - data_subtrahend

    # printing status
    print (f'#   finished subtracting {file_subtrahend} from {file_minuend}!')

    #
    # writing output FITS file
    #

    # printing status
    print (f'#   now, writing a FITS file "{file_output}"...')

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
    print (f'#   finished writing a FITS file {file_output}!')
    print (f'# Finished processing the file "{file_minuend}"!')
    print (f'#')
