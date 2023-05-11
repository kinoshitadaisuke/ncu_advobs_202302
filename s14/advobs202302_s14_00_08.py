#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/05/11 21:26:19 (CST) daisuke>
#

# importing math module
import math

# r'-band magnitude of star ID 7
mag_star1 = 13.718

# net flux of star ID 7
flux_star1 = 112347

# flux error of star ID 7
err_star1 = 364

# net flux of star ID 13
flux_star2 = 52351

# flux error of star ID 13
err_star2 = 267

# r'-band magnitude of star ID 13
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
