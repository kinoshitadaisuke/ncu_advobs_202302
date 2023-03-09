#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 10:20:05 (CST) daisuke>
#

# importing scipy module
import scipy.stats

# generating 100 random numbers of Gaussian distribution
# of mean=100.0 and stddev=10.0
rg = scipy.stats.norm.rvs (loc=100.0, scale=10.0, size=100)

# printing generated random numbers
print (f'generated random numbers:')
print (f'{rg}')
