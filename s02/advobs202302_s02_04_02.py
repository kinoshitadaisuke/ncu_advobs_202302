#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 16:05:30 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy array
a = numpy.array ([5.0, 3.0, 7.0, 4.0, 9.0, 8.0, 1.0, 6.0, 2.0, 0.0])

# printing "a"
print (f'a:')
print (f'{a}')

# sorting by descending order
b = numpy.sort (a) [::-1]

# printing "b"
print (f'b = numpy.sort (a) [::-1]:')
print (f'{b}')
