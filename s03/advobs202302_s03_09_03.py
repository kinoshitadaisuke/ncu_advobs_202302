#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/02 15:37:02 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.coordinates
import astropy.time
import astropy.units

# units
u_au = astropy.units.au

# setting for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('jpl')

# time t = 2023-03-03T00:00:00 (UTC)
t = astropy.time.Time ('2023-03-03T00:00:00', format='isot', scale='utc')

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
