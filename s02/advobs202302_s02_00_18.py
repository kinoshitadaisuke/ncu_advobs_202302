#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:02:57 (CST) daisuke>
#

# importing numpy module
import numpy

# making a 2-dim Numpy array (ndarray) with elements all equal to zeros
array19 = numpy.zeros ( (3, 3) )

# printing Numpy array
print (f'array19:')
print (f'{array19}')

# printing information
print (f'information:')
print (f'  ndim     = {array19.ndim}')
print (f'  size     = {array19.size}')
print (f'  shape    = {array19.shape}')
print (f'  dtype    = {array19.dtype}')
print (f'  itemsize = {array19.itemsize} byte')
