#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:36:52 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array13 = numpy.array ([-1.23 * 10**10, -123.45, 6.78 * 10**-5, \
                        0, 1.23 * 10**-10, +12.34, +5.67 * 10**8], \
                       dtype='float32')

# printing Numpy array
print (f'array13:')
print (f'{array13}')

# printing information
print (f'information:')
print (f'  ndim     = {array13.ndim}')
print (f'  size     = {array13.size}')
print (f'  shape    = {array13.shape}')
print (f'  dtype    = {array13.dtype}')
print (f'  itemsize = {array13.itemsize} byte')
