#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 14:28:42 (CST) daisuke>
#

# importing numpy module
import numpy

# parameters for random number generation
mean   = 100.0
stddev = 10.0
n      = 10**4

# generating random numbers
rng  = numpy.random.default_rng ()
dist = rng.normal (loc=mean, scale=stddev, size=n)

# printing generated random numbers
print (f'generated random numbers:')
print (f'{dist}')
print (f'number of generated random numbers = {len (dist):g}')
