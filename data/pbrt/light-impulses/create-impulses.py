#!/usr/bin/python

import sys
import os
import shutil

if len(sys.argv) < 2:
    print("enter the impulse wavelength please")
    exit(0)

print("creating a series of photon impulses")
pulse_value = sys.argv[1]

# create a directory with the pulse_value
if not os.path.exists(pulse_value):
    os.makedirs(pulse_value)
else:
    shutil.rmtree(pulse_value)
    os.makedirs(pulse_value)

for i_file in range (300, 800 + 1):
    spd_file = open(pulse_value + "/impulse-" + str(i_file) + ".spd", 'w')
    for i_lambda in range(300, 800 + 1):
        if (i_lambda == i_file):
            spd_file.write(str(i_lambda) + " " + pulse_value + "\n")
        else:
            spd_file.write(str(i_lambda) + " 0 \n")
    spd_file.close()
print("done")
