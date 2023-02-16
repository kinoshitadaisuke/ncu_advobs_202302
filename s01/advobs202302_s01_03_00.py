#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 21:25:53 (CST) daisuke>
#

# defining a function to add two numbers
def add_two_numbers (a, b):
    # adding two numbers
    c = a + b
    # returning result of calculation
    return (c)

# two numbers
n1 = 11
n2 = 23

# using the function "add_two_numbers"
n3 = add_two_numbers (n1, n2)

# printing result
print (f'n1 = {n1}')
print (f'n2 = {n2}')
print (f'n3 = n1 + n2 = {n3}')
