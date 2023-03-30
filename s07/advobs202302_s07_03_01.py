#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/30 22:36:06 (CST) daisuke>
#

# importing numpy module
import numpy

# sample data set 1
data1 = numpy.array ([10.0, 10.0, 9.0, 9.0, 11.0, 11.0])

# number of elements
data1_n = data1.size

# calculation of sum
data1_sum = data1.sum ()

# calculation of simple mean
data1_mean = numpy.mean (data1)

# calculation of simple mean using numpy.nanmean
data1_nanmean = numpy.nanmean (data1)

# printing result
print (f'data1: {data1}')
print (f'  data1_n       = {data1_n}')
print (f'  data1_sum     = {data1_sum}')
print (f'  data1_mean    = {data1_mean}')
print (f'  data1_nanmean = {data1_nanmean}')

# sample data set 2 with NaN value
data2 = numpy.array ([numpy.nan, 10.0, 10.0, 9.0, 9.0, 11.0, 11.0, numpy.nan])

# number of elements
data2_n = data2.size

# calculation of sum
data2_sum = data2.sum ()

# calculation of simple mean
data2_mean = numpy.mean (data2)

# calculation of simple mean using numpy.nanmean
data2_nanmean = numpy.nanmean (data2)

# printing result
print (f'data2: {data2}')
print (f'  data2_n       = {data2_n}')
print (f'  data2_sum     = {data2_sum}')
print (f'  data2_mean    = {data2_mean}')
print (f'  data2_nanmean = {data2_nanmean}')
