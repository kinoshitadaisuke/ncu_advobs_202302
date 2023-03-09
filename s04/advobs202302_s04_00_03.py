#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 10:03:18 (CST) daisuke>
#

# importing scipy module
import scipy.constants

# searching constants
search_result = scipy.constants.find ('light')

# printing search result
for constant in search_result:
    print (f'{constant}')
