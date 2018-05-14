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

    parser.add_argument('--list',
                        action='store',
                        dest='gid_list',
                        help='input list of gids')

    parser.add_argument('--output',
                        action='store', default='list',
                        dest='output',
                        help='output file name')

    parser.add_argument('--n-tags',
                        action='store', default=1,
                        dest='number_tags',
                        help='number sampled lists')
    
    parser.add_argument('--percent',
                        action='store', default=100.0,
                        dest='percent',
                        help='percentage of the target')
                        
    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @sample_target
###############################################################################
def sample_target(blue_config, gid_list, number_tags=1, percent=100.0,
                  output="list"):
    # load the list file and sample it 
    list_file = open(gid_list, 'r')
    target_gids = []
    for i_line in list_file:
        target_gids.append(int(i_line))
    list_file.close()

    # a list containing all the target gids after sampling 
    list_gids = random.sample(set(target_gids),
                              int((len(target_gids) * percent / 100.0)))
                              
    # load the circuit and the selected targets 
    circuit = brain.Circuit(blue_config)

    # final lists 
    lists = []

    # sample the list randomly to _number_tags_ lists 
    remaining_cells = len(list_gids)
    cell_count = int(len(list_gids) / number_tags)
    for i_list in range(0, number_tags):
        # handle the last case
        if(i_list == number_tags - 1):
            cell_count = remaining_cells
        cell_list = []
        for i_cell in range(0, cell_count):
            cell = random.choice(list_gids)
            list_gids.remove(cell)
            cell_list.append(cell)
        lists.append(cell_list)
        remaining_cells = remaining_cells - cell_count

    # write the data to an output file list 
    output_file = open("%s.list" % output, 'w')
     
    # print the lists and save them to a file 
    for i_list in range(0, len(lists)):
        # loads an empty target until further notice
        gids = circuit.gids('a1')
        gids = numpy.delete(gids, 0)

        for i_gid in lists[i_list]:
            gids = numpy.append(gids, i_gid)

        # obtain the position of the targets   
        positions = circuit.positions(gids)

        # obtain the soma radii and soma centers from the morphologies 
        soma_radii = []
        morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)
        uris = circuit.morphology_uris(gids)
        for i_gid in range(0, len(gids)):
            morphology = brain.neuron.Morphology(uris[i_gid])
            soma_radii.append(morphology.soma().mean_radius())

        for i_gid in range(0, len(gids)):
            line = "%d %.2f %.2f %.2f %.3f %d\n" % (gids[i_gid],
             positions[i_gid][0], positions[i_gid][1], positions[i_gid][2],
             soma_radii[i_gid], i_list + 1)
            output_file.write(line)
            
    output_file.close()
    exit(0)

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


