#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 12:04:31 (CST) daisuke>
#

# importing matplotlib module
import matplotlib.pyplot

# data to be plotted
data_x = [1.0, 2.0, 3.0, 4.0, 5.0]
data_y = [3.0, 2.0, 5.0, 1.0, 4.0]

# output file name
file_output = 'advobs202302_s03_00_01.png'

#
# for making a plot using object-oriented interface,
# we first construct "fig" and "axes" objects,
# and then use methods for these "fig" and "axes".
#

# making a "fig" object using a function "matplot.pyplot.figure ()"
fig = matplotlib.pyplot.figure ()

# constructing an axes object using object-oriented interface
ax = fig.add_subplot (111)

# plotting data using object-oriented interface
ax.plot (data_x, data_y, label='Sample data')

# adding legend to the plot
ax.legend ()

# saving a plot as a file
fig.savefig (file_output)
