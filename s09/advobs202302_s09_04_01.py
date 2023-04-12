#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 16:11:08 (CST) daisuke>
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
import numpy.ma

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc   = 'combining flatfield frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_datatype  = ['BIAS', 'DARK', 'FLAT', 'LIGHT']
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
parser.add_argument ('-e', '--exptime', type=float, default=-1.0, \
                     help='exposure time (-1 for any) (default: -1)')
parser.add_argument ('-f', '--filtername', default='__ANY__', \
                     help='filter name')
parser.add_argument ('-d', '--date', default='__ANY__', \
                     help='date in YYYY-MM-DD format (default: __ANY__)')
parser.add_argument ('-t', '--datatype', default='__ANY__', \
                     choices=choices_datatype, \
                     help='data type (default: __ANY__)')
parser.add_argument ('-r', '--rejection', default='sigclip', \
                     choices=choices_rejection, \
                     help='rejection algorithm (default: sigclip)')
parser.add_argument ('-s', '--threshold', type=float, default=4.0, \
                     help='threshold for sigma clipping (default: 4)')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='median', \
                     help='method to estimate centre value (default: median)')
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
date0       = args.date
exptime0    = args.exptime
filtername0 = args.filtername
datatype0   = args.datatype
rejection   = args.rejection
threshold   = args.threshold
maxiters    = args.maxiters
cenfunc     = args.cenfunc
file_output = args.output
list_files  = args.files

# making pathlib object
path_output = pathlib.Path (file_output)

# examination of output file name
if (file_output == ''):
    # print message
    print (f'Output file name must be given.')
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # print message
    print (f'Output file must be a FITS file.')
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print (f'file "{file_output}" exists. exiting...')
    # exit
    sys.exit ()

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

# printing information
print (f'# Data search condition:')
print (f'#   data type = {datatype0}')
print (f'#   exptime   = {exptime0:.3f} sec')
print (f'#   filter    = "{filtername0}"')
print (f'# Input parameters')
print (f'#   rejection algorithm         = {rejection}')
print (f'#   threshold of sigma-clipping = {threshold}')

# printing status
print (f'#')
print (f'# Now scanning data...')

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

    #
    # reading FITS keywords
    #

    # reading FITS header
    header = read_fits_header (file_fits)

    # 'DATE-OBS' keyword
    if ('DATE-OBS' in header):
        date_obs = header['DATE-OBS']
        if (len (date_obs) > 10):
            date_obs = date_obs[:10]
    else:
        date_obs = '__NONE__'
    # 'TIME-OBS' keyword
    if ('TIME-OBS' in header):
        time_obs = header['TIME-OBS']
    else:
        time_obs = '__NONE__'
    # 'IMAGETYP' keyword
    if ('IMAGETYP' in header):
        datatype = header['IMAGETYP']
    else:
        datatype = '__NONE__'
    # 'EXPTIME' keyword
    if ('EXPTIME' in header):
        exptime = header['EXPTIME']
    else:
        exptime = -1.0
    # 'FILTER' keyword
    if ('FILTER' in header):
        filtername = header['FILTER']
    else:
        filtername = '__NONE__'

    # if the data type is not "FLAT", the we skip the file
    if not (datatype == 'FLAT'):
        continue

    # appending FITS header information to the dictionary
    if not (filtername in dict_target):
        dict_target[filtername] = {}
    dict_target[filtername][file_fits] = {}
    dict_target[filtername][file_fits]['exptime']  = exptime
    dict_target[filtername][file_fits]['date-obs'] = date_obs
    dict_target[filtername][file_fits]['time-obs'] = time_obs

# printing status
print (f'#')
print (f'# Finished scanning files')
print (f'#   {len (dict_target[filtername0])} files are found for combining')

# checking number of target files
if ( len (dict_target) < 2 ):
    # printing message
    print (f'number of target files must be greater than 1.')
    # exit
    sys.exit ()

print (f'#')
print (f'# Target files:')
for file_fits in dict_target[filtername0]:
    print (f'#   {file_fits}')

# list for median pixel values
list_median = []

# printing status
print (f'#')
print (f'# Reading image data...')

# counter
i = 0

# reading dark frames
for file_fits in dict_target[filtername0]:
    # reading FITS header
    if (i == 0):
        header = read_fits_header (file_fits)

    # reading FITS data
    data = read_fits_data (file_fits)
    
    # median pixel value of first image
    if (i == 0):
        median_ref = numpy.median (data)

    # median pixel value
    median = numpy.median (data)
    list_median.append (median)

    # scaling
    data_scaled = data / median * median_ref
    
    # constructing a data cube
    if (i == 0):
        data_tmp = data_scaled
    elif (i == 1):
        cube = numpy.concatenate ( ([data_tmp], [data_scaled]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [data_scaled]), axis=0 )

    # printing status
    print (f'#   {i+1:04d} : "{file_fits}" (median: {median:8.2f})')
    
    # incrementing "i"
    i += 1

# printing status
print (f'#')
print (f'# Finished reading image data')

# printing status
print (f'#')
print (f'# Combining image...')

# combining flat frames
if (rejection == 'sigclip'):
    # sigma clipping
    clipped_cube = \
        astropy.stats.sigma_clip (cube, sigma=threshold, \
                                  maxiters=maxiters, cenfunc=cenfunc, \
                                  axis=0, masked=True)
    # combining using average
    combined = numpy.ma.average (clipped_cube, weights=list_median, axis=0)
elif (rejection == 'NONE'):
    # combining using average
    combined = numpy.ma.average (cube, weights=list_median, axis=0)

# printing status
print (f'#')
print (f'# Finished combining image')

# printing status
print (f'#')
print (f'# Writing image into a new FITS file...')
print (f'#   output file = {file_output}')

# mean of combined image
mean_combined = numpy.ma.mean (combined)
    
# adding comments to the header
header['history'] = f'FITS file created by the command "{command}"'
header['history'] = f'Updated on {now}'
header['comment'] = f'multiple FITS files are combined into a single FITS file'
header['comment'] = f'List of combined files:'
for file_fits in dict_target[filtername0]:
    header['comment'] = f'  {file_fits}'
header['comment'] = f'Options given:'
header['comment'] = f'  rejection = {rejection}'
header['comment'] = f'  threshold = {threshold} sigma'
header['comment'] = f'  maxiters  = {maxiters}'
header['comment'] = f'  cenfunc   = {cenfunc}'

# writing a new FITS file
astropy.io.fits.writeto (file_output, \
                         numpy.ma.filled (combined, fill_value=mean_combined), \
                         header=header)

# printing status
print (f'#')
print (f'# Finished writing image into a new FITS file')
print (f'#')
