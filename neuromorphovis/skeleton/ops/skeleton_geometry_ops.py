####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.bbox

####################################################################################################
# @compute_section_bounding_box
####################################################################################################
def compute_section_bounding_box(section,
                                 p_min,
                                 p_max):
    """
    Computes the bounding box of a morphological section.

    :param section:
        A given morphological section to compute the bounding box for. The result is stored in the
        p_min and p_max parameters.
    :param p_min:
        Return value for the p_min
    :param p_max:
        Return value for the p_max.
    """

    # Iterate over all the samples of the section and get the min and max ones
    for sample in section.samples:

        # Get the coordinates of the sample
        point = sample.point

        # Minimum
        if point[0] < p_min[0]:
            p_min[0] = point[0]
        if point[1] < p_min[1]:
            p_min[1] = point[1]
        if point[2] < p_min[2]:
            p_min[2] = point[2]

        # Maximum
        if point[0] > p_max[0]:
            p_max[0] = point[0]
        if point[1] > p_max[1]:
            p_max[1] = point[1]
        if point[2] > p_max[2]:
            p_max[2] = point[2]


####################################################################################################
# @compute_sections_bounding_box
####################################################################################################
def compute_sections_bounding_box(arbor,
                                  p_min,
                                  p_max):
    """
    Computes the bounding box of a morphological section and its children.

    :param arbor:
        A given arbor to compute the bounding box for.
    :param p_min:
        Return value for @p_min
    :param p_max:
        Return value for @p_max.
    """

    # Compute the bounding box for the first section
    compute_section_bounding_box(section=arbor, p_min=p_min, p_max=p_max)

    # Do it recursively
    for child_section in arbor.children:

        # Update the bounding box via updating p_min and p_max
        compute_sections_bounding_box(arbor=child_section, p_min=p_min, p_max=p_max)


####################################################################################################
# @compute_arbor_bounding_box
####################################################################################################
def compute_arbor_bounding_box(arbor):
    """
    Computes the bounding box of a given arbor.

    :param arbor:
        A given morphological arbor to compute the bounding box for.
    :return:
        The bounding box of the given arbor.
    """

    # Initialize the min and max points
    p_min = Vector((100000000000, 100000000000, 100000000000))
    p_max = Vector((-100000000000, -100000000000, -100000000000))

    # Compute the arbor bounding box
    compute_sections_bounding_box(arbor=arbor, p_min=p_min, p_max=p_max)

    # Build bounding box object
    bounding_box_object = nmv.bbox.BoundingBox(p_min=p_min, p_max=p_max)

    # Return the computed bounding box
    return bounding_box_object


####################################################################################################
# @compute_full_morphology_bounding_box
####################################################################################################
def compute_full_morphology_bounding_box(morphology):
    """
    Computes the bounding box of the entire morphology including all the existing arbors.

    :param morphology:
        A given morphology to compute the bounding box for.
    :return:
        The bounding box of the computed morphology.
    """

    # Compute the axon bounding box
    axon_bounding_box = None
    if morphology.has_axon():
        axon_bounding_box = compute_arbor_bounding_box(morphology.axon)

    # Compute basal dendrites bounding boxes
    basal_dendrites_bounding_boxes = []
    for dendrite in morphology.dendrites:
        basal_dendrite_bounding_box = compute_arbor_bounding_box(dendrite)
        basal_dendrites_bounding_boxes.append(basal_dendrite_bounding_box)

    # Compute apical dendrite bounding box, if exists
    apical_dendrite_bounding_box = None
    if morphology.has_apical_dendrite():
        apical_dendrite_bounding_box = compute_arbor_bounding_box(morphology.apical_dendrite)

    # Get the joint bounding box of the entire morphology by collecting the individual ones in a
    # list and then merging the list into a single bounding box
    morphology_bounding_boxes = basal_dendrites_bounding_boxes

    # If the axon is there, add it
    if axon_bounding_box is not None:
        morphology_bounding_boxes.append(axon_bounding_box)

    # If the apical dendrite is there, add it
    if apical_dendrite_bounding_box is not None:
        morphology_bounding_boxes.append(apical_dendrite_bounding_box)

    # Get the joint bounding box from the list
    morphology_bounding_box = nmv.bbox.extend_bounding_boxes(morphology_bounding_boxes)

    # Return the morphology bounding box
    return morphology_bounding_box


####################################################################################################
# @transform_to_global
####################################################################################################
def transform_to_global(neuron_object,
                        blue_config,
                        gid):
    """
    Transforms a given neuron object from the global coordinates to the local coordinates defined
    by a given circuit. The transformation matrix is obtained based on the GID of the neuron object.

    :param neuron_object:
        A given neuron object to transfer from local to global coordinates.
    :param blue_config:
        A circuit blue configuration that contains the absolute position of the neuron object.
    :param gid:
        The neuron identifier in the circuit that is used to retrieve its position in the circuit.
    """

    # To load the circuit, 'brain' must be imported
    try:
        import brain
    except ImportError:
        raise ImportError('ERROR: Cannot import \'brain\'')

    # Load the circuit data from the blue configuration
    circuit = brain.Circuit(blue_config)

    # Get the local to global transformation
    local_to_global_transformation = circuit.transforms({int(gid)})[0]

    # Initialize the transformation matrix to I
    transformation_matrix = Matrix()

    # Fill the matrix row by row
    for i in range(4):
        transformation_matrix[i][:] = local_to_global_transformation[i]

    # Apply the transformation operation vertex by vertex
    for vertex in neuron_object.data.vertices:

        # Update the vertex coordinates
        vertex.co = transformation_matrix * vertex.co