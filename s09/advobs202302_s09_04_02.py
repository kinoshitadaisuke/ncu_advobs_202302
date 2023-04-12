#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 16:26:42 (CST) daisuke>
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
desc   = 'normalising FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('file_input', help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_output = args.output
file_input  = args.file_input

# making pathlib objects
path_input  = pathlib.Path (file_input)
path_output = pathlib.Path (file_output)

# checking input file name
if not (path_input.suffix == '.fits'):
    # printing message
    print (f'Input file must be a FITS file.')
    # exit
    sys.exit ()
if not (path_input.exists ()):
    # printing message
    print (f'file "{file_input}" does not exist.')
    # exit
    sys.exit ()

# checking output file name
if (file_output == ''):
    # printing message
    print (f'Output file name has to be given.')
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # printing message
    print (f'Output file must be a FITS file.')
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print (f'file "{file_output}" exists.')
    # exit
    sys.exit ()

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

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

# printing status
print (f'#')
print (f'# normalisation of a FITS file')
print (f'#')
print (f'# input file  = {file_input}')
print (f'# output file = {file_output}')
print (f'#')

# printing status
print (f'# now, reading FITS file "{file_input}"...')

# reading FITS header
header = read_fits_header (file_input)

# reading FITS data
data = read_fits_data (file_input)

# printing status
print (f'# finished reading FITS file "{file_input}"!')

# printing status
print (f'# now, normalising FITS file "{file_input}"...')

# mean of pixel values
mean = numpy.mean (data)

# printing status
print (f'#   mean value of input file = {mean} ADU')

# normalisation
data_normalised = data / mean

# printing status
print (f'# finished normalising FITS file "{file_input}"!')

# printing status
print (f'# now, writing a new FITS file "{file_output}"...')

# adding comments to the header
header['history'] = f'FITS file created by the command "{command}"'
header['history'] = f'Updated on {now}'
header['comment'] = f'normalisation of a FITS file'
header['comment'] = f'Input file: {file_input}'
header['comment'] = f'Mean of pixel values of input file = {mean}'

# writing a new FITS file
astropy.io.fits.writeto (file_output, data_normalised, header=header)

# printing status
print (f'# finished writing a new FITS file "{file_output}"!')
