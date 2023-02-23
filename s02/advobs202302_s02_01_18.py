#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 15:08:41 (CST) daisuke>
#

# importing numpy module
import numpy

# making 2-dim. Numpy arrays
a = numpy.array ([ [1, 2], [3, 4] ])
b = numpy.array ([ [5, 6], [7, 8] ])

# printing a and b
print (f'a:')
print (f'{a}')
print (f'b:')
print (f'{b}')

# calculation
# no need of using "for"
c = a - b

# printing c
print (f'c = a - b:')
print (f'{c}')
