#!/usr/bin/python

import subprocess
import os

directory = 'S1ULp'
input_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-8-09.03.2021-exc_inh/' + directory + '/results'
output_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-8-09.03.2021-exc_inh/' + directory

for directory in os.listdir(input_directory):
    command = 'cp %s/%s/composite/*.png %s/%s.png' % (input_directory, directory,
                                                      output_directory, directory)
    print(command)
    subprocess.call(command, shell=True)
