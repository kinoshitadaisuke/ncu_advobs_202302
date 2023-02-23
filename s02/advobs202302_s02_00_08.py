#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:04:28 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array9 = numpy.array ([-30000, -20000, -10000, 0, +10000, +20000, +30000], \
                      dtype=numpy.dtype ('i2') )

# printing Numpy array
print (f'array9:\n{array9}')

# printing information
print (f'information:')
print (f'  ndim     = {array9.ndim}')
print (f'  size     = {array9.size}')
print (f'  shape    = {array9.shape}')
print (f'  dtype    = {array9.dtype}')
print (f'  itemsize = {array9.itemsize} byte')
