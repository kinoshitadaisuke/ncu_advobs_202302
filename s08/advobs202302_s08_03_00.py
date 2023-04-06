#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/06 12:51:52 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Calculating statistical values for selected FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019', \
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-d', '--date', default='2000-01-01', \
                     help='accepted date in YYYY-MM-DD (default: 2000-01-01)')
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', \
                     help='accepted data type (default: LIGHT)')
parser.add_argument ('-e', '--exptime', type=float, default=-1.0, \
                     help='accepted exposure time (negative for any exptime)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted filter name')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', help='outlier rejection algorithm')
parser.add_argument ('-s', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files  = args.files
rejection   = args.rejection
threshold   = args.threshold
date        = args.date
datatype    = args.datatype
exptime     = args.exptime
filtername  = args.filtername

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

# printing header
print (f'{"-" * 80}')
print (f'{"file name":20s} {"n_pix":>8s} {"mean":>9s} {"median":>9s}', \
       f'{"stddev":>9s} {"min":>9s} {"max":>9s}')
print (f'{"=" * 80}')

# processing files
for file_fits in list_files:
    # making pathlib module
    path_fits = pathlib.Path (file_fits)
    
    # if the extension of the file is not '.fits', then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print (f'# skipping "{file_fits}"...')
        # skipping
        continue

    # if the file does not exist, then skip
    if not (path_fits.exists ()):
        # printing message
        print (f'# "{file_fits}" does not exist...')
        # skipping
        continue

    # file name
    filename = path_fits.stem

    # reading header from a FITS file
    header0 = read_fits_header_only (file_fits)

    # if the date of data acquisition is different from what we need, then skip
    if not (header0['DATE-OBS'] == date):
        continue

    # if the data type is not what we need, then skip
    if (header0['IMAGETYP'] != datatype):
        continue

    # if the exposure time is not what we need, then skip
    if ( (exptime >= 0.0) and (header0['EXPTIME'] != exptime) ):
        continue

    # if the filter is not what we need, then skip
    if ( ('FILTER' in header0) and (header0['FILTER'] != filtername) \
         and (filtername != '__NONE__') ):
        continue
    
    # reading header and data from a FITS file
    (header0, data0) = read_fits (file_fits)
    
    # flattened image data of primary HDU
    data0_1d = data0.flatten ()

    # if rejection algorithm is used, then do rejection check
    if (rejection == 'sigclip'):
        # sigma clipping using scipy module
        clipped, lower, upper \
            = scipy.stats.sigmaclip (data0_1d, low=threshold, high=threshold)
    elif (rejection == 'none'):
        clipped = data0_1d

    # calculation of statistical values
    n_pix  = len (clipped)
    mean   = numpy.nanmean (clipped)
    median = numpy.nanmedian (clipped)
    stddev = numpy.nanstd (clipped)
    vmin   = numpy.nanmin (clipped)
    vmax   = numpy.nanmax (clipped)
    
    # printing results
    print (f'{filename:20s} {n_pix:8d} {mean:9.2f} {median:9.2f}', \
           f'{stddev:9.2f} {vmin:9.2f} {vmax:9.2f}')

# printing footer
print (f'{"-" * 80}')
