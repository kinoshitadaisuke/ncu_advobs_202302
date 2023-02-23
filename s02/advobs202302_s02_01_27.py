#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 15:35:45 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy array (2x2 matrix)
A = numpy.array ([ [5.0, 3.0], [6.0, 4.0] ])

# printing A
print (f'A:')
print (f'{A}')

# calculating inverse matrix of A
B = numpy.linalg.inv (A)

# priting B
print (f'B = A^-1:')
print (f'{B}')

# calculation of A @ B
C = A @ B

# printing C
print (f'C = A @ B:')
print (f'{C}')
