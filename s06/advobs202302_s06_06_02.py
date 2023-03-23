#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 17:38:32 (CST) daisuke>
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
    mean   = numpy.mean (data0)
    stddev = numpy.std (data0)
    v_min  = numpy.amin (data0)
    v_max  = numpy.amax (data0)

    # sigma clipped mean
    data0_sigclip  = astropy.stats.sigma_clip (data0, sigma=nsigma, \
                                               maxiters=nmaxiter, masked=False)
    mean_sigclip   = numpy.mean (data0_sigclip)
    stddev_sigclip = numpy.std (data0_sigclip)
    v_min_sigclip  = numpy.amin (data0_sigclip)
    v_max_sigclip  = numpy.amax (data0_sigclip)

    # printing result
    print (f'{file_input}')
    print (f'  clipping criterion: mean +/- {nsigma:5.3f} sigma')
    print (f'  before clipping:')
    print (f'    {"filename":22s} {"mean":>10s} {"stddev":>10s}', \
           f'{"min":>10s} {"max":>10s}')
    print (f'    {filename:22s} {mean:10.3f} {stddev:10.3f}', \
           f'{v_min:10.3f} {v_max:10.3f}')
    print (f'  after clipping:')
    print (f'    {"filename":22s} {"mean":>10s} {"stddev":>10s}', \
           f'{"min":>10s} {"max":>10s}')
    print (f'    {filename:22s} {mean_sigclip:10.3f} {stddev_sigclip:10.3f}', \
           f'{v_min_sigclip:10.3f} {v_max_sigclip:10.3f}')
    print (f'  results of sigma-clipping')
    print (f'    number of accepted pixels =', \
           f'{data0_sigclip.size:10d}')
    print (f'    number of rejected pixels =', \
           f'{data0.size - data0_sigclip.size:10d}')
