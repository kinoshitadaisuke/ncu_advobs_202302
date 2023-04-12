#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/13 02:07:50 (CST) daisuke>
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
desc   = 'carrying out flatfielding'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
default_exptime_keyword  = 'EXPTIME'
default_timeobs_keyword  = 'TIME-OBS'
default_dateobs_keyword  = 'DATE-OBS'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-d', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('-t', '--timeobs', default=default_timeobs_keyword, \
                     help='FITS keyword for time-obs')
parser.add_argument ('-y', '--dateobs', default=default_dateobs_keyword, \
                     help='FITS keyword for date-obs')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.datatype
keyword_exptime  = args.exptime
keyword_timeobs  = args.timeobs
keyword_dateobs  = args.dateobs
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
for file_darksub in list_files:
    # making pathlib object
    path_darksub = pathlib.Path (file_darksub)
    
    # if the extension of the file is not '.fits', the we skip
    if not (path_darksub.suffix == '.fits'):
        # printing message
        print (f'### file "{file_darksub}" is not a FITS file! skipping...')
        # skipping
        continue

    # reading FITS header
    header = read_fits_header (file_darksub)
    
    # data type
    if (keyword_datatype in header):
        datatype = header[keyword_datatype]
    else:
        datatype = "__NONE__"
    # exptime
    if (keyword_exptime in header):
        exptime = header[keyword_exptime]
    else:
        exptime = -999.99
    # filter name
    if (keyword_filter in header):
        filter_name = header[keyword_filter]
    else:
        filter_name = "__NONE__"
    # date-obs
    if (keyword_dateobs in header):
        date_obs = header[keyword_dateobs]
    else:
        date_obs = "__NONE__"
    # time-obs
    if (keyword_timeobs in header):
        time_obs = header[keyword_timeobs]
    else:
        time_obs = "__NONE__"

    # if the data type is not "LIGHT", then we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # if the file name is not "*_d.fits", then we skip the file
    if not (path_darksub.stem[-2:] == '_d'):
        continue

    # appending file name to the dictionary
    dict_target[file_darksub] = {}
    dict_target[file_darksub]['filter']  = filter_name
    dict_target[file_darksub]['exptime'] = exptime

# dark subtraction

print (f'#')
print (f'# Processing each FITS file...')
print (f'#')

# processing each FITS file
for file_darksub in sorted (dict_target.keys () ):
    # making pathlib object
    path_darksub = pathlib.Path (file_darksub)
    
    # file names
    file_flatfielded = path_darksub.stem + 'f.fits'
    file_nflat       = 'nflat_' + dict_target[file_darksub]['filter'] + '.fits'

    # if normalised flatfield does not exist, then stop the script
    path_nflat = pathlib.Path (file_nflat)
    if not (path_nflat.exists () ):
        print (f'The flatfield file "{file_nflat}" does not exist.')
        print (f'Check the data!')
        sys.exit ()

    # printing status
    print (f'# dividing {file_darksub} by {file_nflat}...')
    print (f'#   {file_darksub} ==> {file_flatfielded}')

    # printing status
    print (f'#   now, reading data from "{file_darksub}"...')
    
    # reading FITS header and data
    header_darksub = read_fits_header (file_darksub)
    data_darksub   = read_fits_data (file_darksub)

    # printing status
    print (f'#   finished reading data from "{file_darksub}"!')

    # printing status
    print (f'#   now, reading data from "{file_nflat}"...')
    
    # reading FITS header and data
    data_nflat = read_fits_data (file_nflat)

    # printing status
    print (f'#   finished reading data from "{file_nflat}"!')

    # printing status
    print (f'#   now, dividing {file_darksub} by {file_nflat}...')

    # flatfielding
    data_flatfielded = data_darksub / data_nflat

    # printing status
    print (f'#   finished dividing {file_darksub} by {file_nflat}!')
    
    # printing information
    print (f'#     {file_nflat:28s} :', \
           f'mean value = {numpy.mean (data_nflat):8.2f} ADU')
    print (f'#     {file_darksub:28s} :', \
           f'mean value = {numpy.mean (data_darksub):8.2f} ADU')
    print (f'#     {file_flatfielded:28s} :', \
           f'mean value = {numpy.mean (data_flatfielded):8.2f} ADU')

    # adding comments to new FITS file
    header['history'] = f'FITS file created by the command "{command}"'
    header['history'] = f'Updated on {now}'
    header['comment'] = f'flatfielding was carried out'
    header['comment'] = f'dark-subtracted data: {file_darksub}'
    header['comment'] = f'normalised flatfield data: {file_nflat}'
    header['comment'] = f'flatfielded data: {file_flatfielded}'

    # printing status
    print (f'#   now, writing new file "{file_flatfielded}"...')

    # writing a new FITS file
    astropy.io.fits.writeto (file_flatfielded, data_flatfielded, header=header)

    # printing status
    print (f'#   finished writing new file "{file_flatfielded}"!')
