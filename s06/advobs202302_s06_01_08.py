#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 21:06:58 (CST) daisuke>
#

# importing pathlib module
import pathlib

# file name
file_timezone = '/usr/share/zoneinfo/zone.tab'

# making a pathlib object
path_timezone = pathlib.Path (file_timezone)

# printing parent, name, suffix, stem
print (f'parent, name, suffix, and stem:')
print (f'  parent of "{path_timezone}" = {path_timezone.parent}')
print (f'  name of "{path_timezone}"   = {path_timezone.name}')
print (f'  suffix of "{path_timezone}" = {path_timezone.suffix}')
print (f'  stem of "{path_timezone}"   = {path_timezone.stem}')
