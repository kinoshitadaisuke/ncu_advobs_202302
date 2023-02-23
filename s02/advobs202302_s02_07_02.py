#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 16:40:47 (CST) daisuke>
#

# importing numpy module
import numpy

# sample Numpy array
a = numpy.array ([10.0, 10.1, 9.9, 10.2, 9.8, 10.3, 9.7, \
                  300.0, 10.0, 10.0, 9.9, 9.9, 10.1, 10.1, 10.0])

# making a mask
mask = numpy.array ([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])

# making a masked array
a_masked = numpy.ma.array (a, mask=mask)

# printing array "a"
print (f'a:')
print (f'{a}')

# printing mask "mask"
print (f'mask:')
print (f'{mask}')

# printing masked array "a_masked"
print (f'a_masked:')
print (f'{a_masked}')

# calculation of mean of "a"
mean_a = numpy.mean (a)

# calculation of mean of "a_masked"
mean_a_masked = numpy.ma.mean (a_masked)

# printing mean values
print (f'numpy.mean (a) = {mean_a}')
print (f'numpy.ma.mean (a_masked) = {mean_a_masked}')
