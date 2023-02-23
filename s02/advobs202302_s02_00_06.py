#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 11:54:07 (CST) daisuke>
#

# importing numpy
import numpy

# making a Numpy array (ndarray)
array7 = numpy.array ([
    [
        [0.0, 1.0, 2.0], \
        [3.0, 4.0, 5.0], \
        [6.0, 7.0, 8.0]
    ],
    [
        [10.0, 11.0, 12.0], \
        [13.0, 14.0, 15.0], \
        [16.0, 17.0, 18.0]
    ]
])

# printing Numpy array
print (f'array7:')
print (f'{array7}')

# type of "array7"
type_array7 = type (array7)

# printing type of "array7"
print (f'type of "array7" = {type_array7}')

# dimension of "array7"
ndim_array7 = array7.ndim

# size of "array7"
size_array7 = array7.size

# shape of "array7"
shape_array7 = array7.shape

# data type of elements in "array7"
dtype_array7 = array7.dtype

# size of one element in "array7"
itemsize_array7 = array7.itemsize

# printing information
print (f'information of "array7":')
print (f'  ndim     = {ndim_array7}')
print (f'  size     = {size_array7}')
print (f'  shape    = {shape_array7}')
print (f'  dtype    = {dtype_array7}')
print (f'  itemsize = {itemsize_array7} byte')
