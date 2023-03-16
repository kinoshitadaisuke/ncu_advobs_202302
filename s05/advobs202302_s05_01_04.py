#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 09:04:11 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.coordinates
import astropy.units

# units
u_hourangle = astropy.units.hourangle
u_deg       = astropy.units.deg

# equatorial coordinate of Antares (alpha Sco)
coo_antares = astropy.coordinates.SkyCoord ('16 29 24.46', '-26 25 55.2', \
                                            frame='icrs', \
                                            unit=(u_hourangle, u_deg) )

# printing coordinate
print (f'Antares:')
print (f'  (RA, Dec) = ({coo_antares.ra.deg} deg, {coo_antares.dec.deg} deg)')

# transformation into galactic coordinate
gal_antares = coo_antares.transform_to ('galactic')

# printing results
print (f'  (l, b)    = ({gal_antares.l.deg} deg, {gal_antares.b.deg} deg)')
