# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:07:54 2019

@author: gabriel
"""
import noise_to_current as ntc
import numpy as np

# Setup Configuration:
filename = "T-40V-550_0"     # File name
curr_setup = 101 * 1e-6       # Total current of setup for this temperature while taking noise data
curr_err_percentage = 0.1   # Current error is a % of the current
T = 40                       # Temperature of setup

grp_pxl = 16                 # Groups of pixel (1 pixel = 16x16 original pixels)

noise, mask = ntc.loadNoise("./" + filename)
noise, mask = ntc.average_quantity(noise, mask, grp_pxl)

curr = ntc.noiseToCurrent(noise, grp_pxl, curr_setup)
np_curr = np.array(curr)


# Error estimation based on the fit of Kazu's paper data (fluence x current)
def error_estimation(const, slope, const_err, slope_err, current, percent_current_err, mode):
    current_err = 0.000002 ** 2
    current /= 0.000001
    const_contribution_error = 0
    slope_contribution_error = 0
    current_contribution_error = (current * percent_current_err) ** 2  # Current error contribution from data taking
    # 110V, 140V and 250V Fits are exponential; 550V Fit is linear
    if mode == "exp":
        const_contribution_error = (np.exp(slope * current + const) * const_err) ** 2
        slope_contribution_error = (current * np.exp(slope * current + const) * slope_err) ** 2
        current_contribution_error += (slope * np.exp(slope * current + const) * current_err) ** 2
    elif mode == "linear":
        const_contribution_error = const_err ** 2
        slope_contribution_error = slope_err ** 2
        current_contribution_error += (slope*current_err) ** 2
    return np.sqrt(const_contribution_error + slope_contribution_error + current_contribution_error)


def fluence_110v(current):
    const = -0.8234
    slope = 0.3743
    const_err = 0.1062
    slope_err = 0.01742
    return (np.exp(slope * current / 0.000001 + const)), error_estimation(const, slope, const_err, slope_err, current,
                                                                          curr_err_percentage, "exp")


def fluence_140v(current):
    const = -0.7703
    slope = 0.3352
    const_err = 0.09666
    slope_err = 0.01454
    return np.exp(slope * current / 0.000001 + const), error_estimation(const, slope, const_err, slope_err, current,
                                                                        curr_err_percentage, "exp")


def fluence_250v(current):
    const = -0.511
    slope = 0.2393
    const_err = 0.06646
    slope_err = 0.007802
    return np.exp(slope * current / 0.000001 + const), error_estimation(const, slope, const_err, slope_err, current,
                                                                        curr_err_percentage, "exp")


def fluence_550v(current):
    const = -0.1712
    slope = 0.4353
    const_err = 0.0856
    slope_err = 0.00665
    return (slope * current / 0.000001 + const), error_estimation(const, slope, const_err, slope_err, current,
                                                                  curr_err_percentage, "linear")


# print(np.shape(np_curr))
curr_parts = []
curr_parts38 = []
fluence_parts = []
fluence_err_parts = []

curr_parts.append(np.sum(np_curr[0:13][0:8]))
curr_parts.append(np.sum(np_curr[0:13][8:16]))
curr_parts.append(np.sum(np_curr[13:25][0:8]))
curr_parts.append(np.sum(np_curr[13:25][8:16]))
curr_parts.append(np.sum(np_curr[25:37][0:8]))
curr_parts.append(np.sum(np_curr[25:37][8:16]))
curr_parts.append(np.sum(np_curr[37:][0:8]))
curr_parts.append(np.sum(np_curr[37:][8:16]))

print("########## Currents at {} ##########".format(T))
for i in range(8):
    print("I{} =".format(i + 1), curr_parts[i])

print("")

print("########## Currents at -38 ##########")
for i in range(8):
    curr_parts38.append(ntc.currForAnotherTemp((curr_parts[i]), 273 - T, 273 - 38))
    print("I{} =".format(i + 1), curr_parts38[i])

print("")

print("########## Fluences ##########")
for i in range(8):
    _fluence, _fluence_err = fluence_550v(curr_parts38[i])
    fluence_parts.append(_fluence)
    fluence_err_parts.append(_fluence_err)
    print("\u03A6{} = {} +/- {}".format((i + 1), fluence_parts[i], fluence_err_parts[i]))

with open(filename + ".dat", "w", encoding="utf-8") as f:
    f.write("{:#^30} {:#^44}\n".format("Currents(\u03BCA)", "Fluences(*10^15 MeV/cm^2)"))
    for i in range(8):
        f.write("I{:<2} = {:<20}  \u03A6{} = {:<20} +/- {:20}\n".format((i + 1), curr_parts[i] * 1000000, (i + 1),
                                                                        fluence_parts[i], fluence_err_parts[i]))
