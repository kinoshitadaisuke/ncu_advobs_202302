#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/17 09:39:40 (CST) daisuke>
#

# importing argparse module
import argparse

# importing math module
import math

# constructing a parser object
desc = 'calculation of trigonometric functions'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-f', choices=['sin', 'cos', 'tan'], default='sin', \
                     help='number 1')
parser.add_argument ('angle', type=float, help='angle in degree')

# command-line argument analysis
args = parser.parse_args ()

# values
func  = args.f
x_deg = args.angle

# value of pi
pi = math.pi

# calculation
if (func == 'sin'):
    y = math.sin (x_deg / 180.0 * pi)
elif (func == 'cos'):
    y = math.cos (x_deg / 180.0 * pi)
elif (func == 'tan'):
    y = math.tan (x_deg / 180.0 * pi)

# printing result
print (f'{func} ({x_deg} [deg]) = {y}')
