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
import bbp

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
                        
    parser.add_argument('--bounds-file',
                        action='store',
                        dest='bounds_file',
                        help='bounds file')
    
    parser.add_argument('--percent',
                        action='store', default='100',
                        dest='percent',
                        help='percent of the cells')

    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @select_neurons_in_bounding_box
###############################################################################
def select_neurons_in_bounding_box(blue_config, target, bounds_file, percent):

    # use the blue config to open a bbp experiment.
    print("opening experiment")
    experiment = bbp.Experiment()
    experiment.open(blue_config)
    print("experiment is opened successfully")

    # define a micro-circuit.
    print("microcircuit")
    micro_circuit = experiment.microcircuit()
    print("microcircuit is opened successfully")

    # define a cell target from the given target in the original blue-config.
    # file.
    # this target will be used for the final filtration stage to pick the new
    # targets within the bounding box given by the center and xyz dimensions.
    print("adding the cell target %s" % target)
    cell_target = experiment.cell_target(target)
    
    # get the bounds from the bounds file
    x_min = 0 
    y_min = 0 
    z_min = 0 
    x_max = 0 
    y_max = 0 
    z_max = 0
    
    # asumming pmin and pmax are in one line
    bounds_data = open(bounds_file, 'r')
    for i_line in bounds_data:
        data = i_line.split(' ')
        x_min = float(data[0])
        y_min = float(data[1])
        z_min = float(data[2])
        x_max = float(data[3])
        y_max = float(data[4])
        z_max = float(data[5])
        
    print('loaded bounds [%f, %f, %f] [%f, %f, %f]'% (x_min, y_min, z_min,
                                                      x_max, y_max, z_max))
        
    # loading flags.
    load_flags = bbp.Loading_Flags

    print("loading the microcircuit")
    micro_circuit.load(cell_target,load_flags.NEURONS)
    print("microcircuit is loaded successfully with NEURONS")

    # getting the neurons
    neurons = micro_circuit.neurons()
    print("the neurons were loaded in the list successfully")
    
    gids = []
    for i_neuron in neurons:
        neuron_gid = i_neuron.gid()
        neuron_position = i_neuron.position()
        if(neuron_position.x() > x_min and 
           neuron_position.y() > y_min and
           neuron_position.z() > z_min and
           neuron_position.x() < x_max and 
           neuron_position.y() < y_max and
           neuron_position.z() < z_max):
            gids.append(neuron_gid)
    
    # sample the targets 
    print("sampling targets")
    # a list containing all the target gids after sampling 
    gids = random.sample(set(gids),
                        int((len(gids) * percent / 100.0)))
    print('%d neurons selecetd' % len(gids))
    
    list_output = open("%s-%dp.list" % (target, int(percent)), 'w')
    target_output = open("%s-%dp.target" % (target, int(percent)), 'w')

    target_output.write("Target Cell %s-%dp \n" % (target, int(percent)))
    target_output.write("{\n")
    gids_string = ''
    for i_gid in gids:
        gids_string += "a%d " % i_gid
        list_output.write("%d\n" % i_gid)
    target_output.write(gids_string)
    target_output.write("\n}\n")
    list_output.close()
    target_output.close()

###############################################################################
# @run_application
###############################################################################
def run_application():

    # parse the arguments
    argument_list = parse_command_line_arguments()

    select_neurons_in_bounding_box(argument_list.circuit_config,
        argument_list.target, argument_list.bounds_file, 
        float(argument_list.percent))

if __name__ == "__main__":

    run_application()


