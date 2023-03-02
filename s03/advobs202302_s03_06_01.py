#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 14:24:27 (CST) daisuke>
#

# input data file
file_input = 'alf_ori.data'

# opening input file
with open (file_input, 'r') as fh_in:
    # reading data line-by-line
    for line in fh_in:
        # splitting data
        (date, mag_str, error_str, band, observer) = line.split ()
        # conversion from string to float
        mag   = float (mag_str)
        error = float (error_str)
        # printing data
        print (f'{date} {mag:f} {error:f} {band} {observer}')
