#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:31:45 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array12 = numpy.array ([-1.23 * 10**10, -123.45, 6.78 * 10**-5, \
                        0, 1.23 * 10**-10, +12.34, +5.67 * 10**8], \
                       dtype=numpy.float32)

# printing Numpy array
print (f'array12:')
print (f'{array12}')

# printing information
print (f'information:')
print (f'  ndim     = {array12.ndim}')
print (f'  size     = {array12.size}')
print (f'  shape    = {array12.shape}')
print (f'  dtype    = {array12.dtype}')
print (f'  itemsize = {array12.itemsize} byte')
