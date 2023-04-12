#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 14:42:03 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'carrying out dark subtraction for object and flatfield frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
default_exptime_keyword  = 'EXPTIME'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-d', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.datatype
keyword_exptime  = args.exptime
list_files       = args.files

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# function to read FITS header
def read_fits_header (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header
    # returning header
    return (header)

# function to read FITS data
def read_fits_data (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # data of primary HDU
        data = hdu_list[0].data
    # returning data
    return (data)

# processing FITS files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the extension of the file is not '.fits', the we skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print (f'### file "{file_fits}" is not a FITS file! skipping...')
        # skipping
        continue

    # reading FITS header
    header = read_fits_header (file_fits)
    
    # data type
    if (keyword_datatype in header):
        datatype = header[keyword_datatype]
    else:
        datatype = "__NONE__"

    # exposure time
    if (keyword_exptime in header):
        exptime = header[keyword_exptime]
    else:
        exptime = -999.99

    # filter name
    if (keyword_filter in header):
        filter_name = header[keyword_filter]
    else:
        filter_name = "__NONE__"

    # if the data type is not "LIGHT" or "FLAT", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        continue

    # appending file name to the dictionary
    dict_target[file_fits] = {}
    dict_target[file_fits]['filter']  = filter_name
    dict_target[file_fits]['exptime'] = exptime

#
# dark subtraction
#

print (f'#')
print (f'# {len (dict_target)} files are found for dark subtraction')
print (f'#')
print (f'# Processing each FITS file...')
print (f'#')

# processing each FITS file
for file_raw in sorted (dict_target.keys () ):
    # making pathlib object
    path_raw = pathlib.Path (file_raw)
    
    # file name of dark subtracted FITS file
    file_subtracted = path_raw.stem + '_d.fits'
    
    print (f'# subtracting dark from {file_raw}')
    print (f'#   {file_raw} ==> {file_subtracted}')

    # printing status
    print (f'#     now, reading raw data from {file_raw}...')
    
    # reading FITS header
    header = read_fits_header (file_raw)

    # reading FITS data
    data_raw = read_fits_data (file_raw)

    # printing status
    print (f'#     finished reading raw data from {file_raw}!')
    
    # finding EXPTIME keyword
    if ('EXPTIME' in header):
        exptime = header[keyword_exptime]
    else:
        # printing status
        print (f'### ERROR: EXPTIME keyword not found in {file_raw}!')
        # exit
        sys.exit ()

    # dark file name
    file_dark = f'dark_{int (exptime):04d}.fits'

    # making pathlib object
    path_dark = pathlib.Path (file_dark)

    # checking whether dark file exists
    # if dark file does not exist, then stop the script
    if not (path_dark.exists () ):
        # printing message
        print (f'### ERROR: The dark file "{file_dark}" is NOT found.')
        print (f'### ERROR: Check the data!')
        # exit
        sys.exit ()

    # reading FITS header (dark)
    header_dark = read_fits_header (file_dark)

    # checking EXPTIME keyword of dark frame
    if ('EXPTIME' in header_dark):
        exptime_dark = header_dark [keyword_exptime]
    else:
        # printing message
        print (f'### ERROR: EXPTIME keyword not found in "{file_dark}"!')
        print (f'### ERROR: Check the data!')
        # exit
        sys.exit ()

    # if exptime_dark is not the same as exptime, then stop the script
    if not (exptime == exptime_dark):
        # printing message
        print (f'### ERROR: Exposure times of raw and dark frames are NOT same.')
        print (f'### ERROR: Check the data!')
        # exit
        sys.exit ()
        
    # printing status
    print (f'#     now, reading dark data from "{file_dark}"...')

    # reading FITS data (dark)
    data_dark = read_fits_data (file_dark)
    
    # printing status
    print (f'#     finished reading dark data from "{file_dark}"!')

    # printing status
    print (f'#     now, subtracting dark from "{file_raw}"...')

    # dark subtraction
    data_subtracted = data_raw - data_dark

    # printing status
    print (f'#     finished subtracting dark from "{file_raw}"!')

    # printing status
    print (f'#     mean value of raw data             =', \
           f'{numpy.ma.mean (data_raw):8.1f} ADU')
    print (f'#     mean value of dark data            =', \
           f'{numpy.ma.mean (data_dark):8.1f} ADU')
    print (f'#     mean value of dark subtracted data =', \
           f'{numpy.ma.mean (data_subtracted):8.1f} ADU')

    # adding comments to new FITS file
    header['history'] = f'FITS file created by the command "{command}"'
    header['history'] = f'Updated on {now}'
    header['comment'] = f'dark subtraction was carried out'
    header['comment'] = f'raw data: {file_raw}'
    header['comment'] = f'dark data: {file_dark}'
    header['comment'] = f'dark subtracted data: {file_subtracted}'

    # printing status
    print (f'#     now, writing new file "{file_subtracted}"...')

    # writing a new FITS file
    astropy.io.fits.writeto (file_subtracted, data_subtracted, header=header)

    # printing status
    print (f'#     finished writing new file "{file_subtracted}" done!')
