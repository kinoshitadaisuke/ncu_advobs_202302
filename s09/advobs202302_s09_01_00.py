#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/11 22:26:45 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Generating a simple observing log'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_keyword = 'DATE-OBS,TIME-OBS,IMAGETYP,EXPTIME,FILTER'
parser.add_argument ('-k', '--keywords', default=default_keyword, \
                     help='a list of keywords to check (e.g. TIME-OBS,EXPTIME)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keywords   = args.keywords
list_files = args.files

# a list of keywords
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
    record = f'{filename}  '
    # processing for each keyword
    for key in list_keywords:
        if key in header0:
            if ( (key == 'DATE-OBS') and (len (header0[key]) > 10) ):
                header0[key] = header0[key][:10]
            # if keyword exists, then copy value to the variable "value"
            value = str (header0[key])
        else:
            # if keyword does not exists, then copy "__NONE__"
            # to the varialble "value"
            value = f'__NONE__'
        # appending "value" to the end of "record"
        record += f' {value:10s}'

    # printing information
    print (f'{record}')
