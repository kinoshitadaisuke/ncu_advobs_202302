#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 09:57:45 (CST) daisuke>
#

# file to reading
file_input = 'comets.data'

# opening file for reading
with open (file_input, 'r') as fh_read:
    # reading file line-by-line
    for line in fh_read:
        # unless data for comet 1P/Halley is found, skip the line
        if not ('Halley' in line):
            continue
        # print the line
        print (f'{line}')
