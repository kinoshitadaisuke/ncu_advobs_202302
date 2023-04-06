#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/06 18:41:31 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy.io.fits
import astropy.stats

# importing datetime module
import datetime

# construction of parser object
desc   = 'Combining twilight flatfields'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--date', default='2000-01-01', \
                     help='accepted date in YYYY-MM-DD (default: 2000-01-01)')
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', help='accepted data type')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=-1.0, help='accepted exposure time (default: -1)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted filter name')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', help='outlier rejection algorithm')
parser.add_argument ('-s', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='median', help='method to estimate centre value')
parser.add_argument ('-m', '--max', type=float, \
                     default=30000.0, help='maximum mean value for use')
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
date        = args.date
datatype    = args.datatype
exptime     = args.exptime
filtername  = args.filtername
limit_max   = args.max

# command name
command = sys.argv[0]

# checking number of intput FITS files
if ( len (list_input) < 2 ):
    # if the number of input files is less than 2, then stop the script
    print (f'ERROR: Number of input files must be 2 or larger!')
    print (f'files = {list_input}')
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
        print (f'ERROR: Input file does not exist!')
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
    print (f'ERROR: given output file name = {file_output}')
    # exit the script
    sys.exit ()
# if the file exist, then stop the script
if (path_output.exists ()):
    # printing error message
    print (f'ERROR: Output file exists!')
    print (f'ERROR: The file "{file_output}" exists!')
    # exit the script
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()
    
# printing information
print (f'#')
print (f'# Data criteria:')
print (f'#  date          = {date}')
print (f'#  data type     = {datatype}')
print (f'#  exposure time = {exptime} sec')
print (f'#  filter        = {filtername}')
print (f'#')

# parameter for counting
i = 0

# a list for file names to be combined
file_selected = []

# a Numpy array for weighted average
weight = numpy.array ([], dtype='float64')

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

# reading FITS files and constructing a data cube
for file_fits in list_input:
    # making a pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the extension of the file is not '.fits', then skip
    if (path_fits.suffix != '.fits'):
        # printing message
        print (f'The file "{file_fits}" is not a FITS file!')
        print (f'Skipping...')
        # if the file is not a FITS file, then skip
        continue

    # existence check of FITS file
    if not (path_fits.exists ()):
        # printing message
        print (f'The file "{file_fits}" does not exist!')
        print (f'Skipping...')
        # if FITS file does not exist, then skip
        continue

    # opening FITS file and read the header
    (header0) = read_fits_header_only (file_fits)

    # if the date of data acquisition is different from what we need, then skip
    if (header0['DATE-OBS'] != date):
        continue

    # if the data type is not what we need, then skip
    if (header0['IMAGETYP'] != datatype):
        continue

    # if the exposure time is not what we need, then skip
    if ( (exptime >= 0.0) and (header0['EXPTIME'] != exptime) ):
        continue

    # if the filter is not what we need, then skip
    if ( ('FILTER' in header0) \
         and (header0['FILTER'] != filtername) \
         and (filtername != '__NONE__') ):
        continue
        
    # copying header only for the first FITS file
    if (i == 0):
        header = header0
        
    # opening FITS file and reading header and data
    (header0, data0) = read_fits (file_fits)

    # calculation of sigma-clipped mean
    mean, median, stddev \
        = astropy.stats.sigma_clipped_stats (data0, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std')

    # if mean value is greater than "limit_max", then skip
    if (mean > limit_max):
        continue

    # appending file name to the list "file_selected"
    file_selected.append (file_fits)

    # appending mean value to the array "weight"
    weight = numpy.append (weight, mean)
    
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
    print (f'#   {file_fits} (mean = {mean:8.2f} ADU)')

# printing information
print (f'#')
print (f'# Output file name: "{file_output}"')
print (f'#')
print (f'# Parameters:')
print (f'#  rejection = {rejection}')
print (f'#  threshold = {threshold} sigma')
print (f'#  maxiters  = {maxiters}')
print (f'#  cenfunc   = {cenfunc}')

# printing status
print (f'#')
print (f'# now, combining FITS files...')
print (f'#')

# combining images into a single co-added image
if (rejection == 'sigclip'):
    # sigma clipping
    cube_clipped = astropy.stats.sigma_clip (cube, sigma=threshold, \
                                             maxiters=maxiters, \
                                             cenfunc=cenfunc, stdfunc='std', \
                                             axis=0, masked=True)
    # weighted average
    combined = numpy.ma.average (cube_clipped, weights=weight, axis=0)
elif (rejection == 'none'):
    # weighted average
    combined = numpy.average (cube, weights=weight, axis=0)

# printing status
print (f'#')
print (f'# finished combining FITS files!')
print (f'#')

# printing status
print (f'#')
print (f'# now, writing output FITS file...')
print (f'#')

# adding comments to the header
header['history'] = f'FITS file created by the command "{command}"'
header['history'] = f'Updated on {now}'
header['comment'] = "List of combined files:"
for fits in file_selected:
    header['comment'] = f'  {fits}'
header['comment'] = f'Options given:'
header['comment'] = f'  rejection = {rejection}'
header['comment'] = f'  threshold = {threshold} sigma'
header['comment'] = f'  maxiters  = {maxiters}'
header['comment'] = f'  cenfunc   = {cenfunc}'

# writing a new FITS file
astropy.io.fits.writeto (file_output, \
                         numpy.ma.filled (combined, fill_value=numpy.nan), \
                         header=header)

# printing status
print (f'#')
print (f'# finished writing output FITS file!')
print (f'#')
