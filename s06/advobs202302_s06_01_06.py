#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 20:59:51 (CST) daisuke>
#

# importing pathlib module
import pathlib

# file name
file_timezone = '/usr/share/zoneinfo/zone.tab'

# making a pathlib object
path_timezone = pathlib.Path (file_timezone)

# existence check
exist_timezone = path_timezone.exists ()

# printing result of existence check
print (f'existence check of "{file_timezone}" = {exist_timezone}')
