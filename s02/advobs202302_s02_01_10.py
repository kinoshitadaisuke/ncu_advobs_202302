#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:26:51 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays using numpy.linspace ()
a = numpy.linspace (0.0, 10.0, 11)

# printing a
print (f'a = {a}')

# calculation
# no need of using "for"
b = a**3

# printing b
print (f'b = a**3 = {b}')
