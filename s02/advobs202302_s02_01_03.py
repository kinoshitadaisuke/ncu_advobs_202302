#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:09:57 (CST) daisuke>
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
array_b = numpy.linspace (100, 105, 6)

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

# making Numpy array "array_c" using numpy.linspace ()
array_c = numpy.linspace (1000, 1002, 3)

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

# concatenating array_a, array_b, and array_c and making Numpy array "array_d"
array_d = numpy.concatenate ([array_a, array_b, array_c])

# printing Numpy array
print (f'array_d:')
print (f'{array_d}')

# printing information
print (f'information:')
print (f'  ndim     = {array_d.ndim}')
print (f'  size     = {array_d.size}')
print (f'  shape    = {array_d.shape}')
print (f'  dtype    = {array_d.dtype}')
print (f'  itemsize = {array_d.itemsize} byte')
