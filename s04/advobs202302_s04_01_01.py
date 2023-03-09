#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 10:20:00 (CST) daisuke>
#

# importing scipy module
import scipy.stats

# generating 100 random numbers of uniform distribution between 0.0 and 100.0
ru = scipy.stats.uniform.rvs (loc=0.0, scale=100.0, size=100)

# printing generated random numbers
print (f'generated random numbers:')
print (f'{ru}')

# checking type of object "ru"
type_ru = type (ru)

# printing type of object "ru"
print (f'type (ru) = {type_ru}')
