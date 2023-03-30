#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 13:45:32 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating a Numpy array
b = numpy.array ([
    [1.2, 3.4, 5.6],
    [7.8, 9.0, 12.3],
    [1.0, 2.0, 3.0],
], dtype='float64')

# printing Numpy array
print (f'b:')
print (f'{b}')

# printing information of Numpy array
print (f'information:')
print (f'  ndim     = {b.ndim}')
print (f'  size     = {b.size}')
print (f'  shape    = {b.shape}')
print (f'  dtype    = {b.dtype}')
print (f'  itemsize = {b.itemsize} byte')
print (f'  nbytes   = {b.nbytes} byte')
