#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 23:54:53 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits
import astropy.stats

# importing datetime module
import datetime

# construction of parser object
desc   = 'Combining dark-subtracted flatfields'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', \
                     help='accepted data type (default: LIGHT)')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=5.0, help='accepted exposure time (default: 5)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted filter name')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', help='outlier rejection algorithm')
parser.add_argument ('-s', '--threshold', type=float, default=5.0, \
                     help='rejection threshold in sigma')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='median', help='method to estimate centre value')
parser.add_argument ('-o', '--output', default='combined.fits', \
                     help='output FITS file')
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
list_input  = args.files
file_output = args.output
rejection   = args.rejection
threshold   = args.threshold
cenfunc     = args.cenfunc
maxiters    = args.maxiters
datatype    = args.datatype
exptime     = args.exptime
filtername  = args.filtername

# command name
command = sys.argv[0]

# checking number of intput FITS files
if ( len (list_input) < 2 ):
    # if the number of input files is less than 2, then stop the script
    print (f'ERROR: Number of input files must be 2 or larger!')
    print (f'ERROR: input files = {list_input}')
    # exit the script
    sys.exit ()

# checking input files
for file_fits in list_input:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)
    # if the file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print (f'ERROR: Input files must be FITS files!')
        print (f'ERROR: The file "{file_fits}" is not a FITS file!')
        # exit the script
        sys.exit ()
    # if the file does not exist, then stop the script
    if not (path_fits.exists ()):
        # printing error message
        print (f'ERROR: Input files does not exist!')
        print (f'ERROR: The file "{file_fits}" does not exist!')
        # exit the script
        sys.exit ()
        
# checking output file
# making pathlib object
path_output = pathlib.Path (file_output)
# if the file is not a FITS file, then stop the script
if not (path_output.suffix == '.fits'):
    # printing error message
    print (f'ERROR: Output file must be FITS files!')
    print (f'ERROR: output file = "{file_output}"')
    # exit the script
    sys.exit ()
# if the file exist, then stop the script
if (path_output.exists ()):
    # printing error message
    print (f'ERROR: Output file exists!')
    print (f'ERROR: output file = "{file_output}"')
    # exit the script
    sys.exit ()

#
# function to open a FITS file and read both header and data
#
def read_fits (file_fits):
    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        # header
        header0 = hdu0.header
        # data
        data0 = hdu0.data
    # returning header and data
    return (header0, data0)

#
# function to open a FITS file and read the header
#
def read_fits_header_only (file_fits):
    # opening a FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
        # header
        header0 = hdu0.header
    # returning header and data
    return (header0)
    
# date/time
now = datetime.datetime.now ().isoformat ()
    
# parameter for counting
i = 0

# printing information
print (f'# Data criteria:')
print (f'#   data type     = {datatype}')
print (f'#   exposure time = {exptime} sec')
print (f'#   filter name   = {filtername}')
print (f'#')

# a list for file names to be combined
file_selected = []

# printing information
print (f'# List of files to be combined:')

# reading FITS files and constructing a data cube
for file_fits in list_input:
    # reading header of a FITS file
    header0 = read_fits_header_only (file_fits)
    
    # if the FITS file is not what you want, then skip
    if ('FILTER' in header0):
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) \
                 and (header0['FILTER'] == filtername) ):
            # closing FITS file
            hdu_list.close ()
            continue
    else:
        if not ( (header0['IMAGETYP'] == datatype) \
                 and (header0['EXPTIME'] == exptime) ):
            # closing FITS file
            hdu_list.close ()
            continue

    # appending file name to the list "file_selected"
    file_selected.append (file_fits)
        
    # copying header only for the first FITS file
    if (i == 0):
        header = header0

    # reading data
    (header0, data0) = read_fits (file_fits)

    # calculation of sigma-clipped mean
    mean, median, stddev \
        = astropy.stats.sigma_clipped_stats (data0, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std')

    # normalisation of pixel data
    normalised0 = data0 / mean
    
    # constructing a data cube
    if (i == 0):
        tmp0 = normalised0
    elif (i == 1):
        cube = numpy.concatenate ( ([tmp0], [normalised0]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [normalised0]), axis=0 )
    
    # incrementing the parameter "i"
    i += 1

    # printing information
    print (f'#   {file_fits} (mean = {mean:8.2f})')

# printing information
print (f'# Output file name: {file_output}')
print (f'# Parameters:')
print (f'#   rejection = {rejection}')
print (f'#   threshold = {threshold}')
print (f'#   maxiters  = {maxiters}')
print (f'#   cenfunc   = {cenfunc}')

# printing status
print (f'# now, combining FITS files...')

# combining images into a single co-added image
if (rejection == 'sigclip'):
    # combining using sigma clipping
    combined, median, stddev \
        = astropy.stats.sigma_clipped_stats (cube, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std', \
                                             axis=0)
elif (rejection == 'none'):
    # combining using simple mean
    combined = numpy.nanmean (cube, axis=0)

# printing status
print (f'# finished combining FITS files!')

# printing status
print (f'# now, writing output FITS file...')
    
# adding comments to the header
header['history'] = f'FITS file created by the command "{command}"'
header['history'] = f'Updated on {now}'
header['comment'] = f'List of combined files:'
for fits in file_selected:
    header['comment'] = f'  {fits}'
header['comment'] = f'Options given:'
header['comment'] = f'  rejection = {rejection}'
header['comment'] = f'  threshold = {threshold} sigma'
header['comment'] = f'  maxiters  = {maxiters}'
header['comment'] = f'  cenfunc   = {cenfunc}'

# writing a new FITS file
astropy.io.fits.writeto (file_output, combined, header=header)

# printing status
print (f'# finished writing output FITS file!')
