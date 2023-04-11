#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 01:00:28 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Checking dark frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_exptime_keyword  = 'EXPTIME'
default_datatype_keyword = 'IMAGETYP'
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time (default: EXPTIME)')
parser.add_argument ('-t', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type (default: IMAGETYP)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_exptime  = args.exptime
keyword_datatype = args.datatype
list_files       = args.files

# declaring a dictionary for filter names
dict_exptime_object = {}
dict_exptime_flat   = {}
dict_exptime_dark   = {}

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

    # reading header of FITS file
    (header) = read_fits_header (file_fits)
    
    # data type
    if (keyword_datatype in header):
        datatype = header[keyword_datatype]
    else:
        datatype = "__NONE__"

    # if the data type is not "LIGHT" or "FLAT" or "DARK", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') \
             or (datatype == 'DARK') ):
        continue

    # exposure time
    if (keyword_exptime in header):
        exptime = float (header[keyword_exptime])
    else:
        exptime = -999.99

    # checking data type
    if (datatype == 'LIGHT'):
        # object frames
        if not (exptime in dict_exptime_object):
            # appending exptime to the dictionary "dict_exptime_object"
            dict_exptime_object[exptime] = 1
        else:
            # add 1
            dict_exptime_object[exptime] += 1
    elif (datatype == 'FLAT'):
        # flatfield frames
        if not (exptime in dict_exptime_flat):
            # appending exptime to the dictionary "dict_exptime_flat"
            dict_exptime_flat[exptime] = 1
        else:
            # add 1
            dict_exptime_flat[exptime] += 1
    elif (datatype == 'DARK'):
        # dark frames
        if not (exptime in dict_exptime_dark):
            # appending exptime to the dictionary "dict_exptime_dark"
            dict_exptime_dark[exptime] = 1
        else:
            # add 1
            dict_exptime_dark[exptime] += 1

# list of exposure times used for the observation
list_exptime = list ( dict_exptime_object.keys () ) \
    + list ( dict_exptime_flat.keys () )
            
# printing information
print (f'Exposure time information:')
print (f'  object frames:')
for exptime in sorted (dict_exptime_object.keys () ):
    print (f'    {exptime} sec exposure :', \
           f'{dict_exptime_object[exptime]:4d} frames')
    print (f'      Do we have dark frames of {exptime:8.3f} sec exposure?')
    if (exptime in dict_exptime_dark):
        print (f'      Yes, dark frames of {exptime:8.3f} sec exposure', \
               f'are found.')
        print (f'      We have {dict_exptime_dark[exptime]} frames', \
               f'of {exptime} sec dark frames.')
    else:
        print (f'      No, dark frames of {exptime:8.3f} sec exposure', \
               f'are not found.')
        print (f'      ERROR! Check the data.')
print (f'  flatfield frames:')
for exptime in sorted (dict_exptime_flat.keys () ):
    print (f'    {exptime} sec exposure :', \
           f'{dict_exptime_flat[exptime]:4d} frames')
    print (f'      Do we have dark frames of {exptime:8.3f} sec exposure?')
    if (exptime in dict_exptime_dark):
        print (f'      Yes, dark frames of {exptime:8.3f} sec exposure', \
               f'are found.')
        print (f'      We have {dict_exptime_dark[exptime]} frames', \
               f'of {exptime} sec dark frames.')
    else:
        print (f'      No, dark frames of {exptime:8.3f} sec exposure', \
               f'are not found.')
        print (f'      ERROR! Check the data.')
print (f'  Summary of dark frames:')
complete = 1
for exptime in sorted (list_exptime):
    if (exptime in dict_exptime_dark):
        print (f'    {exptime:8.3f} sec dark frames :', \
               f'{dict_exptime_dark[exptime]} frames')
    else:
        print (f'    {exptime:8.3f} sec dark frames :', \
               f'NOT found, check the data!')
        complete = 0
if (complete):
    print (f'Looks OK. All the necessary dark frames exist.')
else:
    print (f'Some dark frames are missing. Check the data!')
