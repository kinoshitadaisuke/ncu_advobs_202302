#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 21:05:03 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits
import astropy.visualization

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc   = 'Visualisation of a FITS file'
parser = argparse.ArgumentParser (description=desc)

# choice of colour maps
list_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
             'gray', 'bone', 'cool', 'hot']

# adding arguments
parser.add_argument ('fits', help='input FITS file')
parser.add_argument ('-c', choices=list_cmap, default='gray', \
                     help='colour map (default: gray)')
parser.add_argument ('-o', help='output image file (EPS or PDF or PNG or PS)')
parser.add_argument ('-r', type=int, default=300, \
                     help='output image resolution (default: 300 dpi)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.fits
cmap        = args.c
file_output = args.o
resolution  = args.r

# if input file is not a FITS file, then skip
if not (file_input[-5:] == '.fits'):
    # printing a message
    print (f'ERROR: input file must be a FITS file!')
    # exit
    sys.exit ()

# if output file is not either PNG, PDF, or PS, then skip
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    # printing a message
    print (f'ERROR: output file must be a EPS or PDF or PNG or PS!')
    # exit
    sys.exit ()

# file existence check using pathlib module
path_file_input = pathlib.Path (file_input)
if not (path_file_input.exists ()):
    # printing a message
    print (f'ERROR: input file "{file_input}" does not exist!')
    # exit
    sys.exit ()

# file existence check using pathlib module
path_file_output = pathlib.Path (file_output)
if (path_file_output.exists ()):
    # printing a message
    print (f'ERROR: output file "{file_output}" exists!')
    # exit
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

# making objects "fig", "canvas", "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# axes
ax.set_title (file_input)
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
stretch = astropy.visualization.HistEqStretch (data0)
norm    = astropy.visualization.mpl_normalize.ImageNormalize (stretch=stretch)
im      = ax.imshow (data0, origin='lower', cmap=cmap, norm=norm)
fig.colorbar (im)

# printing status
print (f'Visualising FITS file...')
print (f'  converting image: {file_input} ==> {file_output}')
print (f'  colour map = {cmap}')
print (f'  resolution = {resolution} dpi')

# saving file
fig.savefig (file_output, dpi=resolution)
