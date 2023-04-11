#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/11 23:37:50 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Checking existence of flatfield frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name (default: FILTER)')
parser.add_argument ('-t', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type (default: IMAGETYP)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword_filter   = args.filter
keyword_datatype = args.datatype
list_files       = args.files

# declaring empty dictionaries for filter names for object frames and flatfield
dict_filters_object = {}
dict_filters_flat   = {}

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

    # if the data type is not "LIGHT" or "FLAT", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        continue

    # filter
    if (keyword_filter in header):
        filter_name = header[keyword_filter]
    else:
        filter_name = "__NONE__"

    # if the filter name is not in the dictionary "dict_filters",
    # then append filter name to the dictionary
    # if the filter name is in the dictionary "dict_filters", then add 1
    if (datatype == 'LIGHT'):
        # object frames
        if not (filter_name in dict_filters_object):
            # appending "filter_name" to the dictionary "dict_filters_object"
            dict_filters_object[filter_name] = 1
        else:
            # add 1
            dict_filters_object[filter_name] += 1
    elif (datatype == 'FLAT'):
        # flatfield frames
        if not (filter_name in dict_filters_flat):
            # appending "filter_name" to the dictionary "dict_filters_flat"
            dict_filters_flat[filter_name] = 1
        else:
            # add 1
            dict_filters_flat[filter_name] += 1

# data-set completeness parameter
complete = 1

# printing filter list
print (f'List of filters used for acquiring object frames:')
for filter_name in sorted (dict_filters_object.keys () ):
    print (f'  {filter_name} ({dict_filters_object[filter_name]} files)')
    print (f'    Do we have flatfield for {filter_name} band filter?')
    # if flatfield exists, then print the number of flatfield frames we have.
    if (filter_name in dict_filters_flat):
        print (f'    Yes, we do have flatfield frames for {filter_name} band.')
        print (f'    Number of {filter_name} band raw flatfield frames =', \
               f'{dict_filters_flat[filter_name]}')
    # if flatfield does not exist, then print an error message.
    else:
        print (f'    No, flatfield frame for {filter_name} band was not found.')
        print (f'    ERROR! The data set is not complete! Check the data!')
        # setting completeness parameter
        complete = 0
# printing a summary
print (f'Do we have all the necessary flatfield frames?')
if (complete):
    print (f'  Yes, looks OK.')
else:
    print (f'  No, some data are missing. Check the data.')
