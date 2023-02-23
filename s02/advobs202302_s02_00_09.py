#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:30:24 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array10 = numpy.array ([-32000, -16000, -8000, -4000, -2000, -1000, \
                       0, +1000, +2000, +4000, +8000, +16000, +32000], \
                      dtype=numpy.int16)

# printing Numpy array
print (f'array10:')
print (f'{array10}')

# printing information
print (f'information:')
print (f'  ndim     = {array10.ndim}')
print (f'  size     = {array10.size}')
print (f'  shape    = {array10.shape}')
print (f'  dtype    = {array10.dtype}')
print (f'  itemsize = {array10.itemsize} byte')
