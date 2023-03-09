#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 12:02:04 (CST) daisuke>
#

# importing numpy module
import numpy

# importing scipy module
import scipy
import scipy.integrate

# function of a curve
def curve (x):
    # curve
    y = numpy.sqrt (4.0 - x**2)
    # returning a value
    return (y)

# range of integration
x0 = 0.0
x1 = 2.0

# numerical integration
result1 = scipy.integrate.quad (curve, x0, x1)

# printing result of numerical integration
print (f'integ. of sqrt (4-x) from 0 to 2 = {result1[0]} +/- {result1[1]}')
