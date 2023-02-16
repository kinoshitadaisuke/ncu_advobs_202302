#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/02/16 21:16:35 (CST) daisuke>
#

# printing odd number between 1 and 30
for i in range (1, 31):
    # if number is not divisible by 2, then skipping to next number
    if (i % 2 != 0):
        continue
    # if not, then it is an even number
    print (f'{i} is an even number.')
