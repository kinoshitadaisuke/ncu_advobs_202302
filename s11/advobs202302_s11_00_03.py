#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/20 16:54:14 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned
import astroquery.skyview

# importing astropy module
import astropy.coordinates
import astropy.units

# importing datetime module
import datetime

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# units
u_ha  = astropy.units.hourangle
u_deg = astropy.units.deg

# constructing parser object
desc   = "downloading an image"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_resolver = ['simbad', 'ned']
choices_survey   = ['DSS1 Blue', 'DSS1 Red', 'DSS2 Blue', \
                    'DSS2 Red', 'DSS2 IR', \
                    'SDSSu', 'SDSSg', 'SDSSr', 'SDSSi', 'SDSSz']
parser.add_argument ('-r', '--resolver', choices=choices_resolver, \
                     default='simbad', \
                     help='choice of name resolver (default: simbad)')
parser.add_argument ('-s', '--survey', choices=choices_survey, \
                     default='DSS2 Red', \
                     help='choice of survey (default: DSS2 Red)')
parser.add_argument ('-f', '--fov', type=int, default=1024, \
                     help='field-of-view in pixel (default: 1024)')
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('target', default='', help='target name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
name_resolver = args.resolver
survey        = args.survey
fov_pix       = args.fov
file_output   = args.output
target_name   = args.target

# checking target name
if (target_name == ''):
    # printing error message
    print (f'ERROR: No target name is given!')
    print (f'ERROR: Give a target name.')
    # exit
    sys.exit ()

# checking output file name
if (file_output == ''):
    # printing error message
    print (f'ERROR: No output file name is given!')
    print (f'ERROR: Use "-o" option to give an output file name.')
    # exit
    sys.exit ()
else:
    # making pathlib object
    path_fits = pathlib.Path (file_output)
    # if output file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print (f'ERROR: Output file must be FITS file!')
        print (f'ERROR: given output file name = "{file_output}"')
        # exit
        sys.exit ()
    # if output file exists, then stop the script
    if (path_fits.exists ()):
        # printing error message
        print (f'ERROR: Output file "{file_output}" exists!')
        # exit
        sys.exit ()
    
# using name resolver
if (name_resolver == 'simbad'):
    query_result = astroquery.simbad.Simbad.query_object (target_name)
elif (name_resolver == 'ned'):
    query_result = astroquery.ipac.ned.Ned.query_object (target_name)

# object name
if (name_resolver == 'simbad'):
    name = query_result['MAIN_ID'][0]
elif (name_resolver == 'ned'):
    name = query_result['Object Name'][0]

# RA and Dec
RA  = query_result['RA'][0]
Dec = query_result['DEC'][0]

# coordinate
if (name_resolver == 'simbad'):
    coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_ha, u_deg))
elif (name_resolver == 'ned'):
    coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_deg, u_deg))

# coordinates in (hhmmss, ddmmss) format and (deg, deg) format
coord_str = coord.to_string (style='hmsdms')
(coord_ra_str, coord_dec_str) = coord_str.split ()
coord_ra_deg  = coord.ra.deg
coord_dec_deg = coord.dec.deg
    
# printing coordinate
print (f'# Target Name: {target_name} = {name}')
print (f'#   RA:  {coord_ra_str} = {coord_ra_deg} deg')
print (f'#   Dec: {coord_dec_str} = {coord_dec_deg} deg')

# printing status
print (f'#')
print (f'# now, querying image list...')
print (f'#')

# searching image
list_image = astroquery.skyview.SkyView.get_image_list (position=coord, \
                                                        survey=survey)

# printing status
print (f'#')
print (f'# finished querying image list!')
print (f'#')

# printing image list
print (f'#')
print (f'# Available images:')
print (f'# {list_image}')
print (f'#')

# printing status
print (f'#')
print (f'# now, downloading image...')
print (f'#')

# getting image
images = astroquery.skyview.SkyView.get_images (position=coord, \
                                                survey=survey, pixels=fov_pix)

# printing status
print (f'#')
print (f'# finished downloading image!')
print (f'#')

# printing status
print (f'#')
print (f'# now, writing a FITS file...')
print (f'#')

# header and data
image0  = images[0][0]
header0 = image0.header
data0   = image0.data

# adding comments in header
header0['history'] = f'image downloaded by command "{command}"'
header0['history'] = f'image saved on {now}'
header0['comment'] = f'query word         = "{target_name}"'
header0['comment'] = f'name resolver used = "{name_resolver}"'
header0['comment'] = f'resolved name      = "{name}"'
header0['comment'] = f'RA                 = "{coord_ra_str}"'
header0['comment'] = f'Dec                = "{coord_dec_str}"'
header0['comment'] = f'data archive used  = "{survey}"'
header0['comment'] = f'output file name   = "{file_output}"'

# saving to a FITS file
astropy.io.fits.writeto (file_output, data0, header=header0)

# printing status
print (f'#')
print (f'# finished writing a FITS file!')
print (f'#')
