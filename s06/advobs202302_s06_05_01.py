#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 16:34:27 (CST) daisuke>
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

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc   = 'Reading a FITS file and constructing a histogram'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='input FITS file')
parser.add_argument ('-o', help='output image file (EPS, PDF, PNG, PS)')
parser.add_argument ('-a', type=float, default=0.0, \
                     help='minimum value for histogram (default: 0.0)')
parser.add_argument ('-b', type=float, default=10000.0, \
                     help='maximum value for histogram (default: 10000.0)')
parser.add_argument ('-w', type=float, default=1.0, \
                     help='width of a bin for histogram (default: 1.0)')
parser.add_argument ('-r', type=float, default=300.0, \
                     help='resolution of output image file (default: 300 dpi)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file and output image file
file_input  = args.file
file_output = args.o

# parameters
a          = args.a
b          = args.b
width      = args.w
nbin       = int ( (b - a) / width ) + 1
resolution = args.r

# making pathlib objects
path_file_input  = pathlib.Path (file_input)
path_file_output = pathlib.Path (file_output)

# if input file is not a FITS file, then skip
if not (path_file_input.suffix == '.fits'):
    # printing a message
    print (f'ERROR: input file "{file_input}" is NOT a FITS file!')
    # exit
    sys.exit (1)

# if output file is not either PNG, PDF, or PS, then skip
if not ( (path_file_output.suffix == '.eps') \
         or (path_file_output.suffix == '.pdf') \
         or (path_file_output.suffix == '.png') \
         or (path_file_output.suffix == '.ps') ):
    # printing a message
    print (f'ERROR: output file "{file_output}" is NOT either EPS,PNG,PDF,PS!')
    # exit
    sys.exit (1)

# existence check of input file using pathlib module
if not (path_file_input.exists ()):
    # printing a message
    print (f'ERROR: input file "{file_input}" does not exist!')
    # exit
    sys.exit (1)

# existence check of output file using pathlib module
if (path_file_output.exists ()):
    # printing a message
    print (f'ERROR: output file "{file_output}" exists!')
    # exit
    sys.exit (1)
    
# if a >= b, then skip
if (a >= b):
    # printing a message
    print (f'maximum value "a" must be greater than minimum value "b".')
    # exit
    sys.exit (1)
    
# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

# initialisation of Numpy arrays for histogram
bins = numpy.linspace (a, b, nbin)

# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# labels
ax.set_xlabel ('Pixel Value [ADU]')
ax.set_ylabel ('Number of Pixels')

# plotting histogram
ax.hist (data0.flatten (), bins=bins, histtype='bar', \
         edgecolor='black', linewidth=0.3, align='mid', \
         label='Pixel values')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=resolution)
