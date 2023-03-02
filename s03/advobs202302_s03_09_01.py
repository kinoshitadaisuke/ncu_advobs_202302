#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 15:23:37 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib.animation
import matplotlib.backends.backend_agg
import matplotlib.figure

# output animation file
file_anim  = 'advobs202302_s03_09_01.mp4'

# an ellipse
theta     = numpy.linspace (0.0, 2.0 * numpy.pi, 10**4)
ellipse_x = 5.0 * numpy.cos (theta)
ellipse_y = 3.0 * numpy.sin (theta)

# number of frames for animation
n_frame = 600

# an empty list for storing frames for animation
list_frame = []

# making a fig object using object-oriented interface
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

for i in range (n_frame):
    # initialisation of object list for plotting
    list_obj = []

    # range of plot
    ax.set_xlim (-6.0, +6.0)
    ax.set_ylim (-6.0, +6.0)

    # plotting ellipse
    ellipse, = ax.plot (ellipse_x, ellipse_y, linestyle='-', linewidth=3.0, \
                        color='black', label='Ellipse')
    list_obj.append (ellipse)

    # plotting a point
    x = numpy.deg2rad (i / n_frame * 720.0)
    point, = ax.plot (5.0 * numpy.cos (x), 3.0 * numpy.sin (x), \
                      linestyle='None', color='red', marker='o', \
                      markersize=15.0, label='Point')
    list_obj.append (point)

    # aspect of plot
    ax.set_aspect ('equal')

    # appending frame
    list_frame.append (list_obj)

# making animation
anim = matplotlib.animation.ArtistAnimation (fig, list_frame, interval=50)

# saving file
anim.save (file_anim)
