#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/09 13:05:55 (CST) daisuke>
#

# importing numpy module
import numpy

# importing scipy module
import scipy.optimize

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'advobs202302_s04_07_03.eps'

# function of a curve
def curve (x):
    # coefficients
    a = 3.0
    b = 2.0 * numpy.pi
    c = numpy.pi
    d = 5.0
    # curve
    y = a * numpy.sin (b * x + c) + d
    # returning y-value
    return y

# finding minimum
minimum = scipy.optimize.minimize_scalar (curve, method='bounded', bounds=[0,1])

# printing minimum value
print (f'minimum: y={minimum.fun} at x={minimum.x}')

# data to plot
data_x = numpy.linspace (0.0, 1.0, 1001)
data_y = curve (data_x)

#
# making plot using Matplotlib
#
    
# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# axes
ax.set_xlabel ('X [arbitrary unit]')
ax.set_ylabel ('Y [arbitrary unit]')

# plotting data
ax.plot (data_x, data_y, linestyle='-', linewidth=3.0, color='blue', \
         label='$f(x)=3 \sin (2 \pi x + \pi) + 5$')
ax.plot (minimum.x, minimum.fun, linestyle='None', marker='o', \
         markersize=5.0, color='red', label='minimum')

# legend
ax.legend ()

# saving file
fig.savefig (file_output, dpi=225)
