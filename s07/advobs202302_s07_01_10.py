#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 16:08:35 (CST) daisuke>
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
# making 2-dim. numpy arrays
#

# creating Numpy arrays
rng = numpy.random.default_rng ()
a   = rng.normal (mean, sigma, (n_x, n_y))
b   = rng.normal (mean, sigma, (n_x, n_y))
c   = rng.normal (mean, sigma, (n_x, n_y))

# printing information of Numpy arrays
print (f'a:')
print (f'{a}')
print (f'shape of a = {a.shape}')
print (f'b:')
print (f'{b}')
print (f'shape of b = {b.shape}')
print (f'c:')
print (f'{c}')
print (f'shape of c = {c.shape}')

# concatenating array "a" and array "b"
cube = numpy.concatenate ( ([a], [b]), axis=0 )

# printing "cube"
print (f'cube:')
print (f'{cube}')

# printing information of Numpy array "cube"
print (f'shape of cube = {cube.shape}')

# concatenating one more array "c" to "cube"
cube = numpy.concatenate ( (cube, [c]), axis=0)

# printing "cube"
print (f'cube:')
print (f'{cube}')

# printing information of Numpy array "cube"
print (f'shape of cube = {cube.shape}')
