#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 15:44:09 (CST) daisuke>
#

# importing sys module
import sys

# importing astropy module
import astropy
import astropy.coordinates
import astropy.time
import astropy.units

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# output file name
file_output = 'advobs202302_s03_09_04.png'

# units
u_au = astropy.units.au

# setting for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('jpl')

# date/time
t_str = f'2023-03-03T00:00:00'
    
# Astropy's time object
t = astropy.time.Time (t_str, format='isot', scale='utc')

# getting positions of Sun, Earth, and Moon
sun     = astropy.coordinates.get_body_barycentric ('sun', t)
mercury = astropy.coordinates.get_body_barycentric ('mercury', t)
venus   = astropy.coordinates.get_body_barycentric ('venus', t)
earth   = astropy.coordinates.get_body_barycentric ('earth', t)
mars    = astropy.coordinates.get_body_barycentric ('mars', t)

# printing positions of the Sun and planets
print (f'Positions of the Sun and the planets at t = {t}')
print (f'  Sun:')
print (f'    X = {sun.x:+15.3f} = {sun.x.to (u_au).value:+8.5f} au')
print (f'    Y = {sun.y:+15.3f} = {sun.y.to (u_au).value:+8.5f} au')
print (f'    Z = {sun.z:+15.3f} = {sun.z.to (u_au).value:+8.5f} au')
print (f'  Mercury:')
print (f'    X = {mercury.x:+15.3f} = {mercury.x.to (u_au).value:+8.5f} au')
print (f'    Y = {mercury.y:+15.3f} = {mercury.y.to (u_au).value:+8.5f} au')
print (f'    Z = {mercury.z:+15.3f} = {mercury.z.to (u_au).value:+8.5f} au')
print (f'  Venus:')
print (f'    X = {venus.x:+15.3f} = {venus.x.to (u_au).value:+8.5f} au')
print (f'    Y = {venus.y:+15.3f} = {venus.y.to (u_au).value:+8.5f} au')
print (f'    Z = {venus.z:+15.3f} = {venus.z.to (u_au).value:+8.5f} au')
print (f'  Earth:')
print (f'    X = {earth.x:+15.3f} = {earth.x.to (u_au).value:+8.5f} au')
print (f'    Y = {earth.y:+15.3f} = {earth.y.to (u_au).value:+8.5f} au')
print (f'    Z = {earth.z:+15.3f} = {earth.z.to (u_au).value:+8.5f} au')
print (f'  Mars:')
print (f'    X = {mars.x:+15.3f} = {mars.x.to (u_au).value:+8.5f} au')
print (f'    Y = {mars.y:+15.3f} = {mars.y.to (u_au).value:+8.5f} au')
print (f'    Z = {mars.z:+15.3f} = {mars.z.to (u_au).value:+8.5f} au')

# making a fig object using object-oriented interface
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# settings for plot
ax.set_aspect ('equal')
ax.set_xlim (-2.0, +2.0)
ax.set_ylim (-2.0, +2.0)
ax.set_xlabel ("X [au]")
ax.set_ylabel ("Y [au]")
ax.set_title ("Positions of the Sun and planets")

# plotting the Sun
ax.plot (sun.x.to (u_au).value, sun.y.to (u_au).value, \
         marker='o', markersize=25, color='yellow', label='Sun')
ax.text (sun.x.to (u_au).value + 0.1, sun.y.to (u_au).value - 0.3, \
         f'Sun')

# plotting Mercury
ax.plot (mercury.x.to (u_au).value, mercury.y.to (u_au).value, \
         marker='o', markersize=5, color='cyan', label='Mercury')
ax.text (mercury.x.to (u_au).value + 0.1, mercury.y.to (u_au).value - 0.3, \
         f'Mercury')

# plotting Venus
ax.plot (venus.x.to (u_au).value, venus.y.to (u_au).value, \
         marker='o', markersize=15, color='gold', label='Venus')
ax.text (venus.x.to (u_au).value + 0.1, venus.y.to (u_au).value - 0.3, \
         f'Venus')

# plotting Earth
ax.plot (earth.x.to (u_au).value, earth.y.to (u_au).value, \
         marker='o', markersize=15, color='blue', label='Earth')
ax.text (earth.x.to (u_au).value + 0.1, earth.y.to (u_au).value - 0.3, \
         f'Earth')

# plotting Mars
ax.plot (mars.x.to (u_au).value, mars.y.to (u_au).value, \
         marker='o', markersize=10, color='red', label='Mars')
ax.text (mars.x.to (u_au).value + 0.1, mars.y.to (u_au).value - 0.3, \
         f'Mars')

# plotting the time
ax.text (-1.9, -1.9, f'Date/Time: {t} (UTC)')

# grid
ax.grid ()

# saving plot
fig.savefig (file_output, dpi=225)
