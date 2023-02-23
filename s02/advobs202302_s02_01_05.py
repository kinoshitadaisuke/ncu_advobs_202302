#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:17:53 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays using numpy.linspace ()
a = numpy.linspace (0.0, 9.0, 10)
b = numpy.linspace (10.0, 19.0, 10)
c = numpy.linspace (100.0, 109.0, 10)

# printing a and b
print (f'a = {a}')
print (f'b = {b}')
print (f'c = {c}')

# calculation
# no need of using "for"
d = a + b + c

# printing c
print (f'd = a + b + c = {d}')
