#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/23 15:56:53 (CST) daisuke>
#

# importing numpy module
import numpy

# making Numpy array
a = numpy.linspace (0.0, 10.0, 11)

# printing "a"
print (f'a:')
print (f'{a}')

# trying a.copy ()
b = a.copy ()

# printing "b"
print (f'b:')
print (f'{b}')

# IDs of "a" and "b"
print (f'id (a) = {id (a)}')
print (f'id (b) = {id (b)}')

# changing "a[5]"
a[5] += 10

# printing "a"
print (f'a:')
print (f'{a}')

# printing "b"
print (f'b:')
print (f'{b}')

# IDs of "a" and "b"
print (f'id (a) = {id (a)}')
print (f'id (b) = {id (b)}')
