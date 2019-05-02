####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# System imports
import random, copy

# Blender imports
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.bbox
import nmv.skeleton


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
# @get_transformation_matrix
####################################################################################################
def get_transformation_matrix(blue_config,
                              gid):
    """Get the transformation matrix that correspond to a given neuron with a specific GID.

    :param blue_config:
        A given BBP circuit configuration.
    :param gid:
        Neuron GID.
    :return:
        Transformation matrix.

    """
    # To load the circuit, 'brain' must be imported
    try:
        import brain
    except ImportError:
        raise ImportError('ERROR: Cannot import \'brain\'')

    # Load the circuit data from the blue configuration
    circuit = brain.Circuit(blue_config)

    # Get the local to global transformation
    origin_to_circuit_transform = circuit.transforms({int(gid)})[0]

    # Initialize the transformation matrix to I
    transformation_matrix = Matrix()

    # Fill the matrix row by row
    for i in range(4):
        transformation_matrix[i][:] = origin_to_circuit_transform[i]

    return transformation_matrix


####################################################################################################
# @transform_to_local_coordinates
####################################################################################################
def transform_to_local_coordinates(mesh_object,
                                   blue_config,
                                   gid):
    """Transforms a given mesh object to the local coordinates.

    :param mesh_object:
        A given mesh object to get transformed.
    :param blue_config:
        A circuit blue configuration that contains the absolute position of the mesh object.
    :param gid:
        The neuron identifier in the circuit that is used to retrieve its position in the circuit.
    """

    # Get the transformation matrix
    transformation_matrix = get_transformation_matrix(blue_config=blue_config, gid=gid)

    # Invert the transformation matrix
    transformation_matrix = transformation_matrix.inverted()

    # Apply the transformation operation vertex by vertex
    for vertex in mesh_object.data.vertices:

        # Update the vertex coordinates
        vertex.co = transformation_matrix * vertex.co


####################################################################################################
# @transform_to_global
####################################################################################################
def transform_to_global_coordinates(mesh_object,
                                    blue_config,
                                    gid):
    """Transforms a given mesh object from the local coordinates to the global coordinates.

     The transformation matrix is obtained based on the GID of the neuron object.

    :param mesh_object:
        A given neuron object to get transformed.
    :param blue_config:
        A circuit blue configuration that contains the absolute position of the mesh object.
    :param gid:
        The neuron identifier in the circuit that is used to retrieve its position in the circuit.
    """

    # Get the transformation matrix
    transformation_matrix = get_transformation_matrix(blue_config=blue_config, gid=gid)

    # Apply the transformation operation vertex by vertex
    for vertex in mesh_object.data.vertices:

        # Update the vertex coordinates
        vertex.co = transformation_matrix * vertex.co


####################################################################################################
# @transform_morphology_to_global_coordinates
####################################################################################################
def transform_morphology_to_global_coordinates(morphology_objects,
                                               blue_config,
                                               gid):
    """Transforms a given morphology, including the soma and the arbors.

    :param morphology_objects:
        A list of all the objects of the morphology including the arbors and the soma.
    :param blue_config:
        A circuit blue configuration that contains the absolute position of the mesh object.
    :param gid:
        The neuron identifier in the circuit that is used to retrieve its position in the circuit.
    """

    # Get the transformation matrix
    transformation_matrix = get_transformation_matrix(blue_config=blue_config, gid=gid)

    # Arbors transformation
    for morphology_object in morphology_objects:

        # Update the arbors transformation
        morphology_object.matrix_world = transformation_matrix * morphology_object .matrix_world


####################################################################################################
# @taper_section
####################################################################################################
def taper_section(section):
    """Taper a given section.

    This function is used to change the structure of the morphology for artistic purposes. It gets
    the maximum and minimum radii along the section and re-calculates the radii of the samples
    according to their order along the section.

    :param section:
        A given section along the arbor.
    """

    # Get the maximum radius of the section
    section_maximum_radius = nmv.skeleton.ops.compute_max_section_radius(section=section)

    # Get the minimum radius of the section
    section_minimum_radius = nmv.skeleton.ops.compute_min_section_radius(section=section)

    # If this is not a root section, the section maximum radius must be compared to the radius of
    # the last sample of the parent section
    if not section.is_root():

        # Get the radius of the last sample of the parent section
        parent_section_radius = section.parent.samples[-1].radius

        # If the radius of the last sample of the parent section is smaller than section maximum
        # radius, then update the section maximum radius
        if section_maximum_radius > parent_section_radius:
            section_maximum_radius = parent_section_radius

        # If the section maximum radius became greater than the section minimum radius, then set
        # the minimum radius to be a little smaller than the section maximum radius
        if section_minimum_radius > section_maximum_radius:
            section_minimum_radius = section_maximum_radius * 0.9

    # Get the length of the section (in terms of number of samples)
    number_samples = len(section.samples)

    # Make sure that the section has more than one sample
    if number_samples < 2:
        return

    # Ignore root sections
    if section.is_root():
        # To avoid any artifacts when the arbor is getting welded to the soma
        section.samples[1].radius = section_maximum_radius
    else:
        section.samples[0].radius = section_maximum_radius

    # Set the radius of the last sample to the smaller radius
    section.samples[-1].radius = section_minimum_radius

    # If the section has only two samples, return
    if number_samples == 2:
        return

    # Compute the difference
    difference = section_maximum_radius - section_minimum_radius

    # Compute the step of the inner samples between i = 1 and i = number_samples - 1
    section_step = difference / (number_samples - 1)

    # Set the radii based on their distance from the first sample
    for i in range(1, len(section.samples) - 1):

        # Avoid changing the second sample of the root section
        if section.is_root() and i == 1:
            continue

        # Do it for the internal samples
        section.samples[i].radius = section_maximum_radius - (i * section_step)


