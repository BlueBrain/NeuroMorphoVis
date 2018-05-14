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
from mathutils import Vector, Matrix, bvhtree
import bmesh

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.scene


####################################################################################################
# @get_section_data_in_poly_line_format
####################################################################################################
def get_section_poly_line(section,
                          fixed_radius=None,
                          transform=None):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param fixed_radius:
        Use a fixed radius with this value, or None for using the values reported in the morphology.
    :param transform:
        Transform the points from local to circuit coordinates, only valid for a circuit.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = []

    # Global coordinates transformation, use I if no transform is given
    if transform is None:
        transform = Matrix()

    # Construct the section from all the samples
    for i in range(len(section.samples)):

        # Get the coordinates of the sample
        point = transform * section.samples[i].point

        # Append the data 'in the poly-line format' to the list
        if fixed_radius is None:

            # Use the actual radius of the samples reported in the morphology file
            poly_line.append([(point[0], point[1], point[2], 1), section.samples[i].radius])

        else:

            # Use a specific fixed radius along the entire skeleton for visual enhancement
            poly_line.append([(point[0], point[1], point[2], 1), fixed_radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_connected_sections_poly_line
####################################################################################################
def get_connected_sections_poly_line(section,
                                     is_continuous=False,
                                     is_last_section=False,
                                     fixed_radius=None,
                                     transform=None,
                                     process_terminals=False,
                                     connect_to_soma=False,
                                     bridge_to_soma=False):
    """Get the poly-line list or a series of points that reflect the skeleton of a group of
    connected sections along a single arbor or neurite.

    :param section:
        The geometry of the section.
    :param is_continuous:
        Is this section a continuation from a previous one or not.
    :param is_last_section:
        Is this section the last one along an arbor or not.
    :param fixed_radius:
        Use a fixed radius with this value, or None for using the values reported in the morphology.
    :param transform:
       Transform the points from local to circuit coordinates, only valid for a circuit.
    :param process_terminals:
        Process the terminal samples that would reduce the visual quality of the arbor.
    :param connect_to_soma:
        Add a set of auxiliary samples to connect the first sample of the root section to the
        center of the soma (or the origin).
    :param bridge_to_soma:
        Bridge the arbor to the soma surface, and do not connect it to the origin.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # Global coordinates transformation, use I if no transform is given
    if transform is None:
        transform = Matrix()

    # An array containing the data of the section
    poly_line = []

    # If the section is root, then connect it to the origin, if possible
    if section.is_root():

        # Bridge to the soma
        if bridge_to_soma:

            # The section must be logically connected to the soma after the filtration
            if section.connected_to_soma:

                # Add a sample around the origin
                direction = section.samples[0].point.normalized()

                # Sample radius
                radius = section.samples[0].radius

                # Get the starting point of the bridging section (note that delta is 0.25 in
                # case of bridging)
                point = \
                    section.samples[0].point - nmv.consts.Arbors.ARBOR_EXTRUSION_DELTA * direction

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

        # Normal connection to the soma
        else:

            # If the connection to the soma is required
            if connect_to_soma:

                # In the repair mode, if the section is not logically connected to the soma, then
                # ignore connecting the section to the soma
                if process_terminals:

                    # The section must be logically connected to the soma after the filtration
                    if section.connected_to_soma:

                        # Add a sample around the origin
                        direction = section.samples[0].point.normalized()

                        # The initial sample must be far from the origin by one micron
                        initial_sample = transform * Vector((0, 0, 0)) + direction

                        # Sample radius
                        radius = section.samples[0].radius

                        # Compute the distance between the first sample and the origin sample
                        distance = (section.samples[0].point - direction).length

                        # Use N samples, for example 5
                        number_samples = 5
                        for i in range(1, number_samples):

                            # Sample point
                            point = initial_sample + (direction * distance * (i / number_samples))

                            # Append the point to the poly-line data
                            poly_line.append([(point[0], point[1], point[2], 1), radius])

                        # Get the starting point of the bridging section (note that delta is 0.25 in
                        # case of bridging)
                        point = section.samples[0].point

                        # Append the sample to the list
                        poly_line.append([(point[0], point[1], point[2], 1), radius])

                # If the original skeleton is required to be connected to the soma anyway, then we
                # can safely connect the root section to the soma even if it's not logically
                # connected
                else:

                    # Add a sample around the origin
                    direction = section.samples[0].point.normalized()

                    # Sample radius
                    radius = section.samples[0].radius

                    # Sample coordinates
                    point = transform * (Vector((0, 0, 0)) + (1.0 * direction))

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

                    # Get the starting point of the bridging section (note that delta is 0.25 in
                    # case of bridging)
                    point = section.samples[0].point

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

            # If the connection to the soma is NOT required, add only a bridging sample
            else:

                # In the repair mode, if the section is not logically connected to the soma,
                # then ignore connecting the section to the soma
                if process_terminals:

                    # The section must be logically connected to the soma after the filtration
                    if section.connected_to_soma:

                        # Add a sample around the origin
                        direction = section.samples[0].point.normalized()

                        # Sample radius
                        radius = section.samples[0].radius

                        # Add the bridging sample
                        point = section.samples[0].point -\
                                (nmv.consts.Arbors.ARBOR_EXTRUSION_DELTA * direction)

                        # Append the sample to the list
                        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # If the section is a continuation, then do not pre-process the first samples
    if is_continuous:

        # If this is the last section, handle the LAST sample carefully
        if is_last_section:

            # Normal processing of the intermediate samples (ignore first and last)
            for i in range(0, len(section.samples) - 1):

                # Sample coordinates
                point = transform * section.samples[i].point

                # Sample radius
                radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Last sample coordinates
            point = transform * section.samples[-1].point

            # Last sample radius
            original_radius = section.samples[-1].radius
            radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                original_radius

            # Append the last sample to the list
            poly_line.append([(point[0], point[1], point[2], 1), radius])

        # Normal processing for the internal sections
        else:

            # Normal processing of the intermediate samples (ignore first sample only)
            for i in range(0, len(section.samples) - 1):

                # Sample coordinates
                point = transform * section.samples[i].point

                # Sample radius
                radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

    # This 'secondary' section is not a continuation from a previous section, it is a new section
    else: # is_continuous

        # If the section has a parent, then reduce the radius of the first sample
        if section.has_parent():

            # If this is the last section, reduce the radius of the last sample for a clean terminal
            if is_last_section:

                # Normal processing of the internal samples
                for i in range(0, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

                # Handle the last sample or the terminal point of the arbor
                # Sample coordinates
                point = transform * section.samples[-1].point

                # Sample radius
                original_radius = section.samples[-1].radius
                radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                    original_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Normal processing for the internal sections
            else:

                # Normal processing
                for i in range(0, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

        # For roots, just use all the samples
        else:

            # If this is the last section, reduce the radius of the last sample for a clean terminal
            if is_last_section:

                # Normal processing of the first n - 1 samples
                for i in range(0, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

                # Handle the last sample or the terminal point of the arbor
                # Sample coordinates
                point = transform * section.samples[-1].point

                # Sample radius
                original_radius = section.samples[-1].radius
                radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                    original_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # For a root, but non-terminating section, just use all the samples w/o processing
            else:

                # Add all the section samples
                for i in range(0, len(section.samples)):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    # radius = sample.radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_disconnected_skeleton_sections_poly_line
####################################################################################################
def get_disconnected_skeleton_sections_poly_line(section,
                                                 is_continuous=False,
                                                 is_last_section=False,
                                                 fixed_radius=None,
                                                 transform=None,
                                                 process_terminals=False,
                                                 extend_to_soma_origin=False):
    """
    Gets the poly-line list that represents a series of points that reflect that skeleton on
    a series of connected section along a single arbor.

    :param section:
        The geometry of a morphological section.
    :param is_continuous:
        Is this section a continuation from a previous one or not.
    :param is_last_section:
        Is this section the last one along an arbor or not.
    :param fixed_radius:
        Use a fixed radius with this value, or None.
    :param transform:
        Morphology circuit to local transform.
    :param process_terminals:
        Process the terminal samples that would reduce the visual quality of the arbor.
    :param extend_to_soma_origin:
        If this flag is set to True, the first samples of the root arbors will be connected to the
        origin of the soma, because the arbor will not be 'physically' connected to the soma mesh.
        On the other hand, if this Flag is set to False, we will only add an auxiliary sample
        before the initial segment of the root section to allow BRIDGING the arbor to the soma
        later during the mesh reconstruction operation.
    :return:
        Section data in poly-line format that is suitable for drawing.
    """

    # Global coordinates transformation, use I if no transform is given
    if transform is None:
        transform = Matrix()

    # An array containing the data of the section
    poly_line = []

    # If the section is root, then connect it to the origin, if possible
    if not section.has_parent():

        # Ensure that the section is LOGICALLY connected to the soma
        if section.connected_to_soma:

            # Add a sample around the origin
            direction = section.samples[0].point.normalized()

            # Sample radius
            radius = section.samples[0].radius

            # Extend the root section to the soma origin, and add few extra samples between the
            # origin and the bridging sample to avoid vertex smoothing artifacts around the root
            # sections
            if extend_to_soma_origin:

                # Add a sample around the origin
                direction = section.samples[0].point.normalized()

                # The initial sample must be far from the origin by one micron
                initial_sample = transform * Vector((0, 0, 0)) + direction

                # Bridging sample
                bridging_sample = section.samples[0].point - \
                                  (nmv.consts.Arbors.ARBOR_EXTRUSION_DELTA * direction)

                # Sample radius
                radius = section.samples[0].radius

                # Compute the distance between the first sample and the origin sample
                distance = (bridging_sample - initial_sample).length

                # Use N samples, for example 5
                number_samples = 5
                for i in range(1, number_samples - 1):

                    # Sample point
                    point = initial_sample + (direction * distance * (i / number_samples))

                    # Append the point to the poly-line data
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Add the bridging sample
            point = section.samples[0].point - 0.5 * direction

            # Append the sample to the list
            poly_line.append([(point[0], point[1], point[2], 1), radius])

    # If the section is a continuation, then do not pre-process the first samples
    if is_continuous:

        # If the primary section is disconnected, then start from the second sample
        starting_index = 1 if process_terminals else 0

        # If this is the last section, handle the LAST sample carefully
        if is_last_section:

            # Normal processing of the intermediate samples (ignore first and last)
            for i in range(starting_index, len(section.samples) - 1):

                # Sample coordinates
                point = transform * section.samples[i].point

                # Sample radius
                radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Last sample coordinates
            point = transform * section.samples[-1].point

            # Last sample radius
            original_radius = section.samples[-1].radius
            radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                original_radius

            # Append the last sample to the list
            poly_line.append([(point[0], point[1], point[2], 1), radius])

        # Normal processing for the internal sections
        else:

            # Normal processing of the intermediate samples (ignore first sample only)
            for i in range(starting_index, len(section.samples) - 1):

                # Sample coordinates
                point = transform * section.samples[i].point

                # Sample radius
                radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

    # This 'secondary' section is not a continuation from a previous section, it is a new section
    else: # is_continuous

        # If the section has a parent, then reduce the radius of the first sample
        if section.has_parent():

            # If this is the last section, reduce the radius of the last sample for a clean terminal
            if is_last_section:

                # Normal processing of the internal samples
                for i in range(1, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    # radius = section.samples[i].radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

                # Handle the last sample or the terminal point of the arbor
                # Sample coordinates
                point = transform * section.samples[-1].point

                # Sample radius
                original_radius = section.samples[-1].radius
                radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                    original_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Normal processing for the internal sections
            else:

                # Normal processing
                for i in range(1, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    # radius = section.samples[i].radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

        # For roots, just use all the samples
        else:

            # If this is the last section, reduce the radius of the last sample for a clean terminal
            if is_last_section:

                # Normal processing of the first n - 1 samples
                for i in range(1, len(section.samples) - 1):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    # radius = section.samples[i].radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

                # Handle the last sample or the terminal point of the arbor
                # Sample coordinates
                point = transform * section.samples[-1].point

                # Sample radius
                original_radius = section.samples[-1].radius
                radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS if process_terminals else \
                    original_radius

                # Append the sample to the list
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # For a root, but non-terminating section, just use all the samples w/o processing
            else:

                # Remove the last sample if this is not a not terminating section and the
                # disconnect primary flag is active
                last_index = len(section.samples)
                if process_terminals:
                    last_index -= 1

                # Add all the section samples
                for i in range(0, last_index):

                    # Sample coordinates
                    point = transform * section.samples[i].point

                    # Sample radius
                    # radius = sample.radius
                    radius = section.samples[i].radius if fixed_radius is None else fixed_radius

                    # Append the sample to the list
                    poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_poly_line_length
####################################################################################################
def get_poly_line_length(poly_line):
    """
    Returns the total length of a poly-line.
    :param poly_line:
        A given poly-line array to get its total length
    :return:
        The length of the poly-line.
    """

    # Initialize the poly-line length to zero
    poly_line_length = 0.0

    # Get a reference to the poly-line points list
    poly_line_points = poly_line.data.splines.active.points

    # Compute the length of the poly-line
    for i in range(len(poly_line_points) - 1):

        # Get access to the points
        point_0 = poly_line_points[i]
        point_1 = poly_line_points[i + 1]

        # Compute the distance between the two points
        distance = (point_1.co - point_0.co).length

        # Update the poly-line length
        poly_line_length += distance

    # Return the poly-line length
    return poly_line_length


####################################################################################################
# @get_poly_line_normalized_start_factor
####################################################################################################
def get_poly_line_normalized_start_factor(distance,
                                          poly_line_length):
    """
    Returns what's called the 'bevel_factor_start' factor that will be used to draw the poly-line.
    This value is set to update the parameter bpy.context.object.data.bevel_factor_start later
    during the meshing operations to avoid any intersections between the primary and secondary
    meshes.

    :param distance:
        A given distance along the poly-line.
    :param poly_line_length:
        Actual poly-line length.
    :return:
        The bevel_factor_start factor
    """

    # Compute the starting factor
    starting_factor = distance / poly_line_length

    if starting_factor > 1.0:
        return 0.0

    # Return the normalized value
    return starting_factor


####################################################################################################
# @poly_lines_intersect
####################################################################################################
def poly_lines_intersect(poly_line_1,
                         poly_line_2):
    """
    Applies a poly-line intersection test on the given two poly-lines and return True if the two
    poly-lines intersect or False if they do not.

    :param poly_line_1:
        Primary poly-line.
    :param poly_line_2:
        Secondary poly-line.
    :return:
        True or False.
    """

    # Duplicate the poly-lines
    poly_line_1_duplicate = nmv.scene.ops.duplicate_object(poly_line_1)
    poly_line_2_duplicate = nmv.scene.ops.duplicate_object(poly_line_2)

    # Convert them to meshes
    nmv.scene.ops.convert_object_to_mesh(poly_line_1_duplicate)
    nmv.scene.ops.convert_object_to_mesh(poly_line_2_duplicate)

    # Create a new bmesh from the meshes
    poly_line_1_bmesh = bmesh.new()
    poly_line_2_bmesh = bmesh.new()

    poly_line_1_bmesh.from_mesh(poly_line_1_duplicate.data)
    poly_line_2_bmesh.from_mesh(poly_line_2_duplicate.data)

    # To make the intersection faster, transform the poly-lines
    poly_line_1_bmesh.transform(poly_line_1_duplicate.matrix_world)
    poly_line_2_bmesh.transform(poly_line_2_duplicate.matrix_world)

    # Create the BVH for the two meshes
    bv_m1 = bvhtree.BVHTree.FromBMesh(poly_line_1_bmesh)
    bv_m2 = bvhtree.BVHTree.FromBMesh(poly_line_2_bmesh)

    # Find the overlap between the two poly-line meshes
    overlap_list= bv_m1.overlap(bv_m2)

    # Delete the duplicated objects
    nmv.scene.ops.delete_list_objects([poly_line_1_duplicate, poly_line_2_duplicate])

    # If the overlap list is empty, then there is no intersection between the two poly-lines
    if len(overlap_list) == 0:
        return False

    # Otherwise, the two poly-lines do intersect
    return True


####################################################################################################
# @poly_lines_intersect
####################################################################################################
def poly_line_intersect_mesh(poly_line,
                             mesh):
    """
    Applies a poly-line intersection test on the given poly-line and mesh and return True if they
    intersect or False if they do not.

    :param poly_line:
        A given poly-line.
    :param mesh:
        A given mesh
    :return:
        True or False.
    """

    # Duplicate the poly-line
    poly_line_duplicate = nmv.scene.ops.duplicate_object(poly_line)

    # Convert them to meshes
    nmv.scene.ops.convert_object_to_mesh(poly_line_duplicate)

    # Create a new bmesh from the meshes
    poly_line_1_bmesh = bmesh.new()
    mesh_bmesh = bmesh.new()

    poly_line_1_bmesh.from_mesh(poly_line_duplicate.data)
    mesh_bmesh.from_mesh(mesh.data)

    # To make the intersection faster, transform the poly-lines
    poly_line_1_bmesh.transform(poly_line_duplicate.matrix_world)
    mesh_bmesh.transform(mesh.matrix_world)

    # Create the BVH for the two meshes
    bv_m1 = bvhtree.BVHTree.FromBMesh(poly_line_1_bmesh)
    bv_m2 = bvhtree.BVHTree.FromBMesh(mesh_bmesh)

    # Find the overlap between the two poly-line meshes
    overlap_list= bv_m1.overlap(bv_m2)

    # Delete the duplicated poly-line from the scene
    nmv.scene.ops.delete_list_objects([poly_line_duplicate])

    # If the overlap list is empty, then there is no intersection between the two poly-lines
    if len(overlap_list) == 0:
        return False

    # Otherwise, the two poly-lines do intersect
    return True