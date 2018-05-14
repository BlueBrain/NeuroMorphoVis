"""
@author  Marwan Abdellah <marwan.abdellah@epfl.ch>
@remarks Copyright (c) BBP/EPFL 2016 All rights reserved.
         Do not distribute without further notice.
"""

# system imports
import os
import sys
import subprocess
import argparse
import random

# bbp
import brain
import numpy

###############################################################################
# @parse_command_line_arguments
###############################################################################
def parse_command_line_arguments():
    """
    * parses the input arguments to the script.
    """

    # add all the options.
    parser = argparse.ArgumentParser()
    parser.add_argument('--circuit-config',
                        action='store',
                        dest='circuit_config',
                        help='circuit config file')

                        
    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @compute_bounding_box
###############################################################################
def compute_bounding_box(blue_config):

    # load the circuit and the selected targets 
    circuit = brain.Circuit(blue_config)
    gids = circuit.gids()
    
    print('%d gids are loaded' % (len(gids)))

    # write the data to an output file list 
    output_file = open("all-gids.list", 'w')
    for i_gid in gids:
        output_file.write("%s \n" % (str(i_gid)))
    output_file.close()

###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # go for it 
    compute_bounding_box(argument_list.circuit_config)

if __name__ == "__main__":
    run_application()


