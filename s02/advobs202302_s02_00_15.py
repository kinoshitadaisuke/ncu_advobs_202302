#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:53:45 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array16 = numpy.array ([1.0 + 2.0j, 3.0j, 4.0, 5.0 - 6.0j, -7.0 + 8.0j, \
                        -9.0 - 10.0j, -11.0j, -12.0, 13.0 + 14.0j, 15.0j], \
                       dtype='complex64')

# printing Numpy array
print (f'array16:')
print (f'{array16}')

# printing information
print (f'information:')
print (f'  ndim     = {array16.ndim}')
print (f'  size     = {array16.size}')
print (f'  shape    = {array16.shape}')
print (f'  dtype    = {array16.dtype}')
print (f'  itemsize = {array16.itemsize} byte')
