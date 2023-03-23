#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 21:15:30 (CST) daisuke>
#

# importing pathlib module
import pathlib

# file name
file_timezone = '/usr/share/zoneinfo/zone.tab'

# making a pathlib object
path_timezone = pathlib.Path (file_timezone)

# finding file information
info_timezone = path_timezone.stat ()

# printing file information
print (f'file = "{file_timezone}"')
print (f'  st_mode  = {info_timezone.st_mode}')
print (f'  st_ino   = {info_timezone.st_ino}')
print (f'  st_dev   = {info_timezone.st_dev}')
print (f'  st_nlink = {info_timezone.st_nlink}')
print (f'  st_uid   = {info_timezone.st_uid}')
print (f'  st_gid   = {info_timezone.st_gid}')
print (f'  st_size  = {info_timezone.st_size}')
print (f'  st_atime = {info_timezone.st_atime}')
print (f'  st_mtime = {info_timezone.st_mtime}')
print (f'  st_ctime = {info_timezone.st_ctime}')
