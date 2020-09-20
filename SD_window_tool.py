# -*- coding: utf-8 -*-

"""
SD Tensor Window Function Tool

This code will give the SD window function for tensor perturbations injected at
different redshifts zmax. This is outlined in the paper ***INSERT***

Author: Tom Kite (thomas.kite@manchester.ac.uk)
"""

import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt

# ============== #
# User variables #
# ============== #
zmax_in = 1e6      # Any z>10^8 will give the full (primordial) window function
kmin_in = 1e-4     # Interpolation will work best for 1e-4 < k < 1e9
kmax_in = 1e9
k_points_in = 3000
filename_out = "my_window_function.dat"
show_plot = True
nu_damping = False


if __name__ == "__main__":
    # Load in data
    if (nu_damping):
        k_arr = np.load("data/k_arr_data_damp.npy")
        zmax_arr = np.load("data/zmax_arr_data_damp.npy")
        w_arr = np.load("data/w_arr_data_damp.npy")
    elif (not nu_damping):
        k_arr = np.load("data/k_arr_data_free.npy")
        zmax_arr = np.load("data/zmax_arr_data_free.npy")
        w_arr = np.load("data/w_arr_data_free.npy")
    else:
        exit("nu_damp must be True or False")

    window_fit = interp2d(zmax_arr, k_arr, w_arr, kind='cubic')

    # Get fit with user's parameters
    k_arr_out = np.geomspace(kmin_in, kmax_in, k_points_in)
    if (zmax_in <= 5e4):
        w_arr_out = np.zeros(k_points_in)
    else:
        w_arr_out = window_fit(zmax_in, k_arr_out)[:, 0]

    # Write output to file
    ofile = open(filename_out, 'w')
    ofile.write('#k W_mu\n')
    for i in range(k_points_in):
        ofile.write(str(k_arr_out[i]))
        ofile.write(' ')
        ofile.write(str(w_arr_out[i]))
        if (i+1 < k_points_in):
            ofile.write('\n')
    ofile.close()

    # Show plot of window function
    if (show_plot):
        plt.plot(k_arr_out, w_arr_out)
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
