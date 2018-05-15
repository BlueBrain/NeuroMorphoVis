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
    """Parse the input command line arguments and return a list of them.

    :return:
        A list with all the parsed arguments.
    """

    # Add all the options.
    parser = argparse.ArgumentParser()

    help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=help)

    help = 'Cell target, default [mc2_Column]'
    parser.add_argument('--target',
                        action='store', default='mc2_Column', dest='target', help=help)

    help = 'Percentage of the target, default 100'
    parser.add_argument('--percent',
                        action='store', default=100.0, dest='percent', help=help)

    help = 'Number of tags, default 1'
    parser.add_argument('--ntags',
                        action='store', default=1, dest='number_tags', help=help)

    help = 'The output path'
    parser.add_argument('--output',
                        action='store', default='.', dest='output', help=help)

    # Parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @create_targets
################################################################################
def create_targets(circuit_config,
                   target,
                   percent,
                   output,
                   number_tags):
    """Create the specified targets.

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

    # A list that will keep the data of all the neurons from the target
    target_data = list()

    # Filtering
    print('* Filtering circuit')
    for i_neuron, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

        # Morphology type
        morphology_type = neuron.morphology_type().name()

        # Filter the mtypes manually here
        if 'L5_TTPC1' in morphology_type or 'L5_TTPC2' in morphology_type:

            # Position
            position = str(neuron.position()).replace('[ ', '').replace(' ]', '')

            # Neuron orientation
            orientation = \
                str(neuron.orientation()).replace('[ ', '').replace(' ]', '').replace('0 1 0 ', '')

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
            tag = random.randint(1, number_tags)

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

            # Add the neuron data to the list
            target_data.append(neuron)

    # Sample the target randomly
    print('* Sampling target randomly')
    filtered_target_data = random.sample(set(target_data),
                                         int((len(target_data) * percent / 100.0)))

    # Construct the target name
    target_name = '%s_mtypes_%fp_random' % (target, float(percent))

    # Creating the output directory
    core.writer.create_directory(output)

    # Write the NeuroRender configuration file
    print('* Writing rendering config')
    core.write_neurorender_config(
        filtered_target_data, config_file_name=target_name, output_path=output)

    # Write the target file
    print('* Writing target file')
    core.write_target_file(
        filtered_target_data, target_name=target_name,
        target_file_name=target_name, output_path=output)


################################################################################
# @run
################################################################################
def run():
    """Run the script.
    """

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # create targets
    create_targets(circuit_config=argument_list.circuit_config,
                   target=argument_list.target,
                   percent=float(argument_list.percent),
                   output=argument_list.output,
                   number_tags=int(argument_list.number_tags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()
