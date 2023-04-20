#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/20 16:15:24 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned

# importing astropy module
import astropy.coordinates
import astropy.units

# constructing parser object
desc   = "getting coordinate from given target name"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_resolver = ['simbad', 'ned']
choices_format   = ['sexagesimal', 'degree']
parser.add_argument ('-r', '--resolver', choices=choices_resolver, \
                     default='simbad', \
                     help='choice of name resolver (default: simbad)')
parser.add_argument ('-f', '--format', choices=choices_format, \
                     default='sexagesimal', \
                     help='output format (default: sexagesimal)')
parser.add_argument ('target', nargs='+', help='target name(s)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
name_resolver = args.resolver
output_format = args.format
list_target   = args.target

# units
u_ha  = astropy.units.hourangle
u_deg = astropy.units.deg

# printing header
print (f'{"-" * 79}')
if (output_format == 'sexagesimal'):
    print (f'{"Query Word":22s} {"Object Name":22s}', \
           f'{"RA in hh:mm:ss":16s} {"Dec in dd:mm:ss":16s}')
elif (output_format == 'degree'):
    print (f'{"Query Word":22s} {"Object Name":22s}', \
           f'{"RA in deg":>16s} {"Dec in deg":>16s}')
print (f'{"=" * 79}')

# processing for each target
for target_name in list_target:
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

    # making SkyCoord object of Astropy
    if (name_resolver == 'simbad'):
        coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_ha, u_deg))
    elif (name_resolver == 'ned'):
        coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_deg, u_deg))

    # coordinates in (hhmmss, ddmmss) format and (deg, deg) format
    coord_str = coord.to_string (style='hmsdms')
    (coord_ra_str, coord_dec_str) = coord_str.split ()
    coord_ra_deg  = coord.ra.deg
    coord_dec_deg = coord.dec.deg
    
    # printing result
    if (output_format == 'sexagesimal'):
        print (f'{target_name:22s} {name:22s}', \
               f'{coord_ra_str:16s} {coord_dec_str:16s}')
    elif (output_format == 'degree'):
        print (f'{target_name:22s} {name:22s}', \
               f'{coord_ra_deg:12f} deg {coord_dec_deg:12f} deg')

# printing footer
print (f'{"-" * 79}')
