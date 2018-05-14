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

    # use the blue config to open a bbp experiment.
    experiment = bbp.Experiment()
    experiment.open(blue_config)

    # define a micro-circuit.
    micro_circuit = experiment.microcircuit()

    # define a cell target from the given target in the original blue-config.
    # file.
    # this target will be used for the final filtration stage to pick the new
    # targets within the bounding box given by the center and xyz dimensions.
    print("adding the cell target %s" % target)
    cell_target = experiment.cell_target(target)

    # loading flags.
    load_flags = bbp.Loading_Flags
    micro_circuit.load(cell_target,load_flags.NEURONS)

    # getting the neurons
    neurons = micro_circuit.neurons()
    
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
    
    import brain
    import numpy

    # write the data to an output file list 
    output_file = open('%s.list' %(target), 'w')
    
    for i_layer in range(1, 7):        
        layer_list = []
        if(i_layer == 1): layer_list = layer_1
        elif(i_layer == 2) : layer_list = layer_2
        elif(i_layer == 3) : layer_list = layer_3
        elif(i_layer == 4) : layer_list = layer_4
        elif(i_layer == 5) : layer_list = layer_5
        elif(i_layer == 6) : layer_list = layer_6
    
        # load the circuit and the selected targets 
        circuit = brain.Circuit(blue_config)
        gids = circuit.gids('a1')
        gids = numpy.delete(gids, 0)
        
        for i_gid in layer_list:
            gids = numpy.append(gids, i_gid)
        print("layer %d contains %d gids" % (i_layer, len(gids)))
        
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
            soma_radii[i_gid], i_layer)
            output_file.write(line)
    output_file.close()
    
    # compute the bounding-box of the target
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
    output_file = open('%s.bounds' % (target), 'w')
    bounds = '%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f' % \
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
                         argument_list.target)

if __name__ == "__main__":
    run_application()


