#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 13:36:12 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# data to be plotted
data_x = numpy.concatenate ([
    numpy.linspace (1.0, 4.0, 4), \
    numpy.linspace (1.0, 4.0, 4), \
    numpy.linspace (1.0, 4.0, 4), \
    numpy.linspace (1.0, 4.0, 4) ])
data_y = numpy.concatenate ([
    numpy.repeat (1.0, 4), \
    numpy.repeat (2.0, 4), \
    numpy.repeat (3.0, 4), \
    numpy.repeat (4.0, 4) ])

# list of markers
list_marker = [
    '.', 'o', 'v', '^', \
    '<', '>', 's', 'p', \
    'P', '*', 'h', '+', \
    'x', 'X', 'D', 'd' \
]

# list of labels
list_label = [
    'marker="."', 'marker="o"', 'marker="v"', 'marker="^"', \
    'marker="<"', 'marker=">"', 'marker="s"', 'marker="p"', \
    'marker="P"', 'marker="*"', 'marker="h"', 'marker="+"', \
    'marker="x"', 'marker="X"', 'marker="D"', 'marker="d"' \
]

# output file name
file_output = 'advobs202302_s03_03_01.png'

# making a fig object
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# making a plot using object-oriented interface
for i in range (len (data_x)):
    ax.plot (data_x[i], data_y[i], ls='None', marker=list_marker[i], \
             label=list_label[i])

# setting ranges of x-axis and y-axis
ax.set_xlim (0.0, +8.0)
ax.set_ylim (0.0, +6.0)

# setting labels for x-axis and y-axis
ax.set_xlabel ('$x$')
ax.set_ylabel ('$y$')

# setting ticks
ax.set_xticks (numpy.linspace (0.0, +8.0, 9))
ax.set_yticks (numpy.linspace (0.0, +6.0, 7))

# setting aspect ratio
ax.set_aspect ('equal')

# showing grid
ax.grid ()

# adding legend to the plot
ax.legend ()

# saving a plot as a file
fig.savefig (file_output)
