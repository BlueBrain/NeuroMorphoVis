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
    parser.add_argument('--bounds-file',
        action='store', dest='bounds_file', help=help)

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
                   bounds_file,
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
    
    
    # asumming pmin and pmax are in one line
    print('loading bounds data')
    bounds_data = open(bounds_file, 'r')
    for i_line in bounds_data:
        data = i_line.split(' ')
        x_min = float(data[0])
        y_min = float(data[1])
        z_min = float(data[2])
        x_max = float(data[3])
        y_max = float(data[4])
        z_max = float(data[5])
    print('%f %f %f %f %f %f' %(x_min, y_min, z_min, x_max, y_max, z_max))
    
    neurons_list = []

    # get all the cells with that specific mtype
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

        # fetch neuron data
        morphology_type = neuron.morphology_type().name()

        if True: #'L5_TTPC1' in morphology_type or 'L5_TTPC2' in morphology_type:

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
            
            print('.')
            if(position.x() > x_min and position.y() > y_min and position.z() > z_min and position.x() < x_max and position.y() < y_max and position.z() < z_max):
                                
                # add the neuron data to the list
                neurons_list.append(neuron_data)

    sampled_neuron_list = neurons_list #random.sample(set(neurons_list),
        #int((len(neurons_list) * percent / 100.0)))

    # create the output directory
    output = '%s/%s' % (output, str(percent))
    writer.clean_and_create_directory(output)
    voxelization_target_output = open("%s/%s_PCs_%s.list" %
                                      (output, target, str(percent)), 'w')
    default_target_output = open(
        "%s/%s_pcs_%s.target" % (output, target, str(percent)), 'w')
    default_target_output.write(
        "Target Cell pcs_%s \n" % str(percent))
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
        bounds_file=argument_list.bounds_file,
        target=argument_list.target,
        percent=float(argument_list.percent),
        ntags=int(argument_list.ntags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()
