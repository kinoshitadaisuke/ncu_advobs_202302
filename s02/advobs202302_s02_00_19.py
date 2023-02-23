#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:05:50 (CST) daisuke>
#

# importing numpy module
import numpy

# making a 3-dim Numpy array (ndarray) with elements all equal to zeros
array20 = numpy.zeros ( (3, 4, 5) )

# printing Numpy array
print (f'array20:')
print (f'{array20}')

# printing information
print (f'information:')
print (f'  ndim     = {array20.ndim}')
print (f'  size     = {array20.size}')
print (f'  shape    = {array20.shape}')
print (f'  dtype    = {array20.dtype}')
print (f'  itemsize = {array20.itemsize} byte')
