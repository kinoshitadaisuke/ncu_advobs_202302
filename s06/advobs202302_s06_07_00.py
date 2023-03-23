#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 18:31:01 (CST) daisuke>
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
desc   = 'Estimating readout noise from two bias frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs=2, help='file names of 2 bias frames')
parser.add_argument ('-s', type=float, default=5.0, \
                     help='factor for sigma clipping')
parser.add_argument ('-n', type=int, default=10, \
                     help='maximum number of iterations')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_fits = args.files
nsigma     = args.s
nmaxiter   = args.n

# processing FITS files
for file_fits in list_fits:
    # making pathlib object
    path_file_fits = pathlib.Path (file_fits)

    # if input file is not a FITS file, then skip
    if not (path_file_fits.suffix == '.fits'):
        # printing a message
        print (f'ERROR: input file "{file_fits}" is NOT a FITS file!')
        # exit
        sys.exit (1)

    # file existence check using pathlib module
    if not (path_file_fits.exists ()):
        # printing a message
        print (f'ERROR: input file "{file_fits}" does not exist!')
        # exit
        sys.exit (1)

# a function to read a FITS file
def read_fits (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # Primary Header Data Unit
        hdu0 = hdu_list[0]
        # header of primary HDU
        header = hdu0.header
        # data of primary HDU
        data   = hdu0.data

    # returning header and data
    return (header, data)

# reading two FITS file
(header0, data0) = read_fits (list_fits[0])
(header1, data1) = read_fits (list_fits[1])

# conversion of data from uint16 into float64
bias0 = data0.astype (numpy.float64)
bias1 = data1.astype (numpy.float64)

# calculation of (bias0 - bias1)
diff = bias0 - bias1

# sigma-clipping using Astropy
diff_sigclip  = astropy.stats.sigma_clip (diff, sigma=nsigma, \
                                          maxiters=nmaxiter, masked=False)

# sigma clipped statistical values
mean_sigclip     = numpy.mean (diff_sigclip)
stddev_sigclip   = numpy.std  (diff_sigclip)
v_min_sigclip    = numpy.amin (diff_sigclip)
v_max_sigclip    = numpy.amax (diff_sigclip)
skew_sigclip     = scipy.stats.skew (diff_sigclip, axis=None)
kurtosis_sigclip = scipy.stats.kurtosis (diff_sigclip, axis=None)

# calculation of readout noise
readout_noise = stddev_sigclip / (2.0**0.5)

# printing result
print (f'selected bias frames:')
print (f'  file0 = {list_fits[0]}')
print (f'  file1 = {list_fits[1]}')
print (f'statistical values of (file0 - file1):')
print (f'  mean_sigclip     = {mean_sigclip:10.3f}')
print (f'  stddev_sigclip   = {stddev_sigclip:10.3f}')
print (f'  min_sigclip      = {v_min_sigclip:10.3f}')
print (f'  max_sigclip      = {v_max_sigclip:10.3f}')
print (f'  skew_sigclip     = {skew_sigclip:10.3f}')
print (f'  kurtosis_sigclip = {kurtosis_sigclip:10.3f}')
print (f'estimated readout noise:')
print (f'  rough estimate of readout noise = {readout_noise:10.3f} ADU')
