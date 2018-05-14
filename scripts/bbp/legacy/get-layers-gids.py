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

    parser.add_argument('--percent',
                        action='store', default='100',
                        dest='percent',
                        help='percent of the cells')

    # parse the arguments, and return a list of them.
    return parser.parse_args()

###############################################################################
# @pselect_neurons
###############################################################################
def select_neurons(blue_config, target, percent=100.0):

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

    # loading flags.
    load_flags = bbp.Loading_Flags

    print("loading the microcircuit")
    micro_circuit.load(cell_target,load_flags.NEURONS)
    print("microcircuit is loaded successfully with NEURONS")

    # getting the neurons
    neurons = micro_circuit.neurons()
    print("the neurons were loaded in the list successfully")
    
    layer_1 = []
    layer_2 = []
    layer_3 = []
    layer_4 = []
    layer_5 = []
    layer_6 = []
    for i_neuron in neurons:
        neuron_gid = i_neuron.gid()
        neuron_layer = i_neuron.layer()
        if(neuron_layer == 1):
            layer_1.append(neuron_gid)
        elif(neuron_layer == 2):
            layer_2.append(neuron_gid)
        elif(neuron_layer == 3):
            layer_3.append(neuron_gid)
        elif(neuron_layer == 4):
            layer_4.append(neuron_gid)
        elif(neuron_layer == 5):
            layer_5.append(neuron_gid)
        elif(neuron_layer == 6):
            layer_6.append(neuron_gid)
    
    for i in range(1, 7):
        list_output = open("layer-%d-%s.list" % (i, target), 'w')
        target_output = open("layer-%d-%s.target" % (i, target), 'w')
        
        layer_list = []
        if(i == 1): layer_list = layer_1
        elif(i == 2) : layer_list = layer_2
        elif(i == 3) : layer_list = layer_3
        elif(i == 4) : layer_list = layer_4
        elif(i == 5) : layer_list = layer_5
        elif(i == 6) : layer_list = layer_6
        
        target_output.write("Target Cell Layer%d_%s \n" % (i, target))
        target_output.write("{\n")
        gids_string = ''
        for i_gid in layer_list:
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

    select_neurons(argument_list.circuit_config,
                   argument_list.target,
                   float(argument_list.percent))

if __name__ == "__main__":

    run_application()


