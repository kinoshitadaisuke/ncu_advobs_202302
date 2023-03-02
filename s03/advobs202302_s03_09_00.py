#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 15:20:31 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# output image file
file_image = 'advobs202302_s03_09_00.png'

# an ellipse
theta     = numpy.linspace (0.0, 2.0 * numpy.pi, 10**4)
ellipse_x = 5.0 * numpy.cos (theta)
ellipse_y = 3.0 * numpy.sin (theta)

# making a fig object using object-oriented interface
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# range of plot
ax.set_xlim (-6.0, +6.0)
ax.set_ylim (-6.0, +6.0)

# plotting ellipse
ax.plot (ellipse_x, ellipse_y, linestyle='-', linewidth=3.0, color='black', \
         label='Ellipse')

# plotting a point on the ellipse
x = numpy.deg2rad (45.0)
ax.plot (5.0 * numpy.cos (x), 3.0 * numpy.sin (x), linestyle='None', \
         color='red', marker='o', markersize=15.0, label='Point')

# aspect of plot
ax.set_aspect ('equal')

# saving file
fig.savefig (file_image)
