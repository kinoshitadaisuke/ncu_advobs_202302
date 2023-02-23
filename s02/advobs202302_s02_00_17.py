#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:58:57 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with 10 elements all equal to zeros
array18 = numpy.zeros ( (10,) )

# printing Numpy array
print (f'array18:')
print (f'{array18}')

# printing information
print (f'information:')
print (f'  ndim     = {array18.ndim}')
print (f'  size     = {array18.size}')
print (f'  shape    = {array18.shape}')
print (f'  dtype    = {array18.dtype}')
print (f'  itemsize = {array18.itemsize} byte')
