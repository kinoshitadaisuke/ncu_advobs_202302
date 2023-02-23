#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 11:33:31 (CST) daisuke>
#

# importing numpy
import numpy

# making a Numpy array (ndarray)
array6 = numpy.array ([ [0.0, 1.5, 2.0, 3.6, 4.4], \
                        [5.7, 6.3, 7.8, 8.2, 9.9], \
                        [10.1, 11.0, 12.1, 13.2, 14.3] ])

# printing Numpy array
print (f'array6:')
print (f'{array6}')

# type of "array6"
type_array6 = type (array6)

# printing type of "array6"
print (f'type of "array6" = {type_array6}')

# dimension of "array6"
ndim_array6 = array6.ndim

# size of "array6"
size_array6 = array6.size

# shape of "array6"
shape_array6 = array6.shape

# data type of elements in "array6"
dtype_array6 = array6.dtype

# size of one element in "array6"
itemsize_array6 = array6.itemsize

# printing information
print (f'information of "array6":')
print (f'  ndim     = {ndim_array6}')
print (f'  size     = {size_array6}')
print (f'  shape    = {shape_array6}')
print (f'  dtype    = {dtype_array6}')
print (f'  itemsize = {itemsize_array6} byte')
