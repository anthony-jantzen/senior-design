"""
Location processing module
"""
import itertools
import math
import json
from statistics import median
from scipy.optimize import minimize
import numpy as np

# For measurements in meters and megahertz
# See https://en.wikipedia.org/wiki/Free-space_path_loss#Free-space_path_loss_in_decibels #pylint: disable=line-too-long
FPSL_CONSTANT = 27.55

# The default (for this application) transmitter frequency
DEFAULT_TRANS_FREQ = 2462  # MHz (channel 11)


def fspl(rssi: float, trans_freq: float = DEFAULT_TRANS_FREQ) -> float:
    """
    Calculate free space path loss given the transmitter frequency and
    signal strength

    Based on: http://rvmiller.com/2013/05/part-1-wifi-based-trilateration-on-android/ #pylint disable=line-too-long

    Args:
        rssi: The measured signal strength in dB
        trans_freq: The transmitter frequency (in megahertz) of the device
            which meastured the signal strength. Defaults to
            2462MHz (channel 11)

    Returns:
        Distance in meters from the device which measured the signal strength
    """
    exp = (FPSL_CONSTANT - (20.0 * np.log10(trans_freq)) + abs(rssi)) / 20.0
    return pow(10.0, exp)


def mse(x, locations, distances):
    """
    Mean standard error to minimize
    """
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = np.sqrt(np.power(x[0]-location[0], 2) +
                                      np.power(x[1]-location[1], 2))
        mse += np.power(distance_calculated - distance, 2.0)
    return mse / len(locations)


def trilaterate(knowns, distances):
    """
    Trilaterates a location on a cartesion grid given the location
    of known locations and the desired point's distance from those
    locations

    Based on:
    https://github.com/andykamath/Trifi/blob/master/server/regress.py
    """
    # initial guess to start minmization = average of beacon positions
    initial_location = [np.mean([knowns[0][0], knowns[1][0], knowns[2][0]]),
                        np.mean([knowns[0][1], knowns[1][1], knowns[2][1]])]

    result = minimize(
        mse,                         # The error function
        initial_location,            # The initial guess
        args=(knowns, distances),  # Additional parameters for mse
        method='BFGS',           # The optimisation algorithm
        options={
            'maxiter': 1e1      # Maximum iterations
        })

    return result.x.tolist()


def generate_locations(conf, device_data):
    """
    Generates location data
    """
    def filt(combo):
        times = [x[0] for x in combo]
        mid = median(times)
        for capture in combo:
            if not abs(capture[0] - mid) < 0.25:
                return False

        return True

    apnames = device_data.keys()
    ap_locs = [(ap["x"], ap["y"]) for _, ap in conf["access_points"].items()]

    data = {
        "loc_updates": []
    }

    # Since the devices I'm looking for have to have packets captured
    # by each AP it doesn't matter which AP's devices I iterate through
    rand_ap = list(device_data.keys())[0]
    for device, _ in device_data[rand_ap].items():
        sufficient = True
        captures = []
        for apname in apnames:
            if device not in device_data[apname]:
                sufficient = False
            else:
                captures.append(device_data[apname][device])

        if not sufficient:
            continue

        combos = itertools.product(*captures)
        filtered_combos = list(filter(filt, combos))

        for combo in filtered_combos:
            dists = []
            for cap in combo:
                dists.append(fspl(cap[1], trans_freq=conf["transmitter_freq"]))

            # Note: assumes ap_locs and combo captures are in order
            location = trilaterate(ap_locs, dists)
            timestamp = max([c[0] for c in combo])
            data["loc_updates"].append({
                "timestamp": timestamp,
                "location": location,
                "device": device
            })

    with open("output.json", "w") as outfile:
        json.dump(data, outfile)
