#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 12:54:03 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating a Numpy array
a = numpy.array ([1.2, 3.4, 5.6, 7.8, 9.0, 12.3], dtype='float64')

# printing Numpy array
print (f'a = {a}')

# printing information of Numpy array
print (f'information:')
print (f'  ndim     = {a.ndim}')
print (f'  size     = {a.size}')
print (f'  shape    = {a.shape}')
print (f'  dtype    = {a.dtype}')
print (f'  itemsize = {a.itemsize} byte')
