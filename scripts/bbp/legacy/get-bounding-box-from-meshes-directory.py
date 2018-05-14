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
import os

# bbp
import brain
import numpy

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
    
    parser.add_argument('--meshes-directory',
                        action='store',
                        dest='meshes_directory',
                        help='directory containing all the meshes')
                        
    parser.add_argument('--output',
                        action='store',
                        dest='output',
                        help='output file containing the bounds')
                        
    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @compute_bounding_box
###############################################################################
def compute_bounding_box(blue_config, meshes_directory, output):

    # load all the gids from the neurons names 
    gid_list = []
    for i_mesh in os.listdir(meshes_directory):
        if i_mesh.endswith(".ply"):
            gid = int(i_mesh.replace('neuron_', '').replace('.ply', ''))
            gid_list.append(gid)
    
    # load the circuit and the selected targets 
    circuit = brain.Circuit(blue_config)
    gids = circuit.gids('a1')
    gids = numpy.delete(gids, 0)
    
    for i_gid in gid_list:
        gids = numpy.append(gids, i_gid)
    
    print('%d gids are obtained' % (len(gids)))
    
    # obtain the position of the targets   
    positions = circuit.positions(gids) 
    
    pmin_x = largest_number
    pmin_y = largest_number
    pmin_z = largest_number
    pmax_x = smallest_number
    pmax_y = smallest_number
    pmax_z = smallest_number
    
    for i_position in positions:
        if(pmin_x > i_position[0]): pmin_x = i_position[0]
        if(pmin_y > i_position[1]): pmin_y = i_position[1]
        if(pmin_z > i_position[2]): pmin_z = i_position[2]
        if(pmax_x < i_position[0]): pmax_x = i_position[0]
        if(pmax_y < i_position[1]): pmax_y = i_position[1]
        if(pmax_z < i_position[2]): pmax_z = i_position[2]
        
    dim_x = pmax_x - pmin_x
    dim_y = pmax_y - pmin_y
    dim_z = pmax_z - pmin_z
    
    # write the data to an output file list 
    output_file = open('meshes.bounds', 'w')
    bounds = '%.2f %.2f %.2f \n%.2f %.2f %.2f \n%.2f %.2f %.2f' % \
        (pmin_x, pmin_y, pmin_z, pmax_x, pmax_y, pmax_z, dim_x, dim_y, dim_z)
    output_file.write(bounds)
    output_file.close()

###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # go for it 
    compute_bounding_box(argument_list.circuit_config, 
                         argument_list.meshes_directory,
                         argument_list.output)

if __name__ == "__main__":
    run_application()


