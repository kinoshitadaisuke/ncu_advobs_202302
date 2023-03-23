#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 17:54:04 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc   = 'Calculating statistical values using sigma clipping by Astropy'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS file')
parser.add_argument ('-s', type=float, default=5.0, \
                     help='factor for sigma clipping')
parser.add_argument ('-n', type=int, default=10, \
                     help='maximum number of iterations')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.s
nmaxiter   = args.n

# processing file one-by-one
for file_input in list_files:
    # making pathlib object
    path_file_input = pathlib.Path (file_input)

    # if input file is not a FITS file, then skip
    if not (path_file_input.suffix == '.fits'):
        # printing a message
        print (f'ERROR: input file "{file_input}" is NOT a FITS file!')
        # exit
        sys.exit (1)

    # file existence check using pathlib module
    if not (path_file_input.exists ()):
        # printing a message
        print (f'ERROR: input file "{file_input}" does not exist!')
        # exit
        sys.exit (1)

    # file name
    filename = path_file_input.name

    # opening FITS file
    with astropy.io.fits.open (file_input) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]

        # reading header
        header0 = hdu0.header

        # reading data
        data0 = hdu0.data

    # simple mean
    mean     = numpy.mean (data0)
    stddev   = numpy.std (data0)
    v_min    = numpy.amin (data0)
    v_max    = numpy.amax (data0)
    skew     = scipy.stats.skew (data0, axis=None)
    kurtosis = scipy.stats.kurtosis (data0, axis=None)

    # sigma clipped mean
    data0_sigclip  = astropy.stats.sigma_clip (data0, sigma=nsigma, \
                                               maxiters=nmaxiter, masked=False)
    mean_sigclip     = numpy.mean (data0_sigclip)
    stddev_sigclip   = numpy.std (data0_sigclip)
    v_min_sigclip    = numpy.amin (data0_sigclip)
    v_max_sigclip    = numpy.amax (data0_sigclip)
    skew_sigclip     = scipy.stats.skew (data0_sigclip, axis=None)
    kurtosis_sigclip = scipy.stats.kurtosis (data0_sigclip, axis=None)

    # printing result
    print (f'{file_input}')
    print (f'  clipping criterion: mean +/- {nsigma:5.3f} sigma')
    print (f'  before clipping:')
    print (f'    {"mean":>11s} {"stddev":>11s}', \
           f'{"min":>11s} {"max":>11s}', \
           f'{"skewness":>11s} {"kurtosis":>11s}')
    print (f'    {mean:11.3f} {stddev:11.3f}', \
           f'{v_min:11.3f} {v_max:11.3f}', \
           f'{skew:11.3f} {kurtosis:11.3f}')
    print (f'  after clipping:')
    print (f'    {"mean":>11s} {"stddev":>11s}', \
           f'{"min":>11s} {"max":>11s}', \
           f'{"skewness":>11s} {"kurtosis":>11s}')
    print (f'    {mean_sigclip:11.3f} {stddev_sigclip:11.3f}', \
           f'{v_min_sigclip:11.3f} {v_max_sigclip:11.3f}', \
           f'{skew_sigclip:11.3f} {kurtosis_sigclip:11.3f}')
    print (f'  results of sigma-clipping')
    print (f'    number of accepted pixels =', \
           f'{data0_sigclip.size:10d}')
    print (f'    number of rejected pixels =', \
           f'{data0.size - data0_sigclip.size:10d}')
