#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 18:15:10 (CST) daisuke>
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
desc   = 'Reading a FITS file and making a PNG file'
parser = argparse.ArgumentParser (description=desc)

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'twilight', \
                'ocean', 'terrain', 'gnuplot', 'cubehelix', \
                'brg', 'rainbow', 'jet', 'turbo']

# adding arguments
parser.add_argument ('file', help='intput FITS file')
parser.add_argument ('-o', '--output', default='test.png', \
                     help='output image file')
parser.add_argument ('-r', '--resolution', type=int, default=300, \
                     help='resolution of output file (default: 300 dpi)')
parser.add_argument ('-a', '--min', type=float, default=0.0, \
                     help='minimum pixel value')
parser.add_argument ('-b', '--max', type=float, default=65535.0, \
                     help='maximum pixel value')
parser.add_argument ('-c', '--cmap', default='gray', choices=choices_cmap, \
                     help='choice of colour map (default: gray)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.file
file_output = args.output
resolution  = args.resolution
vmin        = args.min
vmax        = args.max
cmap        = args.cmap

# making pathlib objects
path_input  = pathlib.Path (file_input)
path_output = pathlib.Path (file_output)

# if input file is not a FITS file, then skip
if not (path_input.suffix == '.fits'):
    # printing a message
    print (f'ERROR: input file must be a FITS file!')
    # exit
    sys.exit ()

# if output file is not either EPS, PDF, PNG, or PS, then skip
if not ( (path_output.suffix == '.eps') \
         or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') \
         or (path_output.suffix == '.ps') ):
    # printing a message
    print (f'ERROR: output file must be a EPS, PDF, PNG, or PS!')
    # exit
    sys.exit ()

# input file existence check
if not (path_input.exists ()):
    # printing a message
    print (f'ERROR: the file "{file_input}" does not exists!')
    # exit
    sys.exit ()

# output file existence check
if (path_output.exists ()):
    # printing a message
    print (f'ERROR: the file "{file_output}" exists!')
    # exit
    sys.exit ()

# printing input parameters
print (f'#')
print (f'# Input parameters:')
print (f'#   input file  = {file_input}')
print (f'#   output file = {file_output}')
print (f'#   resolution of output image = {resolution} dpi')
print (f'#   minimum value to plot      = {vmin} ADU')
print (f'#   maximum value to plot      = {vmax} ADU')
print (f'#   colour map                 = {cmap}')
print (f'#')

# printing status
print (f'# now, reading a FITS file...')

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

# printing status
print (f'# finished reading a FITS file!')

# printing status
print (f'# now, writing an image file...')

# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# axes
ax.set_title (file_input)
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
im = ax.imshow (data0, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
fig.colorbar (im)

# printing status
print (f'# {file_input} ==> {file_output}')

# saving file
fig.savefig (file_output, dpi=resolution)

# printing status
print (f'# finished writing an image file!')
