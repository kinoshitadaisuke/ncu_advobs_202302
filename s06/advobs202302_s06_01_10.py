#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 21:18:41 (CST) daisuke>
#

# importing pathlib module
import pathlib

# file name
file_resolv = '/etc/resolv.conf'

# making a pathlib object
path_resolv = pathlib.Path (file_resolv)

# opening file
with path_resolv.open () as fh:
    # reading file
    data = fh.read ()

# printing content of file
print (f'---------- {file_resolv} ----------')
print (data)
print (f'---------- {file_resolv} ----------')
