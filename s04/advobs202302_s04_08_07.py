#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 13:36:33 (CST) daisuke>
#

# importing numpy module
import numpy

# importing scipy module
import scipy.stats

# output file name
file_output = 'advobs202302_s04_08_07.data'

# generating random numbers
err = scipy.stats.norm.rvs (loc=0.0, scale=2.0, size=16)

# function for a line
def curve (x):
    # coefficients
    a = 2.0
    b = 7.0
    c = 5.0
    # line
    y = a * (x - b)**2 + c
    # returning y
    return y

# synthetic data for least-squares method
data_x = numpy.linspace (0.0, 15.0, 16)
data_y = curve (data_x) + err

# opening file for writing
with open (file_output, 'w') as fh:
    # writing generated synthetic data into file
    for i in range (len (data_x)):
        fh.write (f'{data_x[i]:8.3f}    {data_y[i]:8.3f}\n')
