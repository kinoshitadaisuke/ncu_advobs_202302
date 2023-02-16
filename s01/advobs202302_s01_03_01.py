#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 21:43:35 (CST) daisuke>
#

# importing sys module
import sys

# defining a function to calculate the distance between 2 points
def calc_distance (a, b):
    if (len (a) != len (b)):
        print (f"ERROR: inconsistent dimension")
        print (f"{a}")
        print (f"{b}")
        sys.exit (1)

    # a variable for distance
    dist = 0

    # calculation of distance
    for i in range (len (a)):
        dist += (a[i] - b[i])**2
    dist = dist**0.5
        
    # returning result of calculation
    return (dist)

# two points on 2-dimensional plane
a = (1.0, 2.0)
b = (4.0, 3.0)

# using the function "calc_distance"
distance_a_b = calc_distance (a, b)

# printing result
print (f'a = {a}')
print (f'b = {b}')
print (f'distance between a and b = {distance_a_b}')

# two points in 3-dimensional space
c = (1.0, 2.0, 3.0)
d = (4.0, 3.0, 2.0)

# using the function "calc_distance"
distance_c_d = calc_distance (c, d)

# printing result
print (f'c = {c}')
print (f'd = {d}')
print (f'distance between c and d = {distance_c_d}')
