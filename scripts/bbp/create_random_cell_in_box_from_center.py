"""
Computes the bounding box of the target and the extracts random samples 
from the center based on a given box dimensions.  
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
    
    help = 'x'
    parser.add_argument('--x',
        action='store', dest='x', default=50.0,  help=help)
    
    help = 'y'
    parser.add_argument('--y',
        action='store', dest='y', default=50.0, help=help)

    help = 'z'
    parser.add_argument('--z',
        action='store', dest='z', default=50.0, help=help)

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
                   x, y, z,
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
    
    # compute the target bounding box 
    target_x_min = 1e32; target_y_min = 1e32; target_z_min = 1e32
    target_x_max = -1e32; target_y_max = -1e32; target_z_max = -1e32
    
    for neuron in neurons:
        position = neuron.position()
        if position.x() > target_x_max:
            target_x_max = position.x()
        if position.y() > target_y_max:
            target_y_max = position.y()
        if position.z() > target_z_max:
            target_z_max = position.z()
            
        if position.x() < target_x_min:
            target_x_min = position.x()
        if position.y() < target_y_min:
            target_y_min = position.y()
        if position.z() < target_z_min:
            target_z_min = position.z()
    
    target_x_center = target_x_min + ((target_x_max - target_x_min) * 0.5)
    target_y_center = target_y_min + ((target_y_max - target_y_min) * 0.5)
    target_z_center = target_z_min + ((target_z_max - target_z_min) * 0.5)
    
    # compute actual bounding box of the experiment 
    bound_x_min = target_x_center - (0.5 * x);
    bound_x_max = target_x_center + (0.5 * x);
    bound_y_min = target_y_center - (0.5 * y);
    bound_y_max = target_y_center + (0.5 * y);
    bound_z_min = target_z_center - (0.5 * z);
    bound_z_max = target_z_center + (0.5 * z);
    
    neurons_list = []
    # get all the cells with that specific mtype
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):
        
        # position
        position = neuron.position()
        
        if position.x() < bound_x_max and position.x() > bound_x_min and \
           position.y() < bound_y_max and position.y() > bound_y_min and \
           position.z() < bound_z_max and position.z() > bound_z_min:
           

            # fetch neuron data
            morphology_type = neuron.morphology_type().name()
        
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
            
            # add the neuron data to the list
            neurons_list.append(neuron_data)

    sampled_neuron_list = random.sample(set(neurons_list),
        int((len(neurons_list) * percent / 100.0)))

    # create the output directory
    output = '%s/%s_%s_%s_%s_%sp' % (output, target, str(x), str(y), str(z), str(percent))
    writer.clean_and_create_directory(output)
    
    # write bounds to a file
    bounds_file = open('%s/%s_%s_%s_%s_%sp.bounds' % \
        (output, target, str(x), str(y), str(z), str(percent)), 'w')
    bounds_file.write('%f %f %f %f %f %f' % (bound_x_min, bound_y_min, 
        bound_z_min, bound_x_max, bound_y_max, bound_z_max))
    bounds_file.close()
    
    voxelization_target_output = open("%s/%s_%s_%s_%s_%sp.list" %
                                      (output, target, str(x), str(y), str(z), str(percent)), 'w')
    default_target_output = open(
        "%s/%s_%s_%s_%s_%sp.target" % (output, target, str(x), str(y), str(z), str(percent)), 'w')
    default_target_output.write(
        "Target Cell Box_%s_%s_%s_%s_%sp \n" % (target, str(x), str(y), str(z), str(percent)))
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
        x=float(argument_list.x), y=float(argument_list.y), z=float(argument_list.z),
        target=argument_list.target,
        percent=float(argument_list.percent),
        ntags=int(argument_list.ntags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()
