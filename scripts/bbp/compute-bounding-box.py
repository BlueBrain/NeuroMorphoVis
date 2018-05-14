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

###############################################################################
# @compute_bounding_box
###############################################################################
def compute_bounding_box(blue_config, target):

    # load the circuit and the selected targets 
    circuit = brain.Circuit(blue_config)
    gids = circuit.gids(target)
    
    print('%d gids are loaded' % (len(gids)))
    
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
    
    print('%.2f %.2f %.2f' % (dim_x, dim_y, dim_z))
    center_x = pmin_x + (0.5 * dim_x)
    center_y = pmin_y + (0.5 * dim_y)
    center_z = pmin_z + (0.5 * dim_z)
    
    # write the data to an output file list 
    output_file = open('%s.bounds' % target, 'w')
    bounds = '%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f' % \
        (pmin_x, pmin_y, pmin_z, pmax_x, pmax_y, pmax_z, center_x, center_y, center_z)
    output_file.write(bounds)
    output_file.close()
    
    for i in 10, 25, 50, 75, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000:
        size = i
        output_file = open('%s_%.1f.bounds' % (target, size), 'w')
        min_x = center_x - (size / 2.0)
        min_y = center_y - (size / 2.0)
        min_z = center_z - (size / 2.0)
        max_x = center_x + (size / 2.0)
        max_y = center_y + (size / 2.0)
        max_z = center_z + (size / 2.0)
        
        # compute how many neurons are in there 
        neuron_count = 0
        for position in positions: 
            if(position[0] > min_x and position[1] > min_y and position[2] > min_z and position[0] < max_x and position[1] < max_y and position[2] < max_z):
                neuron_count += 1
        print('%d: %d' %(i, neuron_count))
        
        dx = max_x - min_x 
        dy = max_y - min_y 
        dz = max_z - min_z 
        bounds = '%.2f %.2f %.2f %.2f %.2f %.2f' % (min_x, min_y, min_z, max_x, max_y, max_z)
        print(bounds + '\t: %.2f %.2f %.2f' % (dx, dy, dz))
        output_file.write(bounds)
        output_file.close()
###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # go for it 
    compute_bounding_box(argument_list.circuit_config, argument_list.target)

if __name__ == "__main__":
    run_application()


