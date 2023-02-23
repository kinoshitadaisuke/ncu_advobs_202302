#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:47:25 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) using numpy.linspace ()
array_a = numpy.linspace (0, 10, 11)

# printing Numpy array
print (f'array_a:')
print (f'{array_a}')

# printing information
print (f'information:')
print (f'  ndim     = {array_a.ndim}')
print (f'  size     = {array_a.size}')
print (f'  shape    = {array_a.shape}')
print (f'  dtype    = {array_a.dtype}')
print (f'  itemsize = {array_a.itemsize} byte')

# appending one more data to "array_a"
array_a = numpy.append (array_a, [100.0, 200.0, 300.0])

# printing Numpy array
print (f'array_a:')
print (f'{array_a}')

# printing information
print (f'information:')
print (f'  ndim     = {array_a.ndim}')
print (f'  size     = {array_a.size}')
print (f'  shape    = {array_a.shape}')
print (f'  dtype    = {array_a.dtype}')
print (f'  itemsize = {array_a.itemsize} byte')
