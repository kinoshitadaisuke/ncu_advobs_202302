#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 08:54:55 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.coordinates
import astropy.units

# equatorial coordinate of Regulus (alpha Leo)
coo_regulus = astropy.coordinates.SkyCoord ('10h08m22.31s', '+11d58m02.0s', \
                                            frame='icrs')

# printing coordinate
print (f'Regulus:')
print (f'  (RA, Dec)      = ({coo_regulus.ra}, {coo_regulus.dec})')

# transformation into ecliptic coordinate
ecl_regulus = coo_regulus.transform_to ('geocentricmeanecliptic')

# printing results
print (f'  (lambda, beta) = ({ecl_regulus.lon}, {ecl_regulus.lat})')
