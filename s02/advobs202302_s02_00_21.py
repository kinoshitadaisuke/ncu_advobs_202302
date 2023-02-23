#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:28:19 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) using numpy.linspace ()
# meaning of numpy.linspace (1000, 1500, 11):
#   starting from 1000, ending at 1500, and 11 elements
array22 = numpy.linspace (1000, 1500, 11)

# printing Numpy array
print (f'array22:')
print (f'{array22}')

# printing information
print (f'information:')
print (f'  ndim     = {array22.ndim}')
print (f'  size     = {array22.size}')
print (f'  shape    = {array22.shape}')
print (f'  dtype    = {array22.dtype}')
print (f'  itemsize = {array22.itemsize} byte')