####################################################################################################
# @zigzag_section
####################################################################################################
def zigzag_section(section,
                   delta=0.9):
    """Zigzag a given section by adding abrupt changes in its geometry.
    This function is only used for artistic purposes as it changes the structure of the
    original morphology.

    NOTES:
    1. Do NOT mess with the initial and lat samples of the sections.
    2. Zigzag directions are random, BUT PERPENDICULAR to the arbor direction.

    :param section:
        A given section to zigzag.
    :param delta:
        The delta (distance) value.
    """

    # Get the length of the section (in terms of number of samples)
    number_samples = len(section.samples)

    # Ignore the first few samples on the root section to have nicer connection with the soma
    if section.is_root():

        if number_samples < 5:
            return

        for i in range(4, number_samples - 2):

            # Compute the normal direction
            random_direction = Vector((random.random(), random.random(), random.random()))

            # Compute the new sample position
            section.samples[i].point += random_direction * random.uniform(-delta, delta)

    # Non root section
    else:

        # Make sure that the section has more than two samples to proceed
        if number_samples < 3:
            return

        for i in range(1, number_samples - 2):

            # Compute the normal direction
            random_direction = Vector((random.random(), random.random(), random.random()))

            # Compute the new sample position
            section.samples[i].point += random_direction * random.uniform(-delta, delta)


####################################################################################################
# @simplify_section_to_straight_line
####################################################################################################
def simplify_section_to_straight_line(section):
    """Simplify the section structure into a straight line that is composed of only two samples
    at the beginning and end of the line.

    :param section:
        A given morphology section.
    """

    # Compose a list of only two samples
    straight_samples = [section.samples[0], section.samples[-1]]

    # Update the samples list in the section
    section.samples = straight_samples


####################################################################################################
# @scale_section_radii
####################################################################################################
def scale_section_radii(section,
                        scale_factor):
    """Scale the section radii.

    :param section:
        A given section.
    :param scale_factor:
        A scale factor that will be used to scale the section.
    """

    # Scale the radius of each section sample
    for i_sample in section.samples:
        i_sample.radius *= scale_factor


####################################################################################################
# @fix_section_radii
####################################################################################################
def fix_section_radii(section,
                      fixed_radius):
    """Fix the radius of all the samples along a given section.
    :param section:
        A given section to filter.
    :param fixed_radius:
        The radius that will be set to all the samples of the section.
    """

    # Set the radius of each section sample to the given fixed radius
    for i_sample in section.samples:
        i_sample.radius = fixed_radius


####################################################################################################
# @filter_section_sub_threshold
####################################################################################################
def filter_section_sub_threshold(section,
                                 threshold):
    """Filters a section with a radius lower than a given threshold value.

    :param section:
         A given section to filter.
    :param threshold:
        Threshold radius.
    """

    # Filter each section sample based on its radius
    for i_sample in section.samples:
        if i_sample.radius < threshold:
            i_sample.radius = 0.00001


####################################################################################################
# @update_branching_order_section
####################################################################################################
def update_branching_order_section(section,
                                   branching_order=1):
    """Update the branching order of the section.

    :param section:
        A given section.
    :param branching_order:
        The current branching order.
    """

    if section is None:
        return

    if section.is_root():
        section.branching_order = 1

    # Do it recursively
    for child_section in section.children:

        # Update the bounding box via updating p_min and p_max
        update_branching_order_section(section=child_section, branching_order=branching_order + 1)


####################################################################################################
# @simplify_morphology
####################################################################################################
def simplify_morphology(section):

    # Handle only the
    if section.is_root():

        # Get the maximum radius of the section
        section_maximum_radius = nmv.skeleton.ops.compute_max_section_radius(section=section)

        # Set the section minimum radius to a very small value
        section_minimum_radius = 0.0001

        # Compute the difference
        difference = section_maximum_radius - section_minimum_radius

        # Get the length of the section (in terms of number of samples)
        number_samples = len(section.samples)

        # Compute the step of the inner samples between i = 1 and i = number_samples - 1
        section_step = difference / (number_samples - 1)

        # Set the radii based on their distance from the first sample
        for i in range(0, len(section.samples)):

            # Do it for the internal samples
            section.samples[i].radius = section_maximum_radius - (i * section_step)

        # Omit the children
        section.children = []
