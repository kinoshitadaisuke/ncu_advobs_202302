#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:59:17 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays using numpy.linspace ()
a = numpy.array ([0.0, 0.5, numpy.sqrt (2.0) / 2.0, numpy.sqrt (3.0) / 2.0, 1.0])

# printing a
print (f'a = {a}')

# using arcsin
b_rad = numpy.arcsin (a)

# printing b_rad
print (f'b_rad = {b_rad}')

# conversion from radian into degree
b_deg = numpy.rad2deg (b_rad)

# printing b_deg
print (f'b_deg = {b_deg}')
