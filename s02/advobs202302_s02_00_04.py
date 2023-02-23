#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 11:29:38 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray)
array5 = numpy.array ([0.1, 2.3, 4.5, 6.7, 8.9, 10.0, 12.3, 14.5, 16.7, 18.9])

# printing Numpy array
print (f'array5 = {array5}')

# type of "array5"
type_array5 = type (array5)

# printing type of "array5"
print (f'type of "array5" = {type_array5}')

# dimension of "array5"
ndim_array5 = array5.ndim

# size of "array5"
size_array5 = array5.size

# shape of "array5"
shape_array5 = array5.shape

# data type of elements in "array5"
dtype_array5 = array5.dtype

# size of one element in "array5"
itemsize_array5 = array5.itemsize

# printing information
print (f'information of "array5":')
print (f'  ndim     = {ndim_array5}')
print (f'  size     = {size_array5}')
print (f'  shape    = {shape_array5}')
print (f'  dtype    = {dtype_array5}')
print (f'  itemsize = {itemsize_array5} byte')
