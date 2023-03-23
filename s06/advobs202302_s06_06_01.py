#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 17:25:58 (CST) daisuke>
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

# construction of parser object
desc   = 'Calculating statistical values using sigma clipping with iterations'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='intput FITS files')
parser.add_argument ('-s', type=float, default=5.0, \
                     help='factor for sigma clipping (default: 5.0)')
parser.add_argument ('-n', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files = args.files
nsigma     = args.s
nmaxiter   = args.n

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
    v_max    = -9.99 * 10**10
    # initial value for minimum value
    v_min    = +9.99 * 10**10
    # a variable for a sum of all the pixel values
    total    = 0.0
    # a variable for a square of sum of all the pixel values
    total_sq = 0.0
    # total number of pixels
    n        = data0.size

    # flattening numpy array
    fdata0 = data0.flatten ()
    
    # calculating statistical values
    for z in fdata0:
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
    accepted = fdata0

    # number of iteration
    niter = 0

    # mean and stddev
    mean_clipped   = mean
    stddev_clipped = stddev

    while (niter < nmaxiter):
        # printing status
        print (f'# iteration #{niter + 1:03d}...')

        # initialising parameters
        total_clipped    = 0.0
        total_sq_clipped = 0.0
        v_max_clipped    = -9.99 * 10**10
        v_min_clipped    = +9.99 * 10**10
        
        # number of rejected pixels before sigma-clipping
        n_rejected_prev = len (rejected)

        # temporary list of accepted pixels
        tmp_accepted = []
        
        # calculating statistical values
        for i in range ( len (accepted) ):
            # if the pixel value is outside of
            # [mean-nsigma*stddev,mean+nsigma*stddev], then reject
            if ( (accepted[i] > mean_clipped + nsigma * stddev_clipped) \
                 or (accepted[i] < mean_clipped - nsigma * stddev_clipped) ):
                # appending the pixel value to the list "rejected"
                rejected.append (accepted[i])
            else:
                # appending the pixel value to the list "tmp_accepted"
                tmp_accepted.append (accepted[i])
                # for calculation of a mean
                total_clipped += accepted[i]
                # for calculation of a variance
                total_sq_clipped += accepted[i]**2
                # for maximum value
                if (accepted[i] > v_max_clipped):
                    v_max_clipped = accepted[i]
                # for minimum value
                if (accepted[i] < v_min_clipped):
                    v_min_clipped = accepted[i]

        # new list of accepted pixels
        accepted = tmp_accepted
                    
        # numbers of accepted and rejected pixels
        n_accepted = len (accepted)
        n_rejected = len (rejected)

        # printing status
        print (f'#  n_accepted = {n_accepted}, n_rejected = {n_rejected}')
        
        # mean
        mean_clipped   = total_clipped / n_accepted
        # variance
        var_clipped    = total_sq_clipped / n_accepted - mean_clipped**2
        # standard deviation
        stddev_clipped = var_clipped**0.5

        # checking whether or not leaving from iteration
        if (n_rejected == n_rejected_prev):
            break
        else:
            niter += 1
        
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
