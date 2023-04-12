#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/12 15:50:04 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy
import astropy.io.fits
import astropy.stats

# construction pf parser object
desc   = 'combining dark frames'
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

# examination of output file
path_output = pathlib.Path (file_output)
if (file_output == ''):
    # printing message
    print (f'ERROR: Output file name must be given.')
    # exit
    sys.exit ()
if not (path_output.suffix == '.fits'):
    # printing message
    print (f'ERROR: Output file must be a FITS file.')
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print (f'ERROR: Output file already exists.')
    # exit
    sys.exit ()

# command name
command = sys.argv[0]
    
# declaration of list
list_target_files = []

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

# scanning files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    
    # if the file is not a FITS file, then skip
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
        date = header['DATE-OBS']
        if (len (date) > 10):
            date = date[:10]
    else:
        date = '__NONE__'
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

    # using FITS file for combining?
    combine = 0
        
    # check of date
    if ( (date != date0) and (date0 != '__ANY__') ):
        continue
    
    # check of FITS header
    # if criteria match, then we do calculate statistical information
    if ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        if ( ( (datatype == datatype0) or (datatype0 == '__ANY__') ) \
             and ( (exptime == exptime0) or (exptime0 < 0.0) ) \
             and ( (filtername == filtername0) \
                   or (filtername0 == '__ANY__') ) ):
            # we do calculate statistical information
            combine = 1
    elif (datatype == 'DARK'):
        if ( ( (datatype == datatype0) or (datatype0 == '__ANY__') ) \
             and ( (exptime == exptime0) or (exptime0 < 0.0) ) ):
            # we do calculate statistical information
            combine = 1
    elif (datatype == 'BIAS'):
        if ( (datatype == datatype0) or (datatype0 == '__ANY__') ):
            combine = 1
            
    # skip, if combine == 0
    if (combine == 0):
        continue

    # appending file name to the list
    list_target_files.append (file_fits)

# checking number of target files
if ( len (list_target_files) < 2 ):
    # printing message
    print (f'ERROR: number of target files must be greater than 1.')
    # exit
    sys.exit ()

# printing status
print (f'#')
print (f'# Finished scanning files')
print (f'#   {len (list_target_files)} files are found for combining!')
print (f'#')
print (f'# Target files:')
for file_fits in list_target_files:
    print (f'#   {file_fits}')

# printing status
print (f'#')
print (f'# Reading image data...')

# counter
i = 0

# reading dark frames
for file_fits in list_target_files:
    # printing status
    print (f'#   {i+1:04d}: "{file_fits}"')

    # reading header from the first FITS file
    if (i == 0):
        header = read_fits_header (file_fits)
    
    # reading data from FITS file
    data = read_fits_data (file_fits)
    
    # making a mask and masked array
    mdata = numpy.ma.array (data, mask=False)

    # for sigma clipping algorithm
    if (rejection == 'sigclip'):
        # iterations
        for j in range (maxiters):
            # number of usable pixels of previous iterations
            npix_prev = mdata.compressed ().size
            # calculation of median
            median = numpy.ma.median (mdata)
            # calculation of standard deviation
            stddev = numpy.ma.std (mdata)
            # lower threshold
            low  = median - threshold * stddev
            # higher threshold
            high = median + threshold * stddev
            # making a mask
            mask = (mdata < low) | (mdata > high)
            # masked array
            mdata = numpy.ma.array (data, mask=mask)
            # number of rejected pixels
            npix_now = mdata.compressed ().size
            # leaving the loop, if number of usable pixels do not change
            if (npix_now == npix_prev):
                break
        
    # constructing a data cube and its mask
    if (i == 0):
        data_tmp = data
        mask_tmp = mask
    elif (i == 1):
        cube      = numpy.concatenate ( ([data_tmp], [data]), axis=0 )
        cube_mask = numpy.concatenate ( ([mask_tmp], [mask]), axis=0 )
    else:
        cube      = numpy.concatenate ( (cube, [data]), axis=0 )
        cube_mask = numpy.concatenate ( (cube_mask, [mask]), axis=0 )

    # incrementing "i" for counting number of files
    i += 1

# printing status
print (f'#')
print (f'# Finished reading image data')

# printing status
print (f'#')
print (f'# Combining image...')

# constructing a masked data cube
masked_cube = numpy.ma.array (cube, mask=cube_mask)

# combining dark frames
if (rejection == 'sigclip'):
    # sigma clipping using Astropy
    clipped_masked_cube = \
        astropy.stats.sigma_clip (masked_cube, sigma=threshold, \
                                  maxiters=maxiters, cenfunc=cenfunc, \
                                  axis=0, masked=True)
    # combining using average
    combined = numpy.ma.average (clipped_masked_cube, axis=0)
elif (rejection == 'none'):
    # combining using simple average
    combined = numpy.ma.average (masked_cube, axis=0)

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
for file_fits in list_target_files:
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
