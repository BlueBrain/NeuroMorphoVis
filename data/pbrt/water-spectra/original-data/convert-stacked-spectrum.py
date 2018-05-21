#!/usr/bin/python

import os
import random
import sys
from scipy.interpolate import interp1d

input_file = sys.argv[1]
print "selected file %s \n" % input_file


with open(input_file, 'rb') as data_file:
    lines = data_file.readlines()

    wl_data = []
    ua_data = []
    us_data = []

    # number of arguments
    number_arguments = 9
    # number of samples in the file
    number_samples = int(len(lines) * 1.0 / float(number_arguments))

    for i in range(0, number_samples):
        wl = lines[(i * number_arguments) + 0].strip("\n")
        ua = lines[(i * number_arguments) + 4].strip("\n")
        us = lines[(i * number_arguments) + 5].strip("\n")

        wl_data.append(float(wl))
        ua_data.append(float(ua))
        us_data.append(float(us))
        print "lambda = %s : ua = %s, us = %s " % (wl, ua, us)

    # interpolate
    interpolated_ua = interp1d(wl_data, ua_data)
    interpolated_us = interp1d(wl_data, us_data)

    # write the data to files
    ua_spd_file = open("water-absorption.spd", 'w')
    for i in range(300, 800):
        if i < 400:
            ua_spd_file.write("%d %f\n" % (i, interpolated_ua(400)))
        else:
            ua_spd_file.write("%d %f\n" % (i, interpolated_ua(i)))
    ua_spd_file.close()

    us_spd_file = open("water-scattering.spd", 'w')
    for i in range(300, 800):
        if i < 400:
            us_spd_file.write("%d %f\n" % (i, interpolated_us(400)))
        else:
            us_spd_file.write("%d %f\n" % (i, interpolated_us(i)))
    us_spd_file.close()

print("done, and the spd files have been created")
