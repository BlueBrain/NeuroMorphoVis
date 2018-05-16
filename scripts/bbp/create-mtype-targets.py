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


# Imports
import argparse
import random
import core.utilities
import core.consts


################################################################################
# @parse_command_line_arguments
################################################################################
def parse_command_line_arguments():
    """Parses the input arguments to the script.

    :return:
        Argument list.
    """

    # Add all the options.
    parser = argparse.ArgumentParser()
    help = 'circuit config file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=help)

    help = 'cell target, default [mc2_Column]'
    parser.add_argument('--target',
                        action='store', default='mc2_Column', dest='target', help=help)

    help = 'percentage of the target, default 100'
    parser.add_argument('--percent',
                        action='store', default=100.0, dest='percent', help=help)

    help = 'output path'
    parser.add_argument('--output',
                        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @get_morphology_exemplars
################################################################################
def create_targets(circuit_config,
                   output,
                   target='mc2_Column',
                   percent=100.0):
    """Returns a list of exemplars where each one represent a category of the different
    morphologies.

    If the random selection flag is set, then they will be picked up randomly, otherwise, the first
    one of each selected type will be picked.

    :param circuit_config:
        Circuit configuration.
    :param target:
        Input target.
    :param percent:
        Percentage.
    :param output:
        Output path.
    :param number_tags:
        The number of tags.
    :return:
        A Neuron list of all the cells created for the specified target.
    """

    try:
        import bbp
    except ImportError:
        print('ERROR: Cannot import bbp')
        exit(0)

    try:
        import brain
    except ImportError:
        print('ERROR: Cannot import brain')
        exit(0)

    # Use the BBP circuit configuration to open a bbp experiment
    experiment = bbp.Experiment()
    experiment.open(circuit_config)

    # Circuit
    micro_circuit = experiment.microcircuit()

    # Cell target
    cell_target = experiment.cell_target(target)

    # Load neurons only, since it will take forever to load the morphologies
    print('* Loading the circuit from the BBPSDK')
    load_flags = bbp.Loading_Flags
    micro_circuit.load(cell_target, load_flags.NEURONS)

    # Get the BBP data
    neurons = micro_circuit.neurons()

    # Load the circuit from Brain
    print('* Loading the circuit from Brain')
    circuit = brain.Circuit(circuit_config)

    # Get all the gids of the target
    gids = circuit.gids(target)

    # Load the morphologies with brain (faster than BBPSDK)
    circuit.load_morphologies(gids, circuit.Coordinates.local)
    uris = circuit.morphology_uris(gids)[0]
    brain.neuron.Morphology(uris)
    morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)

    # Creating the output directory
    core.writer.create_directory(output)

    # Create a list of selected exemplars
    exemplars_list = []

    for ntag, mtype in enumerate(core.consts.MTYPES):

        # all the cells with that specific mtype
        mtype_cells = []

        # get all the cells with that specific mtype
        for i_neuron, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

            # fetch neuron data
            morphology_type = neuron.morphology_type().name()

            if morphology_type == mtype:

                # Position
                position = str(neuron.position()).replace('[ ', '').replace(' ]', '')

                # Neuron orientation
                orientation = str(neuron.orientation())
                orientation = orientation .replace('[ ', '').replace(' ]', '').replace('0 1 0 ', '')

                # Transformation
                transform = circuit.transforms({int(gid)})[0]
                transform_string = ''
                for i in [0, 1, 2, 3]:
                    for j in [0, 1, 2, 3]:
                        value = str(transform[i][j])
                        value = float(value.replace('[', '').replace(']', ''))
                        transform_string += str(value) + ' '
                transform = transform_string

                # Layer
                layer = neuron.layer()

                # Tag
                tag = ntag

                # Mean radius of the soma
                soma_mean_radius = morphologies[i_neuron].soma().mean_radius()

                # Minimum and maximum radii of the soma
                soma_min_radius, soma_max_radius = core.utilities.get_minimum_and_maximum_radii(
                    morphologies[i_neuron].soma().profile_points())

                # Morphology label
                morphology_label = neuron.morphology_label()

                # Column
                column = neuron.column()

                # Construct the neuron structure
                neuron = core.Neuron(
                    gid=gid,
                    morphology_type=morphology_type,
                    morphology_label=morphology_label,
                    position=position,
                    orientation=orientation,
                    transform=transform,
                    layer=layer,
                    column=column,
                    tag=tag,
                    soma_min_radius=soma_min_radius,
                    soma_mean_radius=soma_mean_radius,
                    soma_max_radius=soma_max_radius)

                # add the neuron data to the list
                mtype_cells.append(neuron)

        # Random sampling
        sampled_mtypes = random.sample(set(mtype_cells), int((len(mtype_cells) * percent / 100.0)))

        # Construct the target name
        target_name = '%s_%s_%fp_random' % (target, mtype, float(percent))

        # Write the NeuroRender configuration file
        print('* Writing rendering config')
        core.write_neurorender_config(
            sampled_mtypes, config_file_name=target_name, output_path=output)

        # Write the target file
        print('* Writing target file')
        core.write_target_file(
            sampled_mtypes, target_name=target_name,
            target_file_name=target_name, output_path=output)

        # Extend the exemplars list
        exemplars_list.extend(sampled_mtypes)

    # Construct the target name
    target_name = '%s_mtypes_%fp_random' % (target, float(percent))

    # Write the NeuroRender configuration file
    print('* Writing rendering config')
    core.write_neurorender_config(
        exemplars_list, config_file_name=target_name, output_path=output)

    # Write the target file
    print('* Writing target file')
    core.write_target_file(
        exemplars_list, target_name=target_name,
        target_file_name=target_name, output_path=output)


################################################################################
# @run
################################################################################
def run():
    """Runs the script.
    """

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # create targets
    create_targets(
        argument_list.circuit_config,
        argument_list.output,
        target=argument_list.target,
        percent=float(argument_list.percent))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()