#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/11 21:29:41 (CST) daisuke>
#

# importing math module
import math

# importing uncertainties module
import uncertainties
import uncertainties.umath

# r'-band magnitude of star ID 12
mag_star1 = 13.718

# net flux of star ID 7
# 112347 +/- 364
flux_star1 = uncertainties.ufloat (112347, 364)

# net flux of star ID 13
# 52351 +/- 267
flux_star2 = uncertainties.ufloat (52351, 267)

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
