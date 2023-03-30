#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 16:12:46 (CST) daisuke>
#

# importing Numpy module
import numpy
import numpy.random

#
# parameters
#

# number of elements in X-axis and Y-axis
n_x   = 5
n_y   = 5

# mean and stddev for random number generation
mean  = 100.0
sigma =  10.0

#
# concatenating 10 2-dim. numpy arrays
#
for i in range (10):
    # making 2-dim numpy array
    rng   = numpy.random.default_rng ()
    array = rng.normal (mean, sigma, (n_x, n_y))
    # making 3-dim data cube
    if (i == 0):
        # if i=0, then copy "array" to "array0"
        array0 = numpy.copy (array)
    elif (i == 1):
        # if i=1, then make data cube using first and second arrays
        cube = numpy.concatenate ( ([array0], [array]), axis=0)
        # printing message
        print (f'now, making a data cube using first and second arrays.')
    else:
        # if i>1, then add 2-dim array into 3-dim data cube
        cube = numpy.concatenate ( (cube, [array]), axis=0)
        # printing message
        print (f'now, adding an array to data cube.')
        
# printing information of Numpy array "cube"
print (f'shape of cube = {cube.shape}')
