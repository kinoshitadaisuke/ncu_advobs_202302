#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 15:31:06 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy arrays (2x2 matrix)
A = numpy.array ([ [1.0, 2.0], [3.0, 4.0] ])
B = numpy.array ([ [4.0, 2.0], [1.0, 3.0] ])

# printing A and B
print (f'A:')
print (f'{A}')
print (f'B:')
print (f'{B}')

# the other way to take a matrix product
C = A.dot (B)

# printing C
print (f'C = A.dot (B):')
print (f'{C}')
