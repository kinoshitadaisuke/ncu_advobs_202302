#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/04/05 16:30:05 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing re module
import re

# importing pathlib module
import pathlib

# importing ssl module
import ssl

# importing urllib module
import urllib.request

# setting for SSL
ssl._create_default_https_context = ssl._create_unverified_context

# construction of parser object
desc = 'WWW fetch'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('URL', default='', help='URL of the online resource')
parser.add_argument ('-o', '--output', default='', help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# parameters
target_url  = args.URL
file_output = args.output

#
# check of URL
#
# making a pattern for matching by regular expression
pattern_http = re.compile ('^http')
# matching by regular expression
match_http   = re.search (pattern_http, target_url)
# if not matching, then stop the script
if not (match_http):
    # printing message
    print (f'URL has to start with "http"!')
    print (f'Check the URL!')
    print (f'Stopping the script...')
    # exiting the script
    sys.exit ()

# output file name
if (file_output == ''):
    # default output file name
    #   for URL of https://aaa.bbb.ccc/ddd/eee/fff.ggg
    #   output file name ==> fff.ggg
    file_output = target_url.split ('/') [-1]

# existence check of output file
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing message
    print (f'The output file "{file_output}" exists!')
    print (f'Stopping the script...')
    # exiting the script
    sys.exit ()

# printing input parameters
print (f'#')
print (f'# input parameters')
print (f'#  target URL  = {target_url}')
print (f'#  output file = {file_output}')
print (f'#')
    
# making a request object
req = urllib.request.Request (url=target_url)

# printing status
print (f'# now fetching the object...')

# retrieval of target
with urllib.request.urlopen (req) as www:
    # target file size
    file_size_byte = int (www.length)
    # printing file size of target
    print (f'#  file size = {file_size_byte:10d} byte')
    print (f'#            = {file_size_byte / 1024:10.0f} kB')
    print (f'#            = {file_size_byte / 1024 / 1024:10.0f} MB')
    # retrieving data
    target_data = www.read ()

# printing status
print (f'# finished fetching the object!')

# printing status
print (f'# now writing data into file...')

# opening output file for binary writing mode
with open (file_output, 'wb') as fh:
    # writing data into output file
    fh.write (target_data)

# printing status
print (f'# finished writing data into file!')
