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
    
    parser.add_argument('--gid',
                        action='store',
                        dest='gid',
                        help='target gid')
                        
    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @compute_bounding_box
###############################################################################
def compute_bounding_box(blue_config, gid):

    # load the circuit and the selected targets 
    circuit = brain.Circuit(blue_config)
    gids = circuit.gids("a" + gid)
    
    morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)
    uris = circuit.morphology_uris(gids)
    morphology = brain.neuron.Morphology(uris[0])
    radius = morphology.soma().mean_radius()
    print(radius)
    
    axon = morphology.sections({brain.neuron.SectionType.axon})
    print(len(axon))
    dendrites = morphology.sections({brain.neuron.SectionType.dendrite})
    print(len(dendrites))
    print('%d gids are loaded' % (len(gids)))

    """
    # write the data to an output file list 
    output_file = open("all-gids.list", 'w')
    output_file.write("Target Cell Slice-7x1 \n")
    output_file.write("{\n")
    gids_string = '' 
    for i_gid in gids:
        gids_string += "a%d " % (i_gid) 
    output_file.write(gids_string)
    output_file.write("\n}\n")
    output_file.close()
    """

###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # go for it 
    compute_bounding_box(argument_list.circuit_config,
                         argument_list.gid)

if __name__ == "__main__":
    run_application()


