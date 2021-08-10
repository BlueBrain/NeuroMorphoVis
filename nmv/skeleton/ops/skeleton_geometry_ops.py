####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
    p_min = Vector((1e10, 1e10, 1e10))
    p_max = Vector((-1e10, -1e10, -1e10))

    # Compute the arbor bounding box
    compute_sections_bounding_box(arbor=arbor, p_min=p_min, p_max=p_max)

    # Build bounding box object
    bounding_box_object = nmv.bbox.BoundingBox(p_min=p_min, p_max=p_max)

    # Return the computed bounding box
    return bounding_box_object


####################################################################################################
# @compute_sections_list_bounding_box
####################################################################################################
def compute_sections_list_bounding_box(sections_list):
    """Computes the bounding box of a list of sections.

    :param sections_list:
        A group of sections in a list to compute the bounding box for.
    :return:
        THe resulting bounding box.
    """

    sections_bounding_boxes = list()

    # Initialize the min and max points
    p_min = Vector((1e10, 1e10, 1e10))
    p_max = Vector((-1e10, -1e10, -1e10))

    # Compute the bounding box for each section
    for section in sections_list:
        sections_bounding_boxes.append(
            nmv.skeleton.ops.compute_section_bounding_box(section, p_min, p_max))

    return sections_bounding_boxes


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

    # Arbors bounding box
    arbors_bounding_boxes = list()

    # Compute the axons bounding box
    if morphology.has_axons():
        for arbor in morphology.axons:
            arbors_bounding_boxes.append(compute_arbor_bounding_box(arbor=arbor))

    # Compute basal dendrites bounding boxes
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:
            arbors_bounding_boxes.append(compute_arbor_bounding_box(arbor=arbor))

    # Compute apical dendrite bounding box, if exists
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:
            arbors_bounding_boxes.append(compute_arbor_bounding_box(arbor=arbor))

    # Get the joint bounding box of the entire morphology by collecting the individual ones in a
    # list and then merging the list into a single bounding box
    morphology_bounding_box = nmv.bbox.extend_bounding_boxes(arbors_bounding_boxes)

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

    # Import BluePy
    try:
        import bluepy
    except ImportError:
        print('ERROR: Cannot import [BluePy], please install it')
        return None

    # Loading a circuit
    from bluepy import Circuit
    circuit = Circuit(blue_config)

    # Get the neuron
    neuron = circuit.cells.get(int(gid))

    # Translation
    translation = Vector((neuron['x'], neuron['y'], neuron['z']))

    # Orientation
    o = neuron['orientation']
    o0 = Vector((o[0][0], o[0][1], o[0][2]))
    o1 = Vector((o[1][0], o[1][1], o[1][2]))
    o2 = Vector((o[2][0], o[2][1], o[2][2]))

    # Initialize the transformation matrix to I
    transformation_matrix = Matrix()

    transformation_matrix[0][0] = o0[0]
    transformation_matrix[0][1] = o0[1]
    transformation_matrix[0][2] = o0[2]
    transformation_matrix[0][3] = translation[0]

    transformation_matrix[1][0] = o1[0]
    transformation_matrix[1][1] = o1[1]
    transformation_matrix[1][2] = o1[2]
    transformation_matrix[1][3] = translation[1]

    transformation_matrix[2][0] = o2[0]
    transformation_matrix[2][1] = o2[1]
    transformation_matrix[2][2] = o2[2]
    transformation_matrix[2][3] = translation[2]

    transformation_matrix[2][0] = 0.0
    transformation_matrix[2][1] = 0.0
    transformation_matrix[2][2] = 0.0
    transformation_matrix[2][3] = 1.0

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
# @project_to_plane
####################################################################################################
def project_to_xy_plane(section):
    """Project the section to XY plane.

    :param section:
        A given section to project.
    """

    # Get the length of the section (in terms of number of samples)
    number_samples = len(section.samples)

    for i in range(0, number_samples):

        # Compute the new sample position
        section.samples[i].point[2] = 0


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
# @unify_section_radii
####################################################################################################
def unify_section_radii(section,
                        unified_radius):
    """Unify the radius of all the samples along a given section.
    :param section:
        A given section to filter.
    :param unified_radius:
        The radius that will be set to all the samples of the section.
    """

    # Set the radius of each section sample to the given fixed radius
    for i_sample in section.samples:
        i_sample.radius = unified_radius


####################################################################################################
# @unify_section_radii_based_on_type
####################################################################################################
def unify_section_radii_based_on_type(section,
                                      axon_section_unified_radius,
                                      apical_dendrite_section_radius,
                                      basal_dendrite_section_radius):
    """Unifies the radius of all the samples along a given section based on its type.

    :param section:
        A given section to apply the filter to.
    :param axon_section_unified_radius:
        The unified radius that will be set to all the samples of the axon.
    :param apical_dendrite_section_radius:
        The unified radius that will be set to all the samples of the apical dendrite.
    :param basal_dendrite_section_radius:
        The unified radius that will be set to all the samples of the basal dendrites.
    """

    if section.is_axon():
        for i_sample in section.samples:
            i_sample.radius = axon_section_unified_radius
    elif section.is_apical_dendrite():
        for i_sample in section.samples:
            i_sample.radius = apical_dendrite_section_radius
    elif section.is_basal_dendrite():
        for i_sample in section.samples:
            i_sample.radius = basal_dendrite_section_radius
    else:
        return


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
# @set_section_radii_between_given_range
####################################################################################################
def set_section_radii_between_given_range(section,
                                          minimum_value,
                                          maximum_value):
    """Filters a section with a radius lower than a given threshold value.

    :param section:
         A given section to filter.
    :param minimum_value:
        The minimum radius value.
    :param maximum_value:
        The maximum radius value.
    """

    # Ignore the filter if dirty values were given
    if minimum_value > maximum_value:
        return

    # Filter each section sample based on its radius
    for i_sample in section.samples:
        if i_sample.radius < minimum_value:
            i_sample.radius = minimum_value
        if i_sample.radius > maximum_value:
            i_sample.radius = maximum_value


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
        section.children = list()


####################################################################################################
# @center_morphology
####################################################################################################
def center_morphology(section,
                      soma_centroid):
    """Center a given section in the morphology.

    :param section:
        A given section to center.
    :param soma_centroid:
        The center of the soma.
    """

    for sample in section.samples:
        sample.point -= soma_centroid


####################################################################################################
# @find_section_radius_near_point
####################################################################################################
def find_section_radius_near_point(section,
                                   point):
    """Finds the radius of the closest sample along the section to a given point in space.

    :param section:
        A given section.
    :param point:
        A point in space to perform the search.
    :return:
        The radius of the closest sample along the section to the given point in space.
    """

    # Initial, set to large number
    nearest_sample_distance = 1e10

    # Radius to be found
    radius = 0.0

    # For each sample along the section
    for i_sample in section.samples:

        # Compute the distance
        distance = (i_sample.point - point).length

        # Compare
        if distance < nearest_sample_distance:

            # Update the distance
            nearest_sample_distance = distance

            # Update the radius
            radius = float(i_sample.radius)

    # Return the final radius
    return radius
