#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/31 00:43:18 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing scipy module
import scipy.optimize

# importing astropy module
import astropy.io.fits
import astropy.stats

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# making empty numpy arrays for plotting
data_exptime = numpy.array ([], dtype='float64')
data_mean    = numpy.array ([], dtype='float64')
data_stddev  = numpy.array ([], dtype='float64')

# construction of parser object
desc   = 'Making a plot of exposure time vs mean pixel value of dark frame'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='mean', \
                     help='method to estimate centre value (default: mean)')
parser.add_argument ('-o', '--output', default='dark.png', \
                     help='output image file')
parser.add_argument ('-d', '--resolution', type=int, default=300, \
                     help='resolution of output file (default: 300 dpi)')
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
list_input  = args.files
file_output = args.output
rejection   = args.rejection
threshold   = args.threshold
cenfunc     = args.cenfunc
maxiters    = args.maxiters
resolution  = args.resolution

# checking input files
for file_fits in list_input:
    # making pathlib object
    path_fits = pathlib.Path (file_fits)

    # if the file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print (f'ERROR: Input files must be FITS files!')
        print (f'ERROR: The file "{file_fits}" is not a FITS file!')
        # exit the script
        sys.exit ()

    # existence check
    if not (path_fits.exists ()):
        # printing error message
        print (f'ERROR: the file "{file_fits}" does not exist!')
        # exit the script
        sys.exit ()

# making pathlib object
path_output = pathlib.Path (file_output)

# checking output file
# if the file is not a PNG or PDF or PS file, then stop the script
if not ( (path_output.suffix == '.eps') \
         or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') \
         or (path_output.suffix == '.ps') ):
    # printing error message
    print (f'Output file must be EPS, or PDF, or PNG, or PS file!')
    # exit the script
    sys.exit ()

# existence check
if (path_output.exists ()):
    # printing error message
    print (f'ERROR: the file "{file_output}" exists!')
    # exit the script
    sys.exit ()

# reading FITS files and calculating mean and stddev
for file_fits in list_input:
    # opening FITS file
    with astropy.io.fits.open (file_fits) as hdu_list:
        # primary HDU
        hdu0 = hdu_list[0]

        # reading header
        header0 = hdu0.header

        # reading data
        data0 = hdu0.data

    # exposure time
    exptime = header0['EXPTIME']

    # mean value
    if (rejection == 'sigclip'):
        # calculation of mean, median, and stddev using sigma-clipping
        mean, median, stddev \
            = astropy.stats.sigma_clipped_stats (data0, sigma=threshold, \
                                                 maxiters=maxiters, \
                                                 cenfunc=cenfunc, \
                                                 stdfunc='std')
    elif (rejection == 'none'):
        # calculation of simple mean and stddev
        mean   = numpy.nanmean (data0)
        stddev = numpy.nanstd (data0)

    # appending data to numpy arrays
    data_exptime = numpy.append (data_exptime, exptime)
    data_mean    = numpy.append (data_mean, mean)
    data_stddev  = numpy.append (data_stddev, stddev)

# printing data which will be used for plotting
print (f'data_exptime:')
print (f'{data_exptime}')
print (f'data_mean:')
print (f'{data_mean}')
print (f'data_stddev:')
print (f'{data_stddev}')

#
# least-squares method using SciPy
#

# initial values of coefficients of fitted function
a = 1.0
b = 1.0

# function for least-squares fitting
def func (x, a, b):
    # f(x) = ax + b
    y = a * x + b
    return y

# weighted least-squares fitting
# x: data_exptime
# y: data_mean
# Delta y: data_stddev
popt, pcov = scipy.optimize.curve_fit (func, data_exptime, data_mean, \
                                       p0=(a,b), sigma=data_stddev)

# fitted coefficients
print (f'popt:')
print (f'{popt}')

# covariance matrix
print (f'pcov:')
print (f'{pcov}')

# fitted a and b
a_fitted = popt[0]
b_fitted = popt[1]

# degree of freedom
dof = len (data_exptime) - 2
print (f'dof = {dof}')

# residual
residual = data_mean - func (data_exptime, a_fitted, b_fitted)
reduced_chi2 = (residual**2).sum () / dof
print (f'reduced chi^2 = {reduced_chi2}')

# errors of a and b
a_err = numpy.sqrt (pcov[0][0])
b_err = numpy.sqrt (pcov[1][1])
print (f'a = {a_fitted:g} +/- {a_err:g} ({a_err / a_fitted * 100.0:g} %)')
print (f'b = {b_fitted:g} +/- {b_err:g} ({b_err / b_fitted * 100.0:g} %)')

# fitted line
fitted_x = numpy.linspace (0.0, 3600.0, 10**6)
fitted_y = a_fitted * fitted_x + b_fitted

#
# plotting using Matplotlib
#

# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# axes
ax.set_title ('Dark Current Generation Rate')
ax.set_xlabel ('Exposure Time [sec]')
ax.set_ylabel ('Mean Pixel Value [ADU]')

# plotting a figure
ax.errorbar (data_exptime, data_mean, yerr=data_stddev, \
             fmt='bo', ecolor='black', capsize=5, label='Dark Current')
ax.plot (fitted_x, fitted_y, 'r--', label='Least-squares fitting by SciPy')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=resolution)
