#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/11 20:12:25 (CST) daisuke>
#

# importing math module
import math

# importing uncertainties module
import uncertainties
import uncertainties.umath

# r'-band magnitude of star ID 12
mag_star1 = 14.339

# net flux of star ID 12
# 1712.5 +/- 41.4
flux_star1 = uncertainties.ufloat (1712.5, 41.4)

# net flux of star ID 16
# 1105.8 +/- 33.3
flux_star2 = uncertainties.ufloat (1105.8, 33.3)

# r'-band magnitude of star ID 16
mag_star2 \
    = mag_star1 - 2.5 * uncertainties.umath.log10 (flux_star2 / flux_star1)

# printing result
print (f'#')
print (f'# input parameters')
print (f'#')
print (f'#  mag_star1  = {mag_star1}')
print (f'#  flux_star1 = {flux_star1}')
print (f'#  flux_star2 = {flux_star2}')
print (f'#')
print (f'mag_star2 = {mag_star2}')
