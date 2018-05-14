"""
@ create_exemplars_targets.py:
    Creates exemplars targets.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# imports
import argparse
import random
import bbp
import brain
import writer
import morphology_utils


################################################################################
# @parse_command_line_arguments
################################################################################
def parse_command_line_arguments():
    """
    Parses the input arguments to the script.
    :return:
    """
    # add all the options.
    parser = argparse.ArgumentParser()
    help = 'circuit config file'
    parser.add_argument('--circuit-config',
        action='store', dest='circuit_config', help=help)

    help = 'cell target, default mc2_Column'
    parser.add_argument('--target',
        action='store', default='mc2_Column', dest='target', help=help)

    help = 'percentage of the target'
    parser.add_argument('--percent',
        action='store', default=100.0, dest='percent', help=help)
    
    help = 'bounds file'
    parser.add_argument('--side',
        action='store', dest='side', help=help)

    help = 'numbert tags' 
    parser.add_argument('--ntags',
        action='store', default=1, dest='ntags', help=help)

    help = 'output path'
    parser.add_argument('--output',
        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @get_morphology_exemplars
################################################################################
def create_targets(blue_config, 
                   output,
                   side,
                   target='mc2_Column',
                   percent=100,
                   ntags=1):
    """
    Returns a list of exemplars where each one represent a category of
    the different morphologies. If the random selection flag is set,
    then they will be picked up randomly, otherwise, the first one of each
    selected type will be picked.

    :param blue_config: Circuit config.
    :param random_selection: Randomly selected cells.
    :return: A list of exemplars to all the mtypes that exist in the circuit.
    """

    print('Loading the circuit from BBPSDK')

    # create an experiment
    experiment = bbp.Experiment()

    # open the blue config
    experiment.open(blue_config)

    # load the entire mc2_Column in the micro-circuit
    micro_circuit = experiment.microcircuit()
    cell_target = experiment.cell_target(target)
    micro_circuit.load(cell_target, bbp.Loading_Flags.NEURONS)

    # retrieve a list of all the neurons in the circuit
    neurons = micro_circuit.neurons()

    print('Loading the circuit from Brain')

    # open a circuit
    circuit = brain.Circuit(blue_config)

    # get all the gids of the target
    gids = circuit.gids(target)

    # load the morphologies with brain (faster than BBPSDK)
    circuit.load_morphologies(gids, circuit.Coordinates.local)
    uris = circuit.morphology_uris(gids)[0]
    brain.neuron.Morphology(uris)
    morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)
    
    # get the dimenions of all the pyramidal cell 
    x_min = 1e32
    y_min = 1e32
    z_min = 1e32
    x_max = -1e32
    y_max = -1e32
    z_max = -1e32
    
    # get all the cells with that specific mtype
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):
        
        # fetch neuron data
        morphology_type = neuron.morphology_type().name()
        
        if 'L5_TTPC1' in morphology_type or 'L5_TTPC2' in morphology_type:
            
            # position
            position = neuron.position()
            
            # update the bounds 
            if position.x() < x_min: x_min = position.x()
            if position.y() < y_min: y_min = position.y()
            if position.z() < z_min: z_min = position.z()
            
            if position.x() > x_max: x_max = position.x()
            if position.y() > y_max: y_max = position.y()
            if position.z() > z_max: z_max = position.z()
    
    # compute the dimensions and the center 
    x_dim = x_max - x_min
    y_dim = y_max - y_min
    z_dim = z_max - z_min
    
    x_center = x_min + (x_dim / 2.0)
    y_center = y_min + (y_dim / 2.0)
    z_center = z_min + (z_dim / 2.0)
    
    x_bound_min = x_center - (side / 2.0)
    y_bound_min = y_center - (side / 2.0)
    z_bound_min = z_center - (side / 2.0)
    x_bound_max = x_center + (side / 2.0)
    y_bound_max = y_center + (side / 2.0)
    z_bound_max = z_center + (side / 2.0)
    
    # get all the neurons that are within bounds 
    neurons_list = []

    # get all the cells with that specific mtype
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

        # fetch neuron data
        morphology_type = neuron.morphology_type().name()

        if 'L5_TTPC1' in morphology_type or 'L5_TTPC2' in morphology_type:

            # position
            position = neuron.position()

            # tag
            tag = random.randint(1, ntags)

            # layer
            layer = neuron.layer()

            # mean radius
            mean_radius = morphologies[i].soma().mean_radius()

            # min and max radii
            min_radius, max_radius = morphology_utils.get_minimum_and_maximum_radii(
                morphologies[i].soma().profile_points())

            # morphology label
            morphology_label = neuron.morphology_label()

            # column
            column = neuron.column()

            # compose the neuron data
            neuron_data = '%s %s %s %s %s %s %s %s %s %s %s %s' % \
                          (str(gid),
                           str(tag),
                           str(position.x()),
                           str(position.y()),
                           str(position.z()),
                           str(min_radius),
                           str(mean_radius),
                           str(max_radius),
                           str(morphology_type),
                           str(morphology_label),
                           str(column),
                           str(layer))
            
            if(position.x() > x_bound_min and 
            position.y() > y_bound_min and 
            position.z() > z_bound_min and 
            position.x() < x_bound_max and 
            position.y() < y_bound_max and 
            position.z() < z_bound_max):
                                
                # add the neuron data to the list
                neurons_list.append(neuron_data)

    sampled_neuron_list = random.sample(set(neurons_list),
        int((len(neurons_list) * percent / 100.0)))

    # create the output directory
    output = '%s/%s_%s' % (output, str(side), str(percent))
    writer.clean_and_create_directory(output)
    voxelization_target_output = open("%s/%s_PCs_%s_%s.list" %
                                      (output, target, str(side), str(percent)), 'w')
    default_target_output = open(
        "%s/%s_pcs_%s_%s.target" % (output, target, str(side), str(percent)), 'w')
    default_target_output.write(
        "Target Cell pcs_%s_%s \n" % (str(side), str(percent)))
    default_target_output.write("{\n")
    gids_string = ''
    for data in sampled_neuron_list:
        gids_string += "a%d " % int(data.split(' ')[0])
        voxelization_target_output.write("%s\n" % data)
    default_target_output.write(gids_string)
    default_target_output.write("\n}\n")
    voxelization_target_output.close()
    default_target_output.close()


################################################################################
# @run
################################################################################
def run():
    """
    Runs the script.
    :return:
    """

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # create targets
    create_targets(argument_list.circuit_config, argument_list.output,
        side=float(argument_list.side),
        target=argument_list.target,
        percent=float(argument_list.percent),
        ntags=int(argument_list.ntags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()
