#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/11 20:04:46 (CST) daisuke>
#

# importing math module
import math

# r'-band magnitude of star ID 12
mag_star1 = 14.339

# net flux of star ID 12
flux_star1 = 1712.5

# flux error of star ID 12
err_star1 = 41.4

# net flux of star ID 16
flux_star2 = 1105.8

# flux error of star ID 16
err_star2 = 33.3

# r'-band magnitude of star ID 16
mag_star2 = mag_star1 - 2.5 * math.log10 (flux_star2 / flux_star1)

# error on magnitude
magerr_star1 = 2.5 * math.log10 (1 + err_star1 / flux_star1)
magerr_star2 = 2.5 * math.log10 (1 + err_star2 / flux_star2)
magerr_total = math.sqrt (magerr_star1**2 + magerr_star2**2)

# printing result
print (f'#')
print (f'# input parameters')
print (f'#')
print (f'#  mag_star1  = {mag_star1}')
print (f'#  flux_star1 = {flux_star1} ADU')
print (f'#  err_star1  = {err_star1} ADU')
print (f'#  flux_star2 = {flux_star2} ADU')
print (f'#  err_star2  = {err_star2} ADU')
print (f'#')
print (f'mag_star2 = {mag_star2} +/- {magerr_total}')
