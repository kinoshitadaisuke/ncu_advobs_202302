#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 17:01:58 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Searching data'
parser = argparse.ArgumentParser (description=desc)

# choices
choices_datatype = ['LIGHT', 'FLAT', 'DARK', 'BIAS']

# adding arguments
parser.add_argument ('-d', '--date', default='2000-01-01', \
                     help='date in YYYY-MM-DD format (default: 2000-01-01)')
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', \
                     help='data type (default: LIGHT)')
parser.add_argument ('-e', '--exptime', type=float, default=-1.0, \
                     help='exposure time in sec (default: -1.0)')
parser.add_argument ('-f', '--filtername', default='__NONE__', \
                     help='filter name (default: __NONE__)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files        = args.files
search_date       = args.date
search_filtername = args.filtername
search_exptime    = args.exptime
search_datatype   = args.datatype

# a list of keywords
keywords = 'DATE-OBS,TIME-OBS,IMAGETYP,EXPTIME,FILTER'
list_keywords = keywords.split (',')

# printing header
print (f'# FILENAME,{keywords}')

# processing files
for file_fits in list_files:
    # making a pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the extension of the file is not '.fits', then skip
    if (path_fits.suffix != '.fits'):
        continue

    # if the file does not exist, then skip
    if not (path_fits.exists ()):
        continue
    
    # file name
    filename = path_fits.stem

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
    
        # header of primary HDU
        header0 = hdu0.header

    # gathering information from FITS header
    record = "%s  " % filename
    # processing for each keyword
    for key in list_keywords:
        if key in header0:
            # if keyword exists, then copy value to the variable "value"
            value = str (header0[key])
        else:
            # if keyword does not exists, then copy "__NONE__"
            # to the varialble "value"
            value = "__NONE__"
        # appending "value" to the end of "record"
        record += " %10s" % value

    # printing information
    if 'FILTER' in header0:
        if (search_filtername == '__NONE__'):
            if (search_exptime > 0.0):
                if ( (header0['DATE-OBS'] == search_date) \
                     and (header0['IMAGETYP'] == search_datatype) \
                     and (float (header0['EXPTIME']) == search_exptime) ):
                    print (f'{record}')
            else:
                if ( (header0['DATE-OBS'] == search_date) \
                     and (header0['IMAGETYP'] == search_datatype) ):
                    print (f'{record}')
        else:
            if (search_exptime > 0.0):
                if ( (header0['DATE-OBS'] == search_date) \
                     and (header0['IMAGETYP'] == search_datatype) \
                     and (float (header0['EXPTIME']) == search_exptime) \
                     and (header0['FILTER'] == search_filtername) ):
                    print (f'{record}')
            else:
                if ( (header0['DATE-OBS'] == search_date) \
                     and (header0['IMAGETYP'] == search_datatype) \
                     and (header0['FILTER'] == search_filtername) ):
                    print (f'{record}')
    else:
        if (search_exptime > 0.0):
            if ( (header0['DATE-OBS'] == search_date) \
                 and (header0['IMAGETYP'] == search_datatype) \
                 and (float (header0['EXPTIME']) == search_exptime) ):
                print (f'{record}')
        else:
            if ( (header0['DATE-OBS'] == search_date) \
                 and (header0['IMAGETYP'] == search_datatype) ):
                print (f'{record}')
