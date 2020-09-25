# GW2SD
A simple tool for getting accurate window functions and calculate SD signals from GW.

The code can write window functions to a file, with specified z_max and k range (in Mpc^-1).
It can show a simple plot of the window function.
It can calculate a mu signal by either specifying the function user_PT_function(k) or by reading a data file and interpolating (filename_in).


Parameters can be specified at the top of the main python file: SD_window_tool.py.
These parameters are hopefully intuitive, but for clarity we state them here.

zmax_in:
This is the upper redshift for the window function integral. This should match the time of GW injection. If it is primordial, set 1e9 (This is already ~10^2 higher than realistically necessary).

kmin_in & kmax_in:
These are the lower and upper limits for k respectively. The default values are 1e-4 < k < 1e9 (Mpc^-1). Interpolation beyond these values may not be sensible. For frequencies use k/Mpc^−1 = 6.5×10^14 f/Hz.
              
k_points_in:
The number of points you want to sample in k.

nu_damping:
A boolean to specify if you want to include damping or not. Results will be ~30% lower across the whole window if set to True.

write_window:
A boolean to specify if you want to write the window as a data file (using filename_out)

show_plot:
A boolean to specify if you want to see a log-log plot of the window function (using filename_out). This uses an extremely simple matplotlib.pyplot figure.

filename_out:
The file name for writing out the window function. Don't specify file type, as this one name is used for both file and figure.

calc_mu:
A boolean to specify if you want to calculate the mu amplitude in this run of the code.

input_type:
('function' or 'file') This specifies whether the mu will be calculated with a function called user_PT_function, or by interpolating data in a file (using filename_in).

filename_in:
The file name used to calculate mu from a file.
