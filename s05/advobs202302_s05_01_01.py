#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 08:37:00 (CST) daisuke>
#

# importing astropy module
import astropy.units

# units
u_m  = astropy.units.m
u_pc = astropy.units.pc

# distance in pc
dist_pc = 10.0 * u_pc

# converting the distance in pc into metre
dist_m = dist_pc.to (u_m)

# printing result
print (f'{dist_pc.value:g} [{dist_pc.unit}] = {dist_m.value:g} [{dist_m.unit}]')
