from scipy import signal, interpolate as ip
import numpy as np

def interpolate_missing_values(data):
    nan_indices = data.isnull()
    known_indices = data.index[~nan_indices]
    known_values = data[~nan_indices]

    interp_func = ip.CubicSpline(known_indices, known_values, bc_type='natural')

    nan_indices = data.index[nan_indices]
    data.loc[nan_indices] = interp_func(nan_indices)
    return data