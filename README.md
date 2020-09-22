# SD_GW_tool
A simple tool for getting accurate window functions to calculate SD signals from GW.


Parameters can be specified at the top of the main python file: SD_window_tool.py

These parameters are hopefully intuitive, but for clarity we state them here:

zmax_in:
This is the upper redshift for the window function integral. This should match the time of GW injection. If it is primordial, set 1e9 (This is already ~10^2 higher than realistically necessary)

kmin_in & kmax_in:
These are the lower and upper limits for k respectively. The default values are 1e-4 < k < 1e9 (Mpc^-1). Interpolation beyond these values may not be sensible. For frequencies use k/Mpc^−1 = 6.5×10^14 f/Hz
              
k_points_in:
The number of points you want to sample in k.

filename_out:
The file name for writing out the window function. You must specify a file type as well, usually .dat

show_plot:
A boolean to specify if you want to see a log-log plot of the window function. This uses an extremely simple matplotlib.pyplot figure

nu_damping:
A boolean to specify if you want to include damping or not. Results will be ~30% lower across the whole window if set to True
