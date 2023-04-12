#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 14:17:51 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'listing object and flatfield frames'
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

# printing FITS file list
print (f'List of FITS files for dark subtraction:')
for file_fits in sorted (dict_target.keys () ):
    print (f'  {file_fits} ({dict_target[file_fits]["filter"]},', \
           f'{dict_target[file_fits]["exptime"]} sec)')
print (f'Total number of FITS files for dark subtraction:')
print (f'  {len (dict_target)} files')
