#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:34:13 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays using numpy.logspace ()
a = numpy.logspace (-4.0, 4.0, 9)

# printing a
print (f'a = {a}')

# calculation
# no need of using "for"
b = numpy.log10 (a)

# printing b
print (f'b = numpy.log10 (a) = {b}')
