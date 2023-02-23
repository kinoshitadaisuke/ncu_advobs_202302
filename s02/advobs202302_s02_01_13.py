#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 14:43:06 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays using numpy.linspace ()
a_deg = numpy.linspace (0.0, 180.0, 7)

# printing a_deg
print (f'a_deg = {a_deg}')

# conversion of angle in degree into angle in radian
a_rad = numpy.radians (a_deg)

# printing a_rad
print (f'a_rad = {a_rad}')

# conversion of angle in radian into angle in degree
b_deg = numpy.degrees (a_rad)

# printing b_deg
print (f"b_deg = {b_deg}")
