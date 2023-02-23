#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 11:21:08 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray)
array4 = numpy.array ([0, 10, 20, 30, 40, 50, 60, 70])

# printing Numpy array
print (f'array4 = {array4}')

# type of "array4"
type_array4 = type (array4)

# printing type of "array4"
print (f'type of "array4" = {type_array4}')

# dimension of "array4"
ndim_array4 = array4.ndim

# size of "array4"
size_array4 = array4.size

# shape of "array4"
shape_array4 = array4.shape

# data type of elements in "array4"
dtype_array4 = array4.dtype

# size of one element in "array4"
itemsize_array4 = array4.itemsize

# printing information
print (f'information of "array4":')
print (f'  ndim     = {ndim_array4}')
print (f'  size     = {size_array4}')
print (f'  shape    = {shape_array4}')
print (f'  dtype    = {dtype_array4}')
print (f'  itemsize = {itemsize_array4} byte')
