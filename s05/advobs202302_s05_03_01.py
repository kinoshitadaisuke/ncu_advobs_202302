#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 12:31:37 (CST) daisuke>
#

# importing argparse module
import argparse

# constructing a parser object
parser = argparse.ArgumentParser (description='multiplying two numbers')

# adding arguments
parser.add_argument ('-a', type=float, default=1.0, help='number 1')
parser.add_argument ('-b', type=float, default=1.0, help='number 2')

# command-line argument analysis
args = parser.parse_args ()

# values
a = args.a
b = args.b

# calculation
c = a * b

# printing result
print (f'({a}) * ({b}) = {c}')
