#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/06/01 13:52:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# constructing parser object
desc   = "checking FITS header"
parser = argparse.ArgumentParser (description=desc)

# adding argument
parser.add_argument ('-d', '--dir', default='', help='name of data directory')
parser.add_argument ('-f', '--filter', default='', help='filter name')
parser.add_argument ('-n', '--name', default='', help='name of target object')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
dir_data    = args.dir
target_name = args.name
filter_name = args.filter

# checking "dir_data", "target_name", and "filter_name"
if (dir_data == ''):
    print (f'You have to specify data directory name by using -d option!')
    sys.exit ()
if (target_name == ''):
    print (f'You have to specify target object name by using -n option!')
    sys.exit ()
if (filter_name == ''):
    print (f'You have to specify filter name by using -f option!')
    sys.exit ()

# making a pathlib object for "dir_data"
path_datadir = pathlib.Path (dir_data)

# if not a directory, then stop the script
if not (path_datadir.is_dir () ):
    print ('"{dir_data}" is not a directory!')
    sys.exit ()
# reading directory
list_fits = path_datadir.iterdir ()

# printing header
print (f'# file name, time-obs, data type, exptime, filter, object, airmass')

# processing each FITS file
for path_fits in sorted (list_fits):
    # file name
    file_fits = str (path_fits)

    # if the file is not a FITS file, then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print (f'# file "{path_fits.name}" is not a FITS file, skipping...')
        # skipping to next
        continue
    # if the file is not a reduced data, then skip
    if not (path_fits.stem[-3:] == '_df'):
        # printing message
        print (f'# file "{path_fits.name}" is not a reduced data, skipping...')
        # skipping to next
        continue

    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # reading header information
        header = hdu_list[0].header

    # checking header information
    if not ( (header['IMAGETYP'] == 'LIGHT') \
             and (header['OBJECT'] == target_name) \
             and (header['FILTER'] == filter_name) ):
        continue

    # printing file information
    print (f'{path_fits.name} {header["TIME-OBS"]} {header["IMAGETYP"]}', \
           f'{header["EXPTIME"]:6.1f} {header["FILTER"]}', \
           f'{header["OBJECT"]} {header["AIRMASS"]:5.3f}')
