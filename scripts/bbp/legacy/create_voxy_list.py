"""
@author  Marwan Abdellah <marwan.abdellah@epfl.ch>
@remarks Copyright (c) BBP/EPFL 2017 All rights reserved.
         Do not distribute without further notice.
"""

# system imports
import os
import sys
import subprocess
import argparse
import random

# bbp
import bbp
import brain

largest_number = 1000000000000000000000.0
smallest_number = -1000000000000000000000.0


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

    parser.add_argument('--target',
        action='store', default='mc2_Column',
        dest='target',
        help='cell target, default mc2_Column')

    # parse the arguments, and return a list of them.
    return parser.parse_args()

def create_list(circuit_config, number_tags):
    return


###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # go for it
    sample_target(argument_list.circuit_config,
                  argument_list.gid_list,
                  int(argument_list.number_tags),
                  float(argument_list.percent),
                  argument_list.output)

if __name__ == "__main__":
    run_application()