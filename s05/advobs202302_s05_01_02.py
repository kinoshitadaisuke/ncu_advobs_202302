#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/16 08:41:43 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.time

# time "t1"
t1 = astropy.time.Time ('2023-03-17T12:00:00.000', format='isot', scale='utc')

# JD corrensponding to time "t1"
t1_jd = t1.jd

# printing the time "t1"
print (f't1 = {t1} = {t1_jd}')

# time "t2"
t2 = astropy.time.Time ('2000-01-01T12:00:00.000', format='isot', scale='utc')

# JD corrensponding to time "t2"
t2_jd = t2.jd

# printing the time "t2"
print (f't2 = {t2} = {t2_jd}')

# calculating the time difference between "t1" and "t2"
dt = t1 - t2

# printing "dt"
print (f'dt = t1 - t2 = {dt} [day] = {dt.sec} [sec]')
