#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/23 21:05:07 (CST) daisuke>
#

# importing pathlib module
import pathlib

# file name
file_aaabbbccc = '/aaa/bbb/ccc'

# making a pathlib object
path_aaabbbccc = pathlib.Path (file_aaabbbccc)

# existence check
exist_aaabbbccc = path_aaabbbccc.exists ()

# printing result of existence check
print (f'existence check of "{file_aaabbbccc}" = {exist_aaabbbccc}')
