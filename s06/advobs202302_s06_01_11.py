#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 21:27:31 (CST) daisuke>
#

# importing pathlib module
import pathlib

# directory name
dir_timezone = '/usr/share/zoneinfo'

# making a pathlib object
path_timezone = pathlib.Path (dir_timezone)

# finding files recursively using .glob () method
list_files = path_timezone.glob ('**/*')

# printing all the files and directories found by .glob ()
for filename in sorted (list_files):
    print (f'{filename}')
