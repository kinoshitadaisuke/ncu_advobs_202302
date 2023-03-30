#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 23:49:30 (CST) daisuke>
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

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc   = 'Combining images'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='mean', \
                     help='method to estimate centre value (default: mean)')
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

# command name
command = sys.argv[0]

# checking number of intput FITS files
if ( len (list_input) < 2 ):
    # if the number of input files is less than 2, then stop the script
    print (f'ERROR: Number of input files must be 2 or more!')
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
    # existence check
    if not (path_fits.exists ()):
        print (f'ERROR: file "{file_fits}" does not exist!')
        # exit the script
        sys.exit ()
        
# making pathlib object
path_output = pathlib.Path (file_output)
    
# checking output file
# if the file is not a FITS file, then stop the script
if not (path_output.suffix == '.fits'):
    # printing error message
    print (f'ERROR: Output file must be FITS files!')
    # exit the script
    sys.exit ()
# existence check of output file
if (path_output.exists ()):
    # printing error message
    print (f'ERROR: output file "{file_output}" exists!')
    # exit the script
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()

# printing input parameters
print (f'#')
print (f'# Input parameters:')
print (f'#   input FITS files:')
for file_fits in list_input:
    print (f'#     {file_fits}')
print (f'#   output FITS file = {file_fits}')
print (f'#   rejection method = {rejection}')
print (f'#   threshold        = {threshold} sigma')
print (f'#   cenfunc          = {cenfunc}')
print (f'#   maxiters         = {maxiters}')
print (f'#')

# reading FITS files and constructing a data cube
for i in range (len (list_input)):
    # file name
    file_fits = list_input[i]

    # printing status
    print (f'# now, reading FITS file "{file_fits}"...')
        
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]

        # reading header only for the first FITS file
        if (i == 0):
            header0 = hdu0.header

        # reading data
        data0 = hdu0.data

    # constructing a data cube
    if (i == 0):
        tmp0 = data0
    elif (i == 1):
        cube = numpy.concatenate ( ([tmp0], [data0]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [data0]), axis=0 )

    # printing status
    print (f'# finished reading FITS file "{file_fits}"!')

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
print (f'# now, writing FITS file "{file_output}"...')

# adding comments to the header
header0['history'] = "FITS file created by the command \"%s\"" % (command)
header0['history'] = "Updated on %s" % (now)
header0['comment'] = "List of combined files:"
for fits in list_input:
    header0['comment'] = "  %s" % (fits)
header0['comment'] = "Options given:"
header0['comment'] = "  rejection = %s" % (rejection)
header0['comment'] = "  threshold = %f sigma" % (threshold)
header0['comment'] = "  maxiters  = %d" % (maxiters)
header0['comment'] = "  cenfunc   = %s" % (cenfunc)

# writing a new FITS file
astropy.io.fits.writeto (file_output, combined, header=header0)

# printing status
print (f'# finished writing FITS file "{file_output}"!')
