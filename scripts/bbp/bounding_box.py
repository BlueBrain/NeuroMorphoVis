"""
bounding_box.py:
    Compute the bounding box of the morphology based on the samples.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# imports
import brain

################################################################################
# @compute_bounding_box_for_morphology
################################################################################
def compute_largest_union_bounding_box(bounding_boxes_list):
    """
    Computes the union or the largest bounding box of a given list of
    bounding boxes.
    Output format is [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]

    :param bounding_boxes_list: Input list of multiple bounding boxes.
    :return: Output format is [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]
    """

    x_min = 1e32; y_min = 1e32; z_min = 1e32
    x_max = -1e32; y_max = -1e32; z_max = -1e32

    for bounding_box in bounding_boxes_list:
        if bounding_box[0] < x_min: x_min = bounding_box[0]
        if bounding_box[1] < y_min: y_min = bounding_box[1]
        if bounding_box[2] < z_min: z_min = bounding_box[2]
        if bounding_box[3] > x_max: x_max = bounding_box[3]
        if bounding_box[4] > y_max: y_max = bounding_box[4]
        if bounding_box[5] > z_max: z_max = bounding_box[5]

    return [x_min, y_min, z_min, x_max, y_max, z_max]


################################################################################
# @compute_bounding_box_for_morphology
################################################################################
def compute_bounding_box_for_branch(branch):
    """
    Compute the bounding box of a branch.
    Output format is [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]

    :param branch: Input branch to compute the bounding box for.
    :return: [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]
    """

    x_min = 1e32; y_min = 1e32; z_min = 1e32
    x_max = -1e32; y_max = -1e32; z_max = -1e32

    print(len(branch))
    for section in branch:
        for sample in section.samples():
            if sample[0] < x_min: x_min = sample[0]
            if sample[1] < y_min: y_min = sample[1]
            if sample[2] < z_min: z_min = sample[2]
            if sample[0] > x_max: x_max = sample[0]
            if sample[1] > y_max: y_max = sample[1]
            if sample[2] > z_max: z_max = sample[2]

    return [x_min, y_min, z_min, x_max, y_max, z_max]


################################################################################
# @compute_bounding_box_for_morphology
################################################################################
def compute_bounding_box_for_morphology(morphology):
    """
    Computes the bounding box for a given morphology.
    Output format is [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]

    :param morphology: Input morphology (using brain)
    :return: [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]
    """

    # get axon, dendrites and apical dendrite
    axon = \
        morphology.sections({brain.neuron.SectionType.axon})
    dendrites = \
        morphology.sections({brain.neuron.SectionType.dendrite})
    apical_dendrite = \
        morphology.sections({brain.neuron.SectionType.apical_dendrite})

    # compute the bounding boxes of each component
    bounding_boxes_list = []
    bounding_boxes_list.append(compute_bounding_box_for_branch(axon))
    bounding_boxes_list.append(compute_bounding_box_for_branch(dendrites))
    if len(apical_dendrite) > 0:
        bounding_boxes_list.append(compute_bounding_box_for_branch(
            apical_dendrite))

    # get the union or the largest bounding box
    morphology_bounding_box = compute_largest_union_bounding_box(
        bounding_boxes_list)

    # return the morphology bounding box
    return morphology_bounding_box


################################################################################
# @compute_boundig_box_for_gid
################################################################################
def compute_boundig_box_for_gid(blue_config, gid):
    """
    Computes the bounding box of a neuron from its gid.
    Output format is [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]

    :param blue_config: Circuit configuration.
    :param gid: Neuron gid.
    :return: [X_MIN, Y_MIN, Z_MIN, X_MAX, Y_MAX, Z_MAX]
    """

    # load the circuit and the selected target gid
    circuit = brain.Circuit(blue_config)

    # build gid set
    gids = circuit.gids("a" + gid)

    # load the morphology
    circuit.load_morphologies(gids, circuit.Coordinates.local)

    # get the uris
    uris = circuit.morphology_uris(gids)

    # retrieve the morphology data from the circuit
    morphology = brain.neuron.Morphology(uris[0])

    # return the bounding box of the selected morphology
    return compute_bounding_box_for_morphology(morphology)