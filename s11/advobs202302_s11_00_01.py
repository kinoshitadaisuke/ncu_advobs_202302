#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/20 16:15:06 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned

# constructing parser object
desc   = "getting coordinate from given target name"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_resolver = ['simbad', 'ned']
parser.add_argument ('-r', '--resolver', choices=choices_resolver, \
                     default='simbad', help='choice of name resolver')
parser.add_argument ('target', nargs='+', help='target name(s)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
name_resolver = args.resolver
list_target   = args.target

# printing header
print (f'{"-" * 79}')
if (name_resolver == 'simbad'):
    print (f'{"Query Word":22s} {"Object Name":22s}', \
           f'{"RA in hh:mm:ss":16s} {"Dec in dd:mm:ss":16s}')
elif (name_resolver == 'ned'):
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

    # printing result
    if (name_resolver == 'simbad'):
        print (f'{target_name:22s} {name:22s} {RA:16s} {Dec:16s}')
    elif (name_resolver == 'ned'):
        print (f'{target_name:22s} {name:22s} {RA:12f} deg {Dec:12f} deg')

# printing footer
print (f'{"-" * 79}')
