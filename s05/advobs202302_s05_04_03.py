#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 14:06:12 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy
import astropy.io.fits

# construction of parser object
desc   = 'Generating a simple observing log'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_keyword = 'TIME-OBS,IMAGETYP,OBJECT,EXPTIME,FILTER'
parser.add_argument ('-k', '--keyword', default=default_keyword, \
                     help='a comma-separated list of FITS keywords')
parser.add_argument ('files', nargs='+', help='list of FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keywords   = args.keyword
list_files = args.files

# a list of keywords
list_keyword = keywords.split (',')

# processing files
for file_fits in list_files:
    # if the extension of the file is not '.fits', then skip
    if (file_fits[-5:] != '.fits'):
        continue

    # file name
    pathname = file_fits.split ('/')
    filename = pathname[-1]

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
    
        # header of primary HDU
        header0 = hdu0.header

        # gathering information from FITS header
        record = filename
        for key in list_keyword:
            if key in header0:
                value = str (header0[key])
            else:
                value = "__NONE__"
            record += " %8s" % value

    # printing information
    print (record)
