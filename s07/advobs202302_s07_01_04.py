#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 13:08:50 (CST) daisuke>
#

# importing Numpy module
import numpy

# creating a Numpy array using numpy.linspace
a = numpy.linspace (0.0, 100.0, 10001)

# printing Numpy array
print (f'a = {a}')

# printing size and total bytes of Numpy array
print (f'size        = {a.size}')
print (f'total bytes = {a.nbytes}')
