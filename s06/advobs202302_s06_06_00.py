#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 17:07:08 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Calculating statistical values using sigma clipping'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='input FITS files')
parser.add_argument ('-s', type=float, default=5.0, \
                     help='factor for sigma clipping (default: 5.0)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.s

# processing files one-by-one
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

    # initial value for maximum value
    v_max         = -9.99 * 10**10
    v_max_clipped = -9.99 * 10**10
    # initial value for minimum value
    v_min         = +9.99 * 10**10
    v_min_clipped = +9.99 * 10**10
    # a variable for a sum of all the pixel values
    total         = 0.0
    total_clipped = 0.0
    # a variable for a square of sum of all the pixel values
    total_sq         = 0.0
    total_sq_clipped = 0.0
    # total number of pixels
    n = data0.size

    # calculating statistical values
    for row in data0:
        for z in row:
            # for calculation of a mean
            total += z
            # for calculation of a variance
            total_sq += z**2
            # for maximum value
            if (z > v_max):
                v_max = z
            # for minimum value
            if (z < v_min):
                v_min = z

    # mean
    mean   = total / n
    # variance
    var    = total_sq / n - mean**2
    # standard deviation
    stddev = var**0.5

    # lists for rejected and accepted values
    rejected = []
    accepted = []

    # calculating statistical values
    for row in data0:
        for z in row:
            # if the pixel value is outside of
            # [mean-nsigma*stddev,mean+nsigma*stddev], then reject
            if ( (z > mean + nsigma * stddev) or (z < mean - nsigma * stddev) ):
                # appending the pixel value to the list "rejected"
                rejected.append (z)
            else:
                # appending the pixel value to the list "accepted"
                accepted.append (z)
                # for calculation of a mean
                total_clipped += z
                # for calculation of a variance
                total_sq_clipped += z**2
                # for maximum value
                if (z > v_max_clipped):
                    v_max_clipped = z
                # for minimum value
                if (z < v_min_clipped):
                    v_min_clipped = z

    # numbers of accepted and rejected pixels
    n_accepted = len (accepted)
    n_rejected = len (rejected)

    # mean
    mean_clipped   = total_clipped / n_accepted
    # variance
    var_clipped    = total_sq_clipped / n_accepted - mean_clipped**2
    # standard deviation
    stddev_clipped = var_clipped**0.5

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
    print (f'    {filename:22s} {mean_clipped:10.3f} {stddev_clipped:10.3f}', \
           f'{v_min_clipped:10.3f} {v_max_clipped:10.3f}')
    print (f'  results of sigma-clipping')
    print (f'    number of accepted pixels = {n_accepted:10d}')
    print (f'    number of rejected pixels = {n_rejected:10d}')
    print (f'    rejected pixel values     = {sorted (rejected)}')
