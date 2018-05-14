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

    help = 'output path'
    parser.add_argument('--output',
        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @get_axon_sections
################################################################################
def get_axon_sections(morphology):

	return morphology.sections({brain.neuron.SectionType.axon}) 


################################################################################
# @get_dendrites_sections
################################################################################	
def get_dendrites_sections(morphology):

	dendrites = [morphology.section(int(id)) \
		for id in morphology.section_ids({brain.neuron.SectionType.dendrite})]
	return dendrites
    
################################################################################
# @get_apical_dendrite_sections
################################################################################
def get_apical_dendrite_sections(morphology):

	apical_dendrite = [morphology.section(int(id)) \
        for id in morphology.section_ids(
            {brain.neuron.SectionType.apical_dendrite})]
	return apical_dendrite 


################################################################################
# @compute_sections_bounding_box
################################################################################
def compute_sections_bounding_box(sections):

	x_min = 1e32
	y_min = 1e32
	z_min = 1e32
	x_max = -1e32
	y_max = -1e32
	z_max = -1e32

	for section in sections:
		for sample in section.samples():
			x = sample[0]
			y = sample[1]
			z = sample[2]

			if x < x_min: x_min = x
			if y < y_min: y_min = y
			if z < z_min: z_min = z

			if x > x_max: x_max = x
			if y > y_max: y_max = y
			if z > z_max: z_max = z
			
	return [x_min, y_min, z_min, x_max, y_max, z_max]


################################################################################
# @compute_largest_bounding_box
################################################################################	
def compute_largest_bounding_box(bounding_boxes_list):

	x_min = 1e32
	y_min = 1e32
	z_min = 1e32
	x_max = -1e32
	y_max = -1e32
	z_max = -1e32

	for bounding_box in bounding_boxes_list:
		if bounding_box[0] < x_min: x_min = bounding_box[0]
		if bounding_box[1] < y_min: y_min = bounding_box[1]
		if bounding_box[2] < z_min: z_min = bounding_box[2]

		if bounding_box[3] > x_max: x_max = bounding_box[3]
		if bounding_box[4] > y_max: y_max = bounding_box[4]
		if bounding_box[5] > z_max: z_max = bounding_box[5]
	
	return [x_min, y_min, z_min, x_max, y_max, z_max]


################################################################################
# @compute_morphology_bounding_box
################################################################################
def compute_morphology_bounding_box(morphology):
	
	sections_bounding_boxes = []
	
	axon_sections = get_axon_sections(morphology)
	sections_bounding_boxes.append(
		compute_sections_bounding_box(axon_sections))
	
	dendrites_sections = get_dendrites_sections(morphology)
	sections_bounding_boxes.append(
		compute_sections_bounding_box(dendrites_sections))
	
	apical_dendrites_sections = get_apical_dendrite_sections(morphology)
	if len(apical_dendrites_sections) > 0:
		sections_bounding_boxes.append(
			compute_sections_bounding_box(apical_dendrites_sections))
			
	morphology_bounding_box = compute_largest_bounding_box(
		sections_bounding_boxes)
		
	return morphology_bounding_box
	
	
################################################################################
# @create_targets
################################################################################
def create_targets(circuit_config, target, output):
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
	bounds = []
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

		# compute bounding box
		bounding_box = compute_morphology_bounding_box(morphologies[i])

		# compose the neuron data
		neuron_data = '%s %s %s %s %s %s %s %s %s %s %s %s %s' % \
					  (str(gid),
					   str(1),
					   str(position.x()),
					   str(position.y()),
					   str(position.z()),
					   str(min_radius),
					   str(mean_radius),
					   str(max_radius),
					   str(morphology_type),
					   str(morphology_label),
					   str(column),
					   str(layer),
					   str(bounding_box))

		# add the neuron data to the list
		target_data.append(neuron_data)
		bounds.append(bounding_box)

	for i, j in zip(target_data, bounds):
		gid = i.split(" ")[0] 
		bounds_file = open('%s/%s.bounds' % (output, gid), 'w')
		bounds_file.write(str(j).strip('[]').replace(',', ''))
		bounds_file.close()

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
        argument_list.target, argument_list.output)


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()
