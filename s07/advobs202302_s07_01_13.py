#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 16:06:20 (CST) daisuke>
#

# importing Numpy module
import numpy
import numpy.random

# importing Astropy module
import astropy.stats

# number of elements in X-axis, Y-axis, and Z-axis
n_x = 256
n_y = 256
n_z = 100

# mean and stddev for random number generation
mean  = 3000.0
sigma =  100.0

# printing header
print (f'# {"array":<14s} {"min":>10s} {"max":>10s}', \
       f'{"mean":>10s} {"median":>10s} {"stddev":>10s}')

# creating a data cube from a set of 2-dim. arrays
for i in range (n_z):
    # creating 2-dim. array
    tmp = numpy.random.normal (mean, sigma, (n_x, n_y) )

    # choosing a pixel for an outlier
    rng = numpy.random.default_rng ()
    x = int ( rng.uniform (0, n_x) )
    y = int ( rng.uniform (0, n_y) )
    # adding an outlier of value around 30,000
    tmp[x,y] += rng.uniform (50000, 250000)

    # printing statistical value of an array
    print (f'array {i:03d}       ', \
           f'{numpy.amin (tmp):10.3f}', \
           f'{numpy.amax (tmp):10.3f}', \
           f'{numpy.mean (tmp):10.3f}', \
           f'{numpy.median (tmp):10.3f}', \
           f'{numpy.std (tmp):10.3f}')
    
    # concatenating 2-dim. arrays to make a data cube
    if (i == 0):
        # for the first 2-dim. array, copy it to "tmp0"
        tmp0 = tmp
    elif (i == 1):
        # for the second 2-dim. array, make a 3-dim. array "cube"
        # by concatenating "tmp0" and "tmp" using the function concatenate
        cube = numpy.concatenate ( ([tmp0], [tmp]), axis=0 )
    else:
        # for other 2-dim. arrays, concatenate "tmp"
        # to the 3-dim. array "cube"
        cube = numpy.concatenate ( (cube, [tmp]), axis=0 )

# printing information of "cube"
print (f'shape of cube             = {cube.shape}')

# combining 2-dim. arrays using simple average
combined_simple = numpy.mean (cube, axis=0)

# printing information of "combined_simple"
print (f'shape of combined_simple  = {combined_simple.shape}')

# combining 2-dim. arrays using sigma clipping
#   threshold = mean +/- 3.0 times of stddev
#   max number of iterations = 10
#   calculation of average = mean
combined_sigclip, median, stddev \
    = astropy.stats.sigma_clipped_stats (cube, sigma=3.0, maxiters=10, \
                                         cenfunc='mean', stdfunc='std', \
                                         axis=0)

# printing information of "combined"
print (f'shape of combined_sigclip = {combined_sigclip.shape}')

# printing min, max, mean, median, standard deviation of combined arrays
print (f'# {"array":<14s} {"min":>10s} {"max":>10s}', \
       f'{"mean":>10s} {"median":>10s} {"stddev":>10s}')
print (f'combined_simple ', \
       f'{numpy.amin (combined_simple):10.3f}', \
       f'{numpy.amax (combined_simple):10.3f}', \
       f'{numpy.mean (combined_simple):10.3f}', \
       f'{numpy.median (combined_simple):10.3f}', \
       f'{numpy.std (combined_simple):10.3f}')
print (f'combined_sigclip', \
       f'{numpy.amin (combined_sigclip):10.3f}', \
       f'{numpy.amax (combined_sigclip):10.3f}', \
       f'{numpy.mean (combined_sigclip):10.3f}', \
       f'{numpy.median (combined_sigclip):10.3f}', \
       f'{numpy.std (combined_sigclip):10.3f}')
