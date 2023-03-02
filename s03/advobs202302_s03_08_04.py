#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 15:09:20 (CST) daisuke>
#

# importing gzip module
import gzip

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# catalogue file name
file_catalogue = 'catalog.gz'

# output file name
file_output = 'advobs202302_s03_08_04.png'

# dictionary for storing data
stars = {}

# opening catalogue file
with gzip.open (file_catalogue, 'rb') as fh:
    # reading catalogue line-by-line
    for line in fh:
        # Harvard Revised Number of star
        HR = line[0:4].strip ()
        # name
        name = line[4:14].strip ()
        # Vmag
        mag_V = line[102:107].strip ()
        # B-V colour
        colour_BV = line[109:114].strip ()
        # spectral type
        sptype = line[127:147].strip ()
        # dynamical parallax flag
        dynamical_parallax = line[160]
        # parallax
        parallax = line[161:166]

        # skip, if any of mag_V, colour_BV, parallax is missing
        if ( (mag_V == '') or (colour_BV == '') or (parallax == '') ):
            continue
        # skip, if parallax is dynamical parallax
        if (dynamical_parallax == 'D'):
            continue
        # reformat parallax
        if (parallax[:2] == '+.'):
            parallax = '+0.' + parallax[2:]

        # conversion from string to float
        try:
            mag_V     = float (mag_V)
        except:
            continue
        try:
            colour_BV = float (colour_BV)
        except:
            continue
        try:
            parallax  = float (parallax)
        except:
            continue

        # skip, if parallax is negative
        if (parallax < 0.0):
            continue

        # skip, if parallax is zero
        if (parallax < 10**-4):
            continue
    
        # distance in parsec
        dist_pc = 1.0 / parallax

        # absolute magnitude
        absmag_V = mag_V - 5.0 * numpy.log10 (dist_pc) + 5.0

        # constructing the dictionary
        stars[HR] = {}
        stars[HR]["mag_V"]     = mag_V
        stars[HR]["colour_BV"] = colour_BV
        stars[HR]["parallax"]  = parallax
        stars[HR]["dist_pc"]   = dist_pc
        stars[HR]["absmag_V"]  = absmag_V
        stars[HR]["sptype"]    = sptype
        stars[HR]["name"]      = name

# making empty numpy arrays for plotting
colour = numpy.array ([])
absmag = numpy.array ([])
label  = numpy.array ([], dtype=str)

# printing header
print ("# Vmag, (B-V), parallax, distance, absmag_V, HR, name")

# printing information of 1st mag stars
for key, value in sorted (stars.items (), key=lambda x: x[1]['mag_V']):
    # if mag of star is equal to or greater than 1.5, then skip
    if (stars[key]['mag_V'] >= 1.5):
        break
    # printing information
    print (f'{stars[key]["mag_V"]:+6.3f} ', \
           f'{stars[key]["colour_BV"]:+6.3f} ', \
           f'{stars[key]["parallax"]:+6.3f} ', \
           f'{stars[key]["dist_pc"]:+8.3f} ', \
           f'{stars[key]["absmag_V"]:+6.3f} ', \
           f'{int (key.decode ("utf-8")):4d} ', \
           f'{stars[key]["name"].decode ("utf-8")}')
    # appending data into numpy arrays
    colour = numpy.append (colour, stars[key]['colour_BV'])
    absmag = numpy.append (absmag, stars[key]['absmag_V'])
    label  = numpy.append (label, f'{stars[key]["name"].decode ("utf-8")}')

# making a fig object
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# adjustment of plot
box = ax.get_position ()
ax.set_position ([box.x0, box.y0, box.width * 0.8, box.height])

# labels
ax.set_xlabel ('$(B-V)$ Colour Index')
ax.set_ylabel ('Absolute Magnitude')

# flipping direction of Y-axis
ax.invert_yaxis ()

# plotting data
for i in range (len (colour)):
    size = 15 - i * 0.5
    ax.plot (colour[i], absmag[i], linestyle='None', marker='o', \
             markersize=size, label=label[i])

# grid
ax.grid ()

# legend
ax.legend (bbox_to_anchor=(1.0, 1.05), loc='upper left')

# saving the figure to a file
fig.savefig (file_output)
