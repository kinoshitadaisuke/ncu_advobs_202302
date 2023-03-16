#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 08:24:19 (CST) daisuke>
#

# importing Astropy module
import astropy.constants

# gravitational constant
G = astropy.constants.G

# printing gravitational constant G
print (f'G = {G.value} [{G.unit}] (Ref.: {G.reference})')
