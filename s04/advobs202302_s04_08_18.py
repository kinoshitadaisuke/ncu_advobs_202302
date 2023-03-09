#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 14:12:59 (CST) daisuke>
#

# importing urllib module
import urllib.request

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# URL of data file
url_data = 'https://s3b.astro.ncu.edu.tw/advobs_202302/data/solsys.data'

# output file name
file_output = 'solsys.data'

# printing status
print (f'Now, fetching the file {url_data}...')

# opening URL
with urllib.request.urlopen (url_data) as fh_read:
    # reading data
    data_byte = fh_read.read ()

# printing status
print (f'Finished fetching the file {url_data}!')

# converting raw byte data into string
data_str = data_byte.decode ('utf-8')

# printing status
print (f'Now, writing the data into file {file_output}...')

# opening file for writing
with open (file_output, 'w') as fh_write:
    # writing data
    fh_write.write (data_str)

# printing status
print (f'Finished writing the data into file {file_output}!')
