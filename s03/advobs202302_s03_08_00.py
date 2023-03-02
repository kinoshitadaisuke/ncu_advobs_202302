#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 14:46:33 (CST) daisuke>
#

# importing urllib module
import urllib.request

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# URL of data file
url_data = 'https://cdsarc.cds.unistra.fr/ftp/V/50/catalog.gz'

# output file name
file_output = 'catalog.gz'

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
