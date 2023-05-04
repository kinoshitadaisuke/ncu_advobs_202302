#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/05 00:43:58 (CST) daisuke>
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
import astropy.modeling

# importing photutils module
import photutils.centroids
import photutils.aperture

# constructing parser object
desc   = 'calculating net flux of star'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-f', '--fwhm', type=float, default=4.0, \
                     help='FWHM of stellar PSF in pixel (default: 4.0)')
parser.add_argument ('-a', '--aperture', type=float, default=1.5, \
                     help='aperture radius in FWHM (default: 1.5)')
parser.add_argument ('-s1', '--skyannulus1', type=float, default=3.0, \
                     help='inner sky annulus radius in FWHM (default: 3.0)')
parser.add_argument ('-s2', '--skyannulus2', type=float, default=5.0, \
                     help='outer sky annulus radius in FWHM (default: 5.0)')
parser.add_argument ('-w', '--width', type=int, default=15, \
                     help='half-width of subframe to be plotted (default: 15)')
parser.add_argument ('-x', '--xcentre', type=float, default=-1, \
                     help='x coordinate of target')
parser.add_argument ('-y', '--ycentre', type=float, default=-1, \
                     help='y coordinate of target')
parser.add_argument ('file', default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
fwhm_pixel            = args.fwhm
aperture_radius_fwhm  = args.aperture
skyannulus_inner_fwhm = args.skyannulus1
skyannulus_outer_fwhm = args.skyannulus2
half_width            = args.width
x_centre              = args.xcentre
y_centre              = args.ycentre
file_fits             = args.file

# aperture radius and sky annulus in pixel
aperture_radius_pixel  = aperture_radius_fwhm * fwhm_pixel
skyannulus_inner_pixel = skyannulus_inner_fwhm * fwhm_pixel
skyannulus_outer_pixel = skyannulus_outer_fwhm * fwhm_pixel

# function to read FITS header
def read_fits_header (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # header of primary HDU
        header = hdu_list[0].header
    # returning header
    return (header)

# function to read FITS pixel data
def read_fits_data (file_fits):
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # data of primary HDU
        data = hdu_list[0].data
    # returning pixel data
    return (data)

# making pathlib objects
path_fits   = pathlib.Path (file_fits)

# checking input FITS file name
if (file_fits == ''):
    # printing message
    print (f'You need to specify input file name.')
    # exit
    sys.exit ()
# if input file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing message
    print (f'Input file must be a FITS file.')
    # exit
    sys.exit ()
# if input file does not exist, then stop the script
if not (path_fits.exists ()):
    # printing message
    print (f'Input file does not exist.')
    # exit
    sys.exit ()

# printing status
print (f'# now, reading FITS file "{file_fits}"...')

# reading header of FITS file
header = read_fits_header (file_fits)

# image size
image_size_x = header['NAXIS1']
image_size_y = header['NAXIS2']
    
# checking x_centre and y_centre
if not ( (x_centre > 0) and (x_centre < image_size_x) ):
    print (f'Input x_centre value exceed image size.')
    sys.exit ()
if not ( (y_centre > 0) and (y_centre < image_size_y) ):
    print (f'Input y_centre value exceed image size.')
    sys.exit ()

# reading FITS image data
data = read_fits_data (file_fits)

# printing status
print (f'# finished reading FITS file "{file_fits}"!')

# printing status
print (f'# now, generating an aperture...')
    
# making subframe
x_min = int (x_centre) - half_width
x_max = int (x_centre) + half_width + 1
y_min = int (y_centre) - half_width
y_max = int (y_centre) + half_width + 1
subframe = data[y_min:y_max, x_min:x_max]

# calculating statistical values
subframe_median = numpy.median (subframe)
subframe_stddev = numpy.std (subframe)

# position of the centre on subframe
x_centre_sub = x_centre - x_min
y_centre_sub = y_centre - y_min
position = (x_centre_sub, y_centre_sub)

# making an aperture
apphot_aperture = photutils.aperture.CircularAperture (position, \
                                                       r=aperture_radius_pixel)

# making a sky annulus
apphot_annulus \
    = photutils.aperture.CircularAnnulus (position, \
                                          r_in=skyannulus_inner_pixel, \
                                          r_out=skyannulus_outer_pixel)

# printing aperture
print (f'aperture for star:')
print (apphot_aperture)

# printing sky annulus
print (f'sky annulus:')
print (apphot_annulus)

# printing status
print (f'# finished generating an aperture!')

# printing status
print (f'# now, adding all the signal values within aperture...')

# adding all the signal values within the aperture
apphot_star \
    = photutils.aperture.aperture_photometry (subframe, apphot_aperture, \
                                              error=numpy.sqrt (subframe))

# raw flux = star + sky
raw_flux     = apphot_star[0]['aperture_sum']
raw_flux_err = apphot_star[0]['aperture_sum_err']

# printing result
print (apphot_star)
print (f'aperture sum       = {raw_flux} ADU')
print (f'aperture sum error = {raw_flux_err} ADU')

# printing status
print (f'# finished adding all the signal values within aperture!')

# printing status
print (f'# now, estimating sky background value...')

# sky background estimate
sigma_clip_4 = astropy.stats.SigmaClip (sigma=4.0, maxiters=10)
apphot_sky_stats \
    = photutils.aperture.ApertureStats (subframe, apphot_annulus, \
                                        sigma_clip=sigma_clip_4)
skybg_per_pixel     = apphot_sky_stats.mean
skybg_err_per_pixel = apphot_sky_stats.std

# printing result
print (f'sky background       = {skybg_per_pixel} ADU/pix')
print (f'sky background error = {skybg_err_per_pixel} ADU/pix')

# printing status
print (f'# finished estimating sky background value!')

# printing status
print (f'# now, subtracting sky background...')

#
# net flux = (total flux within aperture)
#             - (skybg per pixel) * (number of pixels in aperture)
#

# sky background subtraction
npix         = apphot_aperture.area
net_flux     = raw_flux - skybg_per_pixel * npix
net_flux_err = numpy.sqrt (raw_flux + npix * skybg_err_per_pixel**2)

# printing status
print (f'# finished subtracting sky background!')

# printing result of aperture photometry
print (f'#')
print (f'# result of aperture photometry')
print (f'#')
print (f'# X, Y, APERTURE_RADIUS, OUTER_SKY_ANNULUS, INNER_SKY_ANNULUS,')
print (f'# NPIX_APERTURE, FLUX, SKY_PER_PIX, SKY_ERR_PER_PIX,')
print (f'# NET_FLUX, NET_FLUX_ERR')
print (f'#')
print (f'{x_centre:.3f} {y_centre:.3f} {aperture_radius_pixel:.3f}', \
       f'{skyannulus_inner_pixel:.3f} {skyannulus_outer_pixel:.3f}', \
       f'{npix:.3f} {raw_flux:.3f}', \
       f'{skybg_per_pixel:.3f} {skybg_err_per_pixel:.3f}', \
       f'{net_flux:.3f} {net_flux_err:.3f}')
