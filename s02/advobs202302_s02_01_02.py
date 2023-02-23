#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 13:59:29 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy array "array_a" using numpy.linspace ()
array_a = numpy.linspace (0, 9, 10)

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

# making Numpy array "array_b" using numpy.linspace ()
array_b = numpy.linspace (10, 14, 5)

# printing Numpy array
print (f'array_b:')
print (f'{array_b}')

# printing information
print (f'information:')
print (f'  ndim     = {array_b.ndim}')
print (f'  size     = {array_b.size}')
print (f'  shape    = {array_b.shape}')
print (f'  dtype    = {array_b.dtype}')
print (f'  itemsize = {array_b.itemsize} byte')

# concatenating array_a and array_b and making Numpy array "array_c"
array_c = numpy.concatenate ([array_a, array_b])

# printing Numpy array
print (f'array_c:')
print (f'{array_c}')

# printing information
print (f'information:')
print (f'  ndim     = {array_c.ndim}')
print (f'  size     = {array_c.size}')
print (f'  shape    = {array_c.shape}')
print (f'  dtype    = {array_c.dtype}')
print (f'  itemsize = {array_c.itemsize} byte')
