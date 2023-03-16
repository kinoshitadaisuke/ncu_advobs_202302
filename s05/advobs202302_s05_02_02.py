#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 10:16:37 (CST) daisuke>
#

# file to writing
file_output = 'bright_stars.data'

# data for writing
bright_stars = {
    'Sirius': -1.46,
    'Canopus': -0.74,
    'Rigil Kentaurus': -0.27,
    'Arcturus': -0.05,
    'Vega': 0.03,
    'Capella': 0.08,
    'Rigel': 0.13,
    'Procyon': 0.34,
    'Achernar': 0.46,
    'Betelgeuse': 0.50,
}

# opening file for writing
with open (file_output, 'w') as fh_write:
    # processing for each star
    for name in sorted (bright_stars.keys ()):
        # string to write
        line = f'{name:16s}  {bright_stars[name]:+5.2f} mag\n'
        # writing string into file
        fh_write.write (line)
