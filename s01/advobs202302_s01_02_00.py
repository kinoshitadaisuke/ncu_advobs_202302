#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 18:43:56 (CST) daisuke>
#

# reading an integer number from keyboard typing
a_str = input ('Type one integer number: ')

# converting a string into integer
a = int (a_str)

# if and else statements
if (a % 2 == 0):
    print (f"The number {a:d} is an even number.")
else:
    print (f"The number {a:d} is an odd number.")
