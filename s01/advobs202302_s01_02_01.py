#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 18:44:02 (CST) daisuke>
#

# reading an integer number from keyboard typing
a_str = input ('Type one integer number: ')

# converting a string into integer
a = int (a_str)

# if and else statements
if (a > 0):
    print (f"The number {a:d} is a positive number.")
elif (a < 0):
    print (f"The number {a:d} is a negative number.")
else:
    print (f"The number {a:d} is zero.")
