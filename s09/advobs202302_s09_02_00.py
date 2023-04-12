#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/13 00:53:43 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy
import numpy.ma

# importing scipy module
import scipy.stats

# importing astropy module
import astropy
import astropy.io.fits

# construction pf parser object
desc   = 'calculating statistical information of selected FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_datatype  = ['BIAS', 'DARK', 'FLAT', 'LIGHT']
choices_rejection = ['none', 'sigclip']
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
list_files  = args.files

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

# printing header
print (f'#')
print (f'# {"file name":<20s} {"npix":>7s} {"mean":>8s} {"median":>8s}', \
       f'{"stddev":>7s} {"min":>7s} {"max":>7s} {"skew":>7s}')
print (f'#')

# scanning files
for file_fits in list_files:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)

    # file name
    filename = path_fits.stem

    # if the file is not a FITS file, then skip
    if not (path_fits.suffix == '.fits'):
        # printing message
        print (f'### file "{file_fits}" is not a FITS file! skipping...')
        # skipping
        continue

    # reading FITS header
    header = read_fits_header (file_fits)

    #
    # reading FITS keywords
    #

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
    
    # calculate statistical information?
    calc = 0

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
            calc = 1
    elif (datatype == 'DARK'):
        if ( ( (datatype == datatype0) or (datatype0 == '__ANY__') ) \
             and ( (exptime == exptime0) or (exptime0 < 0.0) ) ):
            # we do calculate statistical information
            calc = 1
    elif (datatype == 'BIAS'):
        if ( (datatype == datatype0) or (datatype0 == '__ANY__') ):
            calc = 1
            
    # skip, if calc == 0
    if (calc == 0):
        continue

    #
    # calculations of statistical values
    #

    # reading data from FITS file
    data = read_fits_data (file_fits)

    # making a masked array
    mdata = numpy.ma.array (data, mask=False)
    
    # sigma clipping algorithm
    if (rejection == 'sigclip'):
        # iterations
        for i in range (maxiters):
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
            # making a masked array
            mdata = numpy.ma.array (mdata, mask=mask)
            # number of usable pixels
            npix_now = mdata.compressed ().size
            # leaving the loop, if number of usable pixels do not change
            if (npix_now == npix_prev):
                break
        
    # calculation of mean, median, stddev, min, max, and skewness
    mean   = numpy.ma.mean (mdata)
    median = numpy.ma.median (mdata)
    stddev = numpy.ma.std (mdata)
    vmin   = numpy.ma.min (mdata)
    vmax   = numpy.ma.max (mdata)
    skew   = scipy.stats.skew (mdata, axis=None)

    # number of pixels
    npix = mdata.compressed ().size

    # printing result
    print (f'{filename:<22s} {npix:7d} {mean:8.2f} {median:8.2f}', \
           f'{stddev:7.2f} {vmin:7.1f} {vmax:7.1f} {skew:7.3f}')
