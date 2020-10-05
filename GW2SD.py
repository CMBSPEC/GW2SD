# -*- coding: utf-8 -*-

"""
SD Tensor Window Function Tool

This code will give the SD window function for tensor perturbations injected at
different redshifts zmax. This is outlined in the paper 2010.00040

Author: Tom Kite (thomas.kite@manchester.ac.uk)
"""

# Import statements
import numpy as np
from scipy.interpolate import interp2d, interp1d
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ============== #
# User variables #
# ============== #
zmax_in = 1e8      # Any z>10^8 will give the full (primordial) window function
kmin_in = 1e-4     # Interpolation will work best for 1e-4 < k < 1e9
kmax_in = 1e11
k_points_in = 3000
nu_damping = True

write_window = False
make_plot = False
filename_out = "my_window_function"

calc_mu = True
input_type = 'function'     # 'function' or 'file'
filename_in = 'my_PT_data.dat'


# Change this function for whichever model under consideration
def user_PT_function(k):
    k0 = 0.05
    r = 1e-3
    AT = r*2.1e-9
    nT = -r/8
    return AT*(k/k0)**nT


# The following functions all use global variables.
# This has been chosen to make it easier for the user to change everything
def interpolate_data():
    if (nu_damping):
        k_arr_in = np.load("data/k_arr_data_damp.npy")
        zmax_arr_in = np.load("data/zmax_arr_data_damp.npy")
        w_arr_in = np.load("data/w_arr_data_damp.npy")
    elif (not nu_damping):
        k_arr_in = np.load("data/k_arr_data_free.npy")
        zmax_arr_in = np.load("data/zmax_arr_data_free.npy")
        w_arr_in = np.load("data/w_arr_data_free.npy")
    else:
        print("nu_damp must be True or False")
    return interp2d(zmax_arr_in, k_arr_in, w_arr_in, kind='cubic')


def get_window():
    window_fit = interpolate_data()
    # Get fit with user's parameters
    k_arr_out = np.geomspace(kmin_in, kmax_in, k_points_in)
    if (zmax_in <= 5e4):
        w_arr_out = np.zeros(k_points_in)
    else:
        w_arr_out = window_fit(zmax_in, k_arr_out)[:, 0]

    return k_arr_out, w_arr_out


def get_mu_from_func():
    fit = interpolate_data()
    rval = quad(lambda lnk: fit(zmax_in, np.exp(lnk)) *
                user_PT_function(np.exp(lnk)),
                np.log(1e-4), np.log(1e9),
                epsabs=1.e-30, epsrel=1.e-5,
                limit=300)[0]
    return rval


def get_mu_from_file():
    # Get window fit
    window_fit = interpolate_data()

    # Attempt to read user file. This line may need modification
    # Works for space separated values with order: k PT(K)
    data = np.genfromtxt(filename_in)
    PT = interp1d(data[:, 0], data[:, 1], kind='cubic')

    # Perform integration
    rval = quad(lambda lnk: window_fit(zmax_in, np.exp(lnk))*PT(np.exp(lnk)),
                np.log(1.e-4), np.log(1e11),
                epsabs=1.e-30, epsrel=1.e-7,
                limit=300)[0]

    return rval


# Start of main body of code
if __name__ == "__main__":

    k_arr, w_arr = get_window()

    # Write output to file
    if (write_window):
        ofile = open(filename_out + ".dat", 'w')
        ofile.write('#k W_mu\n')
        for i in range(k_points_in):
            ofile.write(str(k_arr[i]))
            ofile.write(' ')
            ofile.write(str(w_arr[i]))
            if (i+1 < k_points_in):
                ofile.write('\n')
        ofile.close()

    # Show plot of window function
    if (make_plot):
        plt.plot(k_arr, w_arr)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('k')
        plt.ylabel('k-space window function')
        plt.savefig(filename_out + ".png", dpi=300)
        plt.close()

    # Find mu amplitude
    if (calc_mu):
        if (input_type == 'function'):
            mu_amplitude = get_mu_from_func()
        elif (input_type == 'file'):
            mu_amplitude = get_mu_from_file()
        else:
            print("input_type must be 'function' or 'file'!")

        print("<mu> = " + str(mu_amplitude))
