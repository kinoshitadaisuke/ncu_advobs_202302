#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 10:46:56 (CST) daisuke>
#

# importing scipy module
import scipy.stats

# generating 10000 random numbers of Gaussian distribution
# of mean=100.0 and stddev=10.0
rg = scipy.stats.norm.rvs (loc=100.0, scale=10.0, size=10000)

# printing generated random numbers
print (f'generated random numbers:')
print (f'{rg}')

# finding minimum value
tmin = scipy.stats.tmin (rg)

# finding maximum value
tmax = scipy.stats.tmax (rg)

# calculation of arithmetic mean of distribution
mean = scipy.stats.tmean (rg)

# calculation of variance of distribution
var = scipy.stats.tvar (rg)

# calculation of standard deviation of distribution
stddev = scipy.stats.tstd (rg)

# calculation of zeroth moment about the mean
moment_0 = scipy.stats.moment (rg, moment=0)

# calculation of first moment about the mean
moment_1 = scipy.stats.moment (rg, moment=1)

# calculation of second moment about the mean
moment_2 = scipy.stats.moment (rg, moment=2)

# calculation of third moment about the mean
moment_3 = scipy.stats.moment (rg, moment=3)

# calculation of fourth moment about the mean
moment_4 = scipy.stats.moment (rg, moment=4)

# calculation of skewness
skew = scipy.stats.skew (rg)

# printing arithmetic mean and standard deviation of distribution
print (f'statistical values:')
print (f'  tmin          = {tmin:10.4f}')
print (f'  tmax          = {tmax:10.4f}')
print (f'  mean          = {mean:10.4f}')
print (f'  var           = {var:10.4f}')
print (f'  stddev        = {stddev:10.4f}')
print (f'  zeroth moment = {moment_0:10.4f}')
print (f'  first moment  = {moment_1:10.4f}')
print (f'  second moment = {moment_2:10.4f}')
print (f'  third moment  = {moment_3:10.4f}')
print (f'  fourth moment = {moment_4:10.4f}')
print (f'  skewness      = {skew:10.4f}')
