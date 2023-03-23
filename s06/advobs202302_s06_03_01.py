#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 20:48:04 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc   = 'Visualising a FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('file', help='input FITS file')
parser.add_argument ('-o', default='bias.png', \
                     help='output image file (EPS, PDF, PNG, PS)')
parser.add_argument ('-r', type=int, default=300, \
                     help='resolution of output image (default: 300 dpi)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.file
file_output = args.o
resolution  = args.r

# making pathlib objects
path_file_input  = pathlib.Path (file_input)
path_file_output = pathlib.Path (file_output)

# if input file is not a FITS file, then skip
if not (path_file_input.suffix == '.fits'):
    # printing a message
    print (f'ERROR: input file must be a FITS file!')
    # exit
    sys.exit (1)

# if output file is not either PNG, PDF, or PS, then skip
if not ( (path_file_output.suffix == '.eps') \
         or (path_file_output.suffix == '.pdf') \
         or (path_file_output.suffix == '.png') \
         or (path_file_output.suffix == '.ps') ):
    # printing a message
    print (f'ERROR: output file must be either EPS or PDF or PNG or PS!')
    # exit
    sys.exit (1)

# file existence check using pathlib module
if not (path_file_input.exists ()):
    # printing a message
    print (f'ERROR: input file "{file_input}" does not exist!')
    # exit
    sys.exit (1)

# file existence check using pathlib module
if (path_file_output.exists ()):
    # printing a message
    print (f'ERROR: output file "{file_output}" exists!')
    # exit
    sys.exit (1)

# printing input parameters
print (f'input parameters:')
print (f'  input file  = {file_input}')
print (f'  output file = {file_output}')
print (f'  resolution  = {resolution} dpi')
    
# printing status
print (f'now, reading a FITS file "{file_input}"...')
    
# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

# printing status
print (f'finished reading a FITS file "{file_input}"!')

# printing status
print (f'now, making a graphic file "{file_output}"...')
print (f'converting FITS file into image: {file_input} ==> {file_output}')

# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# axes
ax.set_title (file_input)
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
im = ax.imshow (data0, origin='lower', cmap='inferno')
fig.colorbar (im)

# saving file
fig.savefig (file_output, dpi=resolution)

# printing status
print (f'finished making a graphic file "{file_output}"!')
