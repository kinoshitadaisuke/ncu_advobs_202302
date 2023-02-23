#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:00:38 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array8 = numpy.array ([0, 2, 4, 8, 16, 32, 64, 128], \
                      dtype=numpy.dtype ('u1') )

# printing Numpy array
print (f'array8:')
print (f'{array8}')

# printing information
print (f'information:')
print (f'  ndim     = {array8.ndim}')
print (f'  size     = {array8.size}')
print (f'  shape    = {array8.shape}')
print (f'  dtype    = {array8.dtype}')
print (f'  itemsize = {array8.itemsize} byte')
