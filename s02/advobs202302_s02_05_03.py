#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 16:13:42 (CST) daisuke>
#

# importing numpy module
import numpy

# random number generator
rng = numpy.random.default_rng ()

# generating 10 random numbers of Gaussian distribution
# of mean of 100.0 and standard deviation of 10.0
r = rng.normal (100.0, 10.0, 10)

# printing generated random numbers
print (f'{r}')
