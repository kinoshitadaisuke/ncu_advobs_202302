#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/11 16:04:56 (CST) daisuke>
#

# importing urllib module
import urllib.request

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# URL of data file
file_catalogue = 'usno40stds.clean.v3.tar.gz'
url_data       = 'https://www-star.fnal.gov/NorthEqExtension_ugriz/Data/' \
    + file_catalogue

# output file name
file_output = file_catalogue

# printing status
print (f'Now, fetching the file {url_data}...')

# opening URL
with urllib.request.urlopen (url_data) as fh_read:
    # reading data
    data_byte = fh_read.read ()

# printing status
print (f'Finished fetching the file {url_data}!')

# printing status
print (f'Now, writing the data into file {file_output}...')

# opening file for writing
with open (file_output, 'wb') as fh_write:
    # writing data
    fh_write.write (data_byte)

# printing status
print (f'Finished writing the data into file {file_output}!')
