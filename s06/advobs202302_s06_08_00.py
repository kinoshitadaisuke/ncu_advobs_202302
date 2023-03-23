#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 18:57:06 (CST) daisuke>
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

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc = 'Examining time variation of mean bias level'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='bias frames')
parser.add_argument ('-s', type=float, default=5.0, \
                     help='factor for sigma clipping (default: 5.0)')
parser.add_argument ('-n', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('-o', default='bias.png', \
                     help='output file name (default: bias.png)')
parser.add_argument ('-r', type=int, default=300, \
                     help='resolution of output image (default: 300)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files  = args.files
nsigma      = args.s
nmaxiter    = args.n
file_output = args.o
resolution  = args.r

# making empty Numpy arrays for storing data
data_datetime = numpy.array ([], dtype='datetime64[ms]')
data_mean     = numpy.array ([], dtype='float64')
data_stddev   = numpy.array ([], dtype='float64')

# if input file is not a FITS file, then stop
for file_fits in list_files:
    # making pathlib object
    path_file_fits = pathlib.Path (file_fits)
    # checking suffix of file name
    if not (path_file_fits.suffix == '.fits'):
        # printing a message
        print (f'ERROR: input file "{file_input}" is NOT a FITS file!')
        # exit
        sys.exit (1)

# making pathlib object
path_file_output = pathlib.Path (file_output)

# if output file is not either EPS, PDF, PNG, or PS, then stop
if not ( (path_file_output.suffix == '.eps') \
         or (path_file_output.suffix == '.pdf') \
         or (path_file_output.suffix == '.png') \
         or (path_file_output.suffix == '.ps') ):
    # printing a message
    print (f'ERROR: output file "{file_output}" is NOT either EPS,PNG,PDF,PS!')
    # exit
    sys.exit (1)

# if output file exists, then stop
if (path_file_output.exists ()):
    # printing a message
    print (f'ERROR: otuput file "{file_output}" exists!')
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

# processing files
for file_fits in list_files:
    # printing a message
    print (f'Now processing the file "{file_fits}"...')

    # file existence check using pathlib module
    path_file_fits = pathlib.Path (file_fits)
    if not (path_file_fits.exists ()):
        # printing a message
        print (f'WARNING: input file "{file_fits}" does not exist!')
        # skipping to next
        continue

    # printing a message
    print (f'  now reading pixels...')

    # reading a FITS file
    (header0, data0) = read_fits (file_fits)

    # conversion from uint16 into float64
    data_float = data0.astype (numpy.float64)

    # printing a message
    print (f'  finished reading pixels!')

    # date/time
    if ('DATE-OBS' in header0):
        date = header0['DATE-OBS']
    else:
        continue
    if ('TIME-OBS' in header0):
        time = header0['TIME-OBS']
    else:
        continue
    datetime_str = f'{date}T{time}'
    datetime64   = numpy.datetime64 (datetime_str)

    # printing a message
    print (f'  now calculating sigma-clipped mean and stddev...')

    # sigma clipped mean and stddev
    data_sigclip  = astropy.stats.sigma_clip (data_float, sigma=nsigma, \
                                               maxiters=nmaxiter, masked=False)
    mean_sigclip   = numpy.mean (data_sigclip)
    stddev_sigclip = numpy.std  (data_sigclip)

    # appending data to the lists
    data_datetime = numpy.append (data_datetime, datetime64)
    data_mean     = numpy.append (data_mean, mean_sigclip)
    data_stddev   = numpy.append (data_stddev, stddev_sigclip)

    # printing a message
    print (f'  finished calculating sigma-clipped mean and stddev...')

    # printing a message
    print (f'Finished processing the file "{file_fits}"!')

# printing a message
print (f'Now generating a plot "{file_output}"...')
    
# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# labels
ax.set_xlabel ('Date/Time [UT]')
ax.set_ylabel ('Mean Bias Level [ADU]')
ax.xaxis.set_major_formatter (matplotlib.dates.DateFormatter ('%H:%M'))

# plotting data
ax.errorbar (data_datetime, data_mean, yerr=data_stddev, \
             marker='o', color='blue', markersize=3, linestyle='none', \
             ecolor='black', capsize=2, \
             label='Mean bias level')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=resolution)

# printing a message
print (f'Finished generating a plot "{file_output}"!')
