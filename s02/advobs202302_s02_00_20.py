#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:23:00 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) using numpy.arange ()
# meaning of numpy.arange (0, 20, 2):
#   starting from 0 until just before 20 with step of 2
array21 = numpy.arange (0, 20, 2)

# printing Numpy array
print (f'array21:')
print (f'{array21}')

# printing information
print (f'information:')
print (f'  ndim     = {array21.ndim}')
print (f'  size     = {array21.size}')
print (f'  shape    = {array21.shape}')
print (f'  dtype    = {array21.dtype}')
print (f'  itemsize = {array21.itemsize} byte')
