#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 17:50:09 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# importing astropy module
import astropy.io.fits

# construction of parser object
desc   = 'Calculating statistical values of pixel data for selected FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_datatype  = ['LIGHT', 'FLAT', 'DARK', 'BIAS']
choices_filter    = ['gp_Astrodon_2019', 'rp_Astrodon_2019',
                     'ip_Astrodon_2019', 'V_319142', 'R_10349', '__NONE__']
parser.add_argument ('-t', '--datatype', choices=choices_datatype, \
                     default='LIGHT', help='accepted data type')
parser.add_argument ('-e', '--exptime', type=float, \
                     default=0.0, help='accepted exposure time (default: 0.0)')
parser.add_argument ('-f', '--filtername', choices=choices_filter, \
                     default='__NONE__', help='accepted data type')
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-s', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma (default: 4.0)')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
list_files = args.files
rejection  = args.rejection
threshold  = args.threshold
datatype   = args.datatype
exptime    = args.exptime
filtername = args.filtername

# printing header
print (f'{"-" * 80}')
print (f'{"file name":20s} {"n_pix":>8s} {"mean":>9s} {"median":>9s}', \
       f'{"stddev":>9s} {"min":>9s} {"max":>9s}')
print (f'{"=" * 80}')

# processing files
for file_fits in list_files:
    # making a pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the extension of the file is not '.fits', then skip
    if (path_fits.suffix != '.fits'):
        continue

    # existence check of FITS file
    if not (path_fits.exists ()):
        # if FITS file does not exist, then skip
        continue

    # file name
    filename = path_fits.stem

    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]
    
        # header of primary HDU
        header0 = hdu0.header

        # checking image type, exposure time, and filter name
        # if FITS file is not what you want, then skip
        if ('FILTER' in header0):
            if not ( (header0['IMAGETYP'] == datatype) \
                     and (header0['EXPTIME'] == exptime) \
                     and (header0['FILTER'] == filtername) ):
                continue
        else:
            if not ( (header0['IMAGETYP'] == datatype) \
                     and (header0['EXPTIME'] == exptime) ):
                continue

        # flattened image data of primary HDU
        data0 = hdu0.data.flatten ()

    # if rejection algorithm is used, then do rejection check
    if (rejection == 'sigclip'):
        # sigma clipping using scipy module
        clipped, lower, upper \
            = scipy.stats.sigmaclip (data0, low=threshold, high=threshold)
    # if rejection algorithm is not used, then simply copy data to "clipped"
    elif (rejection == 'none'):
        clipped = data0

    # calculation of statistical values
    n_pix  = clipped.size
    mean   = numpy.nanmean (clipped)
    median = numpy.nanmedian (clipped)
    stddev = numpy.nanstd (clipped)
    vmin   = numpy.nanmin (clipped)
    vmax   = numpy.nanmax (clipped)
    
    # printing results
    print (f'{filename:20s} {n_pix:8d} {mean:9.2f} {median:9.2f}', \
           f'{stddev:9.2f} {vmin:9.2f} {vmax:9.2f}')

# printing footer
print (f'{"-" * 80}')
