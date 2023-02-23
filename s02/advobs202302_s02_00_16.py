#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 12:56:47 (CST) daisuke>
#

# importing numpy module
import numpy

# making a Numpy array (ndarray) with a specified data type
array17 = numpy.array (['Ceres', 'Pallas', 'Juno', 'Vesta', 'Astraea', \
                        'Hebe', 'Iris', 'Flora', 'Metis', 'Hygiea'], \
                       dtype=numpy.dtype ('U10') )

# printing Numpy array
print (f'array17:\n{array17}')

# printing information
print (f'information:')
print (f'  ndim     = {array17.ndim}')
print (f'  size     = {array17.size}')
print (f'  shape    = {array17.shape}')
print (f'  dtype    = {array17.dtype}')
print (f'  itemsize = {array17.itemsize} byte')
