#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 09:21:11 (CST) daisuke>
#

# importing numpy module
import numpy

# importing astropy module
import astropy
import astropy.modeling.models
import astropy.units

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# parameters
file_output = 'advobs202302_s05_01_05.png'
T_eff       = 10000.0

# units
unit_micron = astropy.units.micron
unit_K      = astropy.units.K

# wavelength
wl_min = -8.0
wl_max = -4.0
n_wl   = 10**4
wl     = numpy.logspace (wl_min, wl_max, num=n_wl) * 10**6 * unit_micron

# temperature
T_eff_K = T_eff * unit_K

# making a blackbody model
bb = astropy.modeling.models.BlackBody (temperature=T_eff_K)

# generating blackbody curve data
bb_data = bb (wl)

# making objects "fig" and "ax" for plotting
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Wavelength [micron]'
label_y = 'Spectral Radiance [erg sec^-1 cm^-2, sr^-1 Hz^-1]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# axes
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim (0.01, 100)
ax.set_ylim (10**-10, 10**0)
ax.grid ()

# label
T_str = f'{T_eff:5.0f} K blackbody'

# plotting data
ax.plot (wl, bb_data, '-', linewidth=3, label=T_str)
ax.legend ()

# saving the plot into a file
fig.savefig (file_output, dpi=225)
