#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:31:00 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array11 = numpy.array ([-1.23 * 10**10, -123.45, 6.78 * 10**-5, \
                        0, 1.23 * 10**-10, +12.34, +5.67 * 10**8], \
                       dtype=numpy.dtype ('f4') )

# printing Numpy array
print (f'array11:')
print (f'{array11}')

# printing information
print (f'information:')
print (f'  ndim     = {array11.ndim}')
print (f'  size     = {array11.size}')
print (f'  shape    = {array11.shape}')
print (f'  dtype    = {array11.dtype}')
print (f'  itemsize = {array11.itemsize} byte')
