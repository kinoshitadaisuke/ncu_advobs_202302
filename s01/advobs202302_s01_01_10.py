#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 18:20:35 (CST) daisuke>
#

# importing math module
import math

# value of pi
pi = math.pi

# angle in degree
a_deg = 30.0

# angle in radian
a_rad = a_deg / 180.0 * pi

# calculation of sine
sin_a = math.sin (a_rad)

# printing result of calculation
print (f'pi          = {pi}')
print (f'a_deg       = {a_deg} deg')
print (f'a_rad       = {a_rad} rad')
print (f'sin (a_rad) = sin ({a_rad}) = {sin_a}')
