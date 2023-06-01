#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/06/01 13:09:18 (CST) daisuke>
#

# importing urllib module
import urllib.request

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# URL of data file
file_data = 'pg1047.tar.xz'
url_data  = 'https://s3b.astro.ncu.edu.tw/advobs_202302/data/' + file_data

# output file name
file_output = file_data

# printing status
print (f'Now, fetching file {url_data}...')

# opening URL
with urllib.request.urlopen (url_data) as fh_read:
    # reading data
    data_byte = fh_read.read ()

# printing status
print (f'Finished fetching file {url_data}!')

# printing status
print (f'Now, writing data into file {file_output}...')

# opening file for writing
with open (file_output, 'wb') as fh_write:
    # writing data
    fh_write.write (data_byte)

# printing status
print (f'Finished writing data into file {file_output}!')
