#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 12:40:37 (CST) daisuke>
#

# importing matplotlib module
import matplotlib.pyplot

# data to be plotted
data_x = [1.0, 2.0, 3.0, 4.0, 5.0]
data_y = [3.0, 2.0, 5.0, 1.0, 4.0]

# output file name
file_output = 'advobs202302_s03_00_00.png'

#
# for making a plot using implicit pyplot interface, we call some functions
#

# plotting data using procedural pyplot interface
matplotlib.pyplot.plot (data_x, data_y, label="Sample data")

# adding legend to the plot
matplotlib.pyplot.legend ()

# saving a plot as a file
matplotlib.pyplot.savefig (file_output)
