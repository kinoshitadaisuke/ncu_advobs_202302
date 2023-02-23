#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:30:34 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) using numpy.logspace ()
array23 = numpy.logspace (0, 10, 11)

# printing Numpy array
print (f'array23:\n{array23}')

# printing information
print (f'information:')
print (f'  ndim     = {array23.ndim}')
print (f'  size     = {array23.size}')
print (f'  shape    = {array23.shape}')
print (f'  dtype    = {array23.dtype}')
print (f'  itemsize = {array23.itemsize} byte')
