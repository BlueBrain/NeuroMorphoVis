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

    help = 'number of samples per exemplar, if [n] then get all the neurons'
    parser.add_argument('--number-samples',
        action='store', default='1', dest='number_samples', help=help)

    help = 'output path'
    parser.add_argument('--output',
        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @get_morphology_exemplars
################################################################################
def create_targets(blue_config, output,
                   target='mc2_Column',
                   nsamples=1):
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

    # create a list of selected exemplars
    exemplars_list = []

    mtypes = ['L1_DAC',     ### layer 1
              'L1_NGC-DA',
              'L1_NGC-SA',
              'L1_HAC',
              'L1_DLAC',
              'L1_SLAC',
              'L23_PC',     ### layer 2/3
              'L23_MC',
              'L23_BTC',
              'L23_DBC',
              'L23_BP',
              'L23_NGC',
              'L23_LBC',
              'L23_NBC',
              'L23_SBC',
              'L23_ChC',
              'L4_PC',      ### layer 4
              'L4_SP',
              'L4_SS',
              'L4_MC',
              'L4_BTC',
              'L4_DBC',
              'L4_BP',
              'L4_NGC',
              'L4_LBC',
              'L4_NBC',
              'L4_SBC',
              'L4_ChC',
              'L5_TTPC1',   ### layer 5
              'L5_TTPC2',
              'L5_UTPC',
              'L5_STPC',
              'L5_MC',
              'L5_BTC',
              'L5_DBC',
              'L5_BP',
              'L5_NGC',
              'L5_LBC',
              'L5_NBC',
              'L5_SBC',
              'L5_ChC',
              'L6_TPC_L1',  ### layer 6
              'L6_TPC_L4',
              'L6_UTPC',
              'L6_IPC',
              'L6_BPC',
              'L6_MC',
              'L6_BTC',
              'L6_DBC',
              'L6_BP',
              'L6_NGC',
              'L6_LBC',
              'L6_NBC',
              'L6_SBC',
              'L6_ChC']

    ntags = len(mtypes)
    for ntag, mtype in enumerate(mtypes):

        # all the cells with that specific mtype
        mtype_cells = []

        # get all the cells with that specific mtype
        for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

            # fetch neuron data
            morphology_type = neuron.morphology_type().name()

            if morphology_type == mtype:

                # position
                position = neuron.position()

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
                               str(ntag + 1),
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
                mtype_cells.append(neuron_data)

        # select a random cell and add it to the exemplars list
        if nsamples < len(mtype_cells):
            sampled_exemplars = random.sample(mtype_cells, nsamples)
            exemplars_list.append(sampled_exemplars)
        else:
            exemplars_list.append(mtype_cells)

    # create the output directory
    output = '%s/%s' % (output, nsamples)
    writer.clean_and_create_directory(output)
    for i, mtype in enumerate(mtypes):
        voxelization_target_output = \
            open("%s/%s_%s.list" % (output, mtype, str(nsamples)), 'w')
        default_target_output = open("%s/%s_%s.target" %
                                     (output, mtype, str(nsamples)), 'w')
        default_target_output.write(
            "Target Cell Exemplars_%s_%s \n" % (mtype, str(nsamples)))
        default_target_output.write("{\n")
        gids_string = ''
        for item in exemplars_list:
            for data in item:
                if mtype == data.split(' ')[8]:
                    gids_string += "a%d " % int(data.split(' ')[0])
                    voxelization_target_output.write("%s\n" % data)
        default_target_output.write(gids_string)
        default_target_output.write("\n}\n")
        voxelization_target_output.close()
        default_target_output.close()
    voxelization_target_output = open("%s/Exemplars_%s.list" %
                                      (output, str(nsamples)), 'w')
    default_target_output = open(
        "%s/Exemplars_%s.target" % (output, str(nsamples)), 'w')
    default_target_output.write(
        "Target Cell Exemplars_%s \n" % str(nsamples))
    default_target_output.write("{\n")
    gids_string = ''
    for item in exemplars_list:
        for data in item:
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

    nsamples = 0
    if argument_list.number_samples == 'n':
        nsamples = 100000000000
    else:
        nsamples = int(argument_list.number_samples)
    # create targets
    create_targets(argument_list.circuit_config, argument_list.output,
        nsamples=nsamples)


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()