#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 22:22:38 (CST) daisuke>
#

# name of data file
file_data = 'prime.txt'

# counter
i = 0

# opening file with read mode
with open (file_data, 'r') as fh:
    # reading file line-by-line
    for line in fh:
        # incrementing the counter "i"
        i += 1
        # if i > 20, then stop
        if (i > 20):
            break
        # printing the line
        print (f"{line.rstrip ()}")
        
