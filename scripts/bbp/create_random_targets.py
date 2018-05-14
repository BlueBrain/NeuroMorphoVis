"""
@ create_layer_targets.py:
    Creates targets based on layer
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

    help = 'number of tags'
    parser.add_argument('--ntags',
        action='store', default=2, dest='number_tags', help=help)

    help = 'output path'
    parser.add_argument('--output',
        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @create_targets
################################################################################
def create_targets(circuit_config, target, percent, output, ntags):
    """
    Creates the targets.

    :param circuit_config: Circuit configuration.
    :param target: Input target.
    :param percent: Percentage.
    :param output: Output path.
    :return:
    """

    # use the blue config to open a bbp experiment.
    experiment = bbp.Experiment()
    experiment.open(circuit_config)

    # circuit
    micro_circuit = experiment.microcircuit()

    # cell target
    cell_target = experiment.cell_target(target)

    # load neurons only, since it will take forever to load the morphologies.
    print('Loading the circuit from the BBPSDK')
    load_flags = bbp.Loading_Flags
    micro_circuit.load(cell_target, load_flags.NEURONS)

    # get the bbpsdk data
    neurons = micro_circuit.neurons()

    print('Loading the circuit from Brain')
    circuit = brain.Circuit(circuit_config)

    # get all the gids of the target
    gids = circuit.gids(target)

    # load the morphologies with brain (faster than BBPSDK)
    circuit.load_morphologies(gids, circuit.Coordinates.local)
    uris = circuit.morphology_uris(gids)[0]
    brain.neuron.Morphology(uris)
    morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)

    # filtering
    target_data = []
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

        # position
        position = neuron.position()

        # layer
        layer = neuron.layer()

        # mean radius
        mean_radius = morphologies[i].soma().mean_radius()

        # min and max radii
        min_radius, max_radius = morphology_utils.get_minimum_and_maximum_radii(
            morphologies[i].soma().profile_points())

        # morphology type
        morphology_type = neuron.morphology_type().name()

        # morphology label
        morphology_label = neuron.morphology_label()

        # column
        column = neuron.column()

        # compose the neuron data
        neuron_data = '%s %s %s %s %s %s %s %s %s %s %s %s' % \
                      (str(gid),
                       str(random.randint(1, ntags)),
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

        # add the neuron data to the list
        target_data.append(neuron_data)

    # write all layers data
    all_layers_data = random.sample(set(target_data),
        int((len(target_data) * percent / 100.0)))

    for i in range(1, ntags + 1):
        voxelization_target_output = \
            open("%s/Tag%d_%s-%dp.list" %
                 (output, i, target,int(percent)), 'w')
        default_target_output = open("%s/Tag%d_%s-%dp.target" %
                                     (output, i, target, int(percent)), 'w')
        default_target_output.write(
            "Target Cell Layer%d_%s-%dp \n" % (i, target, int(percent)))
        default_target_output.write("{\n")
        gids_string = ''
        for data in all_layers_data:
            if i == data.split(' ')[1]:
                gids_string += "a%d " % int(data.split(' ')[0])
                voxelization_target_output.write("%s\n" % data)
        default_target_output.write(gids_string)
        default_target_output.write("\n}\n")
        voxelization_target_output.close()
        default_target_output.close()
    voxelization_target_output = open("%s/Random_%s-%dp.list" %
                                      (output, target, int(percent)), 'w')

    default_target_output = open(
        "%s/Random_%s-%dp.target" % (output, target, int(percent)), 'w')
    default_target_output.write(
        "Target Cell Random_%s-%dp \n" % (target, int(percent)))
    default_target_output.write("{\n")
    gids_string = ''
    for data in all_layers_data:
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
    create_targets(argument_list.circuit_config,
        argument_list.target, float(argument_list.percent),
        argument_list.output, int(argument_list.number_tags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()