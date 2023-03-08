####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# System import
import copy
import random

# Blender imports
from mathutils import Vector, Matrix, bvhtree
import bmesh
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.geometry
import nmv.mesh
import nmv.bmeshi
import nmv.utilities

import bpy
import bmesh
import time

from mathutils.bvhtree import BVHTree
from mathutils import Vector
from random import randint


####################################################################################################
# @get_indexed_segments_polylines
####################################################################################################
def get_indexed_segments_polylines(section,
                                   value,
                                   minimum_value,
                                   maximum_value,
                                   colormap_resolution,
                                   prefix,
                                   branching_order):

    # A list that will contain all the constructed polylines
    polylines = list()

    # Construct the segments polylines
    for i in range(len(section.samples) - 1):

        # Reference to the original segment samples
        sample_1 = section.samples[i]
        sample_2 = section.samples[i + 1]

        # Segment polyline samples
        samples = list()
        samples.append([(sample_1.point[0], sample_1.point[1], sample_1.point[2], 1),
                        sample_1.radius])
        samples.append([(sample_2.point[0], sample_2.point[1], sample_2.point[2], 1),
                        sample_2.radius])

        # Get the material index
        material_index = nmv.utilities.get_index(
            value=value, minimum_value=minimum_value, maximum_value=maximum_value,
            number_steps=colormap_resolution)

        # Construct the polyline
        polyline = nmv.geometry.PolyLine(
            name='%s_%d_%d' % (prefix, branching_order, i), samples=samples,
            material_index=material_index)

        # Append the polyline to the polylines list
        polylines.append(polyline)

    # Return the resulting list
    return polylines


####################################################################################################
# @get_polyline_samples_from_segment
####################################################################################################
def get_polyline_samples_from_segment(sample_1,
                                      sample_2):
    # Construct the samples list
    samples = list()
    samples.append([(sample_1.point[0], sample_1.point[1], sample_1.point[2], 1), sample_1.radius])
    samples.append([(sample_2.point[0], sample_2.point[1], sample_2.point[2], 1), sample_2.radius])

    # Return the reconstructed list
    return samples


####################################################################################################
# @get_segments_poly_lines
####################################################################################################
def get_segments_poly_lines(section,
                            transform=None):
    """Get a list of poly-lines that reflect the segments of a single section.

    :param section:
        The geometry of a section.
    :param transform:
        Transform the points from local to circuit coordinates, only valid for a circuit.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # A list of all the poly-lines of all the segments that are found in the given section
    segments_polylines = list()

    for i in range(len(section.samples) - 1):

        # An array containing the data of the segment arranged in blender poly-line format
        segment_polyline = list()

        # Global coordinates transformation, use I if no transform is given
        if transform is None:
            transform = Matrix()

        # Get the coordinates of the sample
        # point_0 = transform * section.samples[i].point
        # point_1 = transform * section.samples[i + 1].point

        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Use the actual radius of the samples reported in the morphology file
        segment_polyline.append([(point_0[0], point_0[1], point_0[2], 1),
                                 section.samples[i].radius])
        segment_polyline.append([(point_1[0], point_1[1], point_1[2], 1),
                                 section.samples[i + 1].radius])

        # Append the segment poly-line data to this final list
        segments_polylines.append(segment_polyline)

    # Return the segments poly-lines list
    return segments_polylines


####################################################################################################
# @get_section_poly_line
####################################################################################################
def get_section_poly_line(section,
                          transform=None):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param transform:
        Transform the points from local to circuit coordinates, only valid for a circuit.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = list()

    # Global coordinates transformation, use I if no transform is given
    if transform is None:
        transform = Matrix()

    # Construct the section from all the samples
    for i in range(len(section.samples)):

        # Get the coordinates of the sample
        # point = transform * section.samples[i].point

        point = section.samples[i].point

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), section.samples[i].radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_section_polyline_without_terminal_samples
####################################################################################################
def get_section_polyline_without_terminal_samples(section):
    """Get the polyline list or a series of points that reflects the skeleton of a single section
    without its terminal samples.

    :param section:
        The geometry of a section.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    polyline = list()

    # Resample the section (ADAPTIVE-RELAXED)
    nmv.skeleton.ops.resample_section_adaptively_relaxed(section=section)

    # If the section has only three samples or less, we cannot construct a polyline here
    if len(section.samples) < 10:
        return None

    # Construct the section from the remaining samples
    for i in range(3, len(section.samples) - 3):

        # Get a reference to the point
        point = section.samples[i].point

        # Use the actual radius of the samples reported in the morphology file
        polyline.append([(point[0], point[1], point[2], 1), section.samples[i].radius])

    # Return the polyline 'list'
    return polyline


####################################################################################################
# @connect_root_to_origin
####################################################################################################
def connect_root_to_origin(section,
                           poly_line):
    """Connect the roots of the connected arbors to the soma by adiing few samples till
    reaching the origin.

    :param section:
        A given section to connect to the soma.
    :param poly_line:
        The polyline list used to collect the samples.
    """

    # Get the direction from the origin to the first sample of the section
    direction = section.samples[0].point.normalized()

    # Get the distance from the origin to the first sample of the section
    distance = section.samples[0].point.length

    # Number of samples required to connect the origin to the soma to the first sample
    number_samples = int(distance / 5.0)

    # Add the 'auxiliary' samples to the poly-line and use the same radius of the first
    # sample on the section
    for i in range(0, number_samples):
        point = Vector((0.0, 0.0, 0.0)) + (i * direction)
        poly_line.append([(point[0], point[1], point[2], 1), section.samples[0].radius])


####################################################################################################
# @get_connected_poly_line
####################################################################################################
def get_connected_poly_line(section,
                            connection_to_soma=nmv.enums.Skeleton.Roots.ALL_DISCONNECTED,
                            transform=None):
    """Get the poly-line list or a series of points that reflect a connected stream passing by
    the given section. This function is different from the @get_section_poly_line one as it ignore
    the duplicated points along the arbor at the beginning and end of the section.

    :param section:
        The geometry of a section.
    :param connection_to_soma:
        A flag that indicates that this section is a root and is connected to the origin.
        If this flag is activated, we will add few more samples between the origin and the first
        sample on the section to the returned poly-line.
        By default, this flag is set to False.
    :param transform:
        Transform the points from local to circuit coordinates, only valid for a circuit.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = list()

    # Global coordinates transformation, use I if no transform is given
    if transform is None:
        transform = Matrix()

    first_sample_index = 0
    last_sample_index = len(section.samples)

    # If this section is a ROOT and is requested by the user to be connected to the origin,
    # add few extra samples from the origin to the first sample of the given root section
    if section.is_root():

        # All connected
        if connection_to_soma == nmv.enums.Skeleton.Roots.ALL_CONNECTED:
            connect_root_to_origin(section=section, poly_line=poly_line)

        # Only connect the arbors connected to the soma to the origin
        elif connection_to_soma == nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN:

            if not section.far_from_soma:
                connect_root_to_origin(section=section, poly_line=poly_line)
        else:
            pass

    # Construct the section
    for i in range(first_sample_index, last_sample_index):

        # Get the coordinates of the sample
        # point = transform * section.samples[i].point

        point = section.samples[i].point

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), section.samples[i].radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_arbor_poly_lines_as_connected_sections
####################################################################################################
def get_arbor_poly_lines_as_connected_sections(root,
                                               poly_lines_data=[],
                                               poly_line_data=[],
                                               branching_order=0,
                                               connection_to_soma=nmv.enums.Skeleton.Roots.ALL_DISCONNECTED,
                                               max_branching_order=nmv.consts.Math.INFINITY):
    """

    :param root:
    :param poly_lines_data:
    :param poly_line_data:
    :param branching_order:
    :param connection_to_soma:
    :param max_branching_order:
    :return:
    """

    # Ignore the drawing if the section is None
    if root is None:
        return

    # Increment the branching level
    branching_order += 1

    # Get a list of all the poly-line that corresponds to the given section
    section_poly_line = get_connected_poly_line(section=root, connection_to_soma=connection_to_soma)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_poly_line)

    # If the section does not have any children, then draw the section and clean the list
    if not root.has_children() or branching_order >= max_branching_order:

        # Polyline name
        poly_line_name = root.label

        # Construct the poly-line
        import nmv.geometry
        poly_line = nmv.geometry.PolyLine(
            name='%s_%d' % (poly_line_name, branching_order),
            samples=copy.deepcopy(poly_line_data),
            material_index=root.get_material_index() + (branching_order % 2))

        # Append the polyline to the list, and copy the data before clearing the list
        poly_lines_data.append(poly_line)

        # Clean @poly_line_data to collect the data from the remaining sections
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for i, child in enumerate(root.children):
        get_arbor_poly_lines_as_connected_sections(
            root=child, poly_lines_data=poly_lines_data, poly_line_data=poly_line_data,
            branching_order=branching_order, max_branching_order=max_branching_order)


####################################################################################################
# @get_soma_connection_poly_line_
####################################################################################################
def get_soma_connection_poly_line_(section):
    """Get an extra poly-line that accounts for the connection between the root section and soma.

    This poly-line is NOT described in the morphology file, but it is added to make a smooth
    connection to the soma.
    NOTE: This function assumes that the morphology has been pre-processed to label the arbors
    that are connected to the soma, otherwise the polyline created by this function is NOT true.

    :param section:
        Section structure.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the poly-line data of the section compatible with Blender
    poly_line = list()

    # The section must be PHYSICALLY connected to the soma after the filtration
    if section.connected_to_soma:

        # Add a sample around the origin
        direction = section.samples[0].point.normalized()

        # Sample radius
        radius = section.samples[0].radius

        # Sample point
        point = section.samples[0].point

        # Get the starting point of the bridging section
        point = point - nmv.consts.Skeleton.ARBOR_EXTRUSION_DELTA * direction

        # Append the sample to the list
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_soma_connection_poly_line
####################################################################################################
def get_origin_connection_poly_line(section,
                                    ignore_physical_connectivity=False):
    """Get an extra poly-line that accounts for the connection between the root section and soma
    origin.

    This poly-line is NOT described in the morphology file, but it is added to account for
    connecting the soma to the root sections. It is only used for creating a piecewise watertight
    mesh that can be used for voxelization.

    :param section:
        Section structure.
    :param ignore_physical_connectivity:
        Connect the arbors to the origin even if they are not connected to the soma physically.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the poly-line data of the section compatible with Blender
    poly_line = list()

    # The section must be PHYSICALLY connected to the soma after the filtration
    if section.connected_to_soma or ignore_physical_connectivity:

        # Add a sample around the origin
        direction = section.samples[0].point.normalized()

        # The initial sample must be far from the origin by one micron
        initial_sample = Vector((0, 0, 0)) + (1.0 * direction)

        # Sample radius
        radius = section.samples[0].radius

        # Compute the distance between the first sample and the origin sample
        distance = (section.samples[0].point - direction).length

        # Add few samples between the origin and the first sample of the root section
        for i in range(1, nmv.consts.Skeleton.N_SAMPLES_ROOT_TO_ORIGIN):

            # Compute the sample distance
            sample_distance = distance * (i / nmv.consts.Skeleton.N_SAMPLES_ROOT_TO_ORIGIN)

            # Sample point
            point = initial_sample + (direction * sample_distance)

            # Append the point to the poly-line data
            poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_stem_section_polyline
####################################################################################################
def get_stem_section_polyline(section,
                              ignore_branching_samples=False):
    """Get the poly-line representing a stem section that is neither root, nor last.

    :param section:
        Section structure.
    :param ignore_branching_samples:
        Ignore the first sample of the section, or the branching sample. False by default.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the poly-line data of the section compatible with Blender
    poly_line = list()

    # Get the starting sample index
    starting_sample_index = 1 if ignore_branching_samples else 0

    # Get the ending sample index
    ending_sampling_index = 2 if ignore_branching_samples else 1

    # Normal processing of the intermediate samples (ignore first sample only)
    for i in range(starting_sample_index, len(section.samples) - ending_sampling_index):

        # Sample coordinates
        point = section.samples[i].point

        # Sample radius
        radius = section.samples[i].radius

        # Append the sample to the list
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_last_section_polyline
####################################################################################################
def get_last_section_polyline(section,
                              ignore_branching_samples=False,
                              process_section_terminals=False):
    """Get the poly-line representing a last section.

    :param section:
        Section structure.
    :param ignore_branching_samples:
        Ignore the first sample of the section, or the branching sample. False by default.
    :param process_section_terminals:
        Process the last samples of the section to make them look smooth. False by default.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the poly-line data of the section compatible with Blender
    poly_line = list()

    # Get the starting sample index
    starting_sample_index = 1 if ignore_branching_samples else 0

    # Normal processing of the intermediate samples (ignore first and last)
    for i in range(starting_sample_index, len(section.samples) - 1):

        # Sample coordinates
        point = section.samples[i].point

        # Sample radius
        radius = section.samples[i].radius

        # Append the sample to the list
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Last sample coordinates
    point = section.samples[-1].point

    # Last sample radius
    if process_section_terminals:
        radius = nmv.consts.Morphology.LAST_SAMPLE_RADIUS
    else:
        radius = section.samples[-1].radius

    # Append the last sample to the list
    poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_last_section_polyline
####################################################################################################
def get_connected_sections_poly_line(section,
                                     roots_connection,
                                     is_continuous=False,
                                     is_last_section=False,
                                     ignore_branching_samples=False,
                                     process_section_terminals=False):
    """Get the poly-line list or a series of points that reflect the skeleton of a group of
    connected sections along a single arbor.

    :param section:
        The geometry of the section.
    :param roots_connection:
        How to root sections will be connected to the soma.
    :param is_continuous:
        Is this section a continuation from a previous one or not.
    :param is_last_section:
        Is this section the last one along an arbor or not.
    :param ignore_branching_samples:
        Ignore adding the samples at the branching points.
        This feature is mainly added for extrusion-based meshing.
    :param process_section_terminals:
        Process the terminal samples that would reduce the visual quality of the arbor.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the poly-line data of the section compatible with Blender
    poly_line = list()

    # Root section
    if section.is_root():

        # If the root section is connected to the soma (soma bridging)
        if roots_connection == nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_SOMA:
            poly_line.extend(get_soma_connection_poly_line_(section=section))

        # All connected
        elif roots_connection == nmv.enums.Skeleton.Roots.ALL_CONNECTED:
            connect_root_to_origin(section=section, poly_line=poly_line)

        # Only connect the arbors connected to the soma to the origin
        elif roots_connection == nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN:
            if not section.far_from_soma:
                connect_root_to_origin(section=section, poly_line=poly_line)
        else:
            pass

        # If the root section is the last section
        if is_last_section:

            # Get the samples and process the last sample to close the edge
            poly_line.extend(get_last_section_polyline(
                section=section, ignore_branching_samples=ignore_branching_samples,
                process_section_terminals=process_section_terminals))

        # The root section is branching to another section
        else:

            # Get the samples without any processing
            poly_line.extend(get_stem_section_polyline(
                section=section, ignore_branching_samples=ignore_branching_samples))

    # Non-root section
    else:

        # If the section is a continuation, then do not pre-process the first samples
        if is_continuous:

            # If this is the last section
            if is_last_section:

                # Get the samples and process the last sample to close the edge
                poly_line.extend(get_last_section_polyline(
                    section=section, ignore_branching_samples=ignore_branching_samples,
                    process_section_terminals=process_section_terminals))

            # A stem section
            else:  # is_last_section

                # Normal processing for the internal sections
                poly_line.extend(get_stem_section_polyline(
                    section=section, ignore_branching_samples=ignore_branching_samples))

        # This 'secondary' section is not a continuation from a previous section, it is new
        else:  # is_continuous

            # If this is the last section
            if is_last_section:

                # Get the samples and process the last sample to close the edge
                poly_line.extend(get_last_section_polyline(
                    section=section, ignore_branching_samples=ignore_branching_samples,
                    process_section_terminals=process_section_terminals))

            # A stem section
            else:  # is_last_section

                # Normal processing for the internal sections
                poly_line.extend(get_stem_section_polyline(
                    section=section, ignore_branching_samples=ignore_branching_samples))

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_poly_line_length
####################################################################################################
def get_poly_line_length(poly_line):
    """Return the total length of a poly-line.
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
    """Return what's called the 'bevel_factor_start' factor that will be used to draw the poly-line.

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
# @create_bvh
####################################################################################################
def create_bvh(scene_object):
    """Creates the BVH of a given scene object.

    :param scene_object:
        A given scene object.
    :return:
        A reference to the BVH
    """

    bm = bmesh.new()
    bm.from_mesh(scene_object.data)
    bm.transform(scene_object.matrix_world)
    object_bvh = BVHTree.FromBMesh(bm)
    bm.free()

    return object_bvh


####################################################################################################
# @are_intersecting
####################################################################################################
def are_intersecting(objects):
    """If the list of objects are intersecting.

    :param objects:
        A given list of objects to check their intersection
    :return:
    """

    # Check every object for intersection with every other object
    i = 0
    intersections = 0

    # Check for a primary one
    for primary in objects:

        # Create a BVH
        primary_bvh = create_bvh(primary)

        # Secondary
        for secondary in objects[i:]:
            if primary == secondary:
                continue

            # Create the BVH
            secondary_bvh = create_bvh(secondary)

            # Get intersecting pairs
            intersection_list = primary_bvh.overlap(secondary_bvh)

            # if list is empty, no objects are touching
            if len(intersection_list) > 0:
                intersections += 1

        i += 1
    if intersections > 0:
        return True
    return False


####################################################################################################
# @poly_lines_intersect
####################################################################################################
def poly_lines_intersect(poly_line_1,
                         poly_line_2):
    """Apply a poly-line intersection test on the given two poly-lines and return True if the two
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
    poly_line_1_duplicate = nmv.scene.ops.convert_object_to_mesh(poly_line_1_duplicate)
    poly_line_2_duplicate = nmv.scene.ops.convert_object_to_mesh(poly_line_2_duplicate)
    
    # Deselect all the object s
    nmv.scene.deselect_all()
    
    # Select the specific ones 
    nmv.scene.select_objects([poly_line_1_duplicate, poly_line_2_duplicate])

    # Are those objects intersecting
    value = are_intersecting(bpy.context.selected_objects)

    # Delete the duplicated objects
    nmv.scene.ops.delete_list_objects([poly_line_1_duplicate, poly_line_2_duplicate])

    # Return the value
    return value


####################################################################################################
# @poly_lines_intersect
####################################################################################################
def poly_line_intersect_mesh(poly_line,
                             mesh):
    """Apply a poly-line intersection test on the given poly-line and mesh and return True if they
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


####################################################################################################
# @skin_section_into_mesh
####################################################################################################
def skin_section_into_mesh(section, smoothing_level=1):
    """Skins a given section into a mesh geometry.

    :param section:
        A given section to skin using the Skinning modifier.
    :param smoothing_level:
        The smoothing factor given to create nicer meshes.
    :return:
        A mesh object reconstructed from skinning the given section.
    """

    copy.deepcopy(section)

    # Create the initial vertex of the section skeleton at the section starting point
    section_bmesh_object = nmv.bmeshi.create_vertex(location=section.samples[0].point)

    # Extrude the section segment by segment
    for i in range(len(section.samples) - 1):
        nmv.bmeshi.ops.extrude_vertex_towards_point(
            section_bmesh_object, section.samples[i].arbor_idx, section.samples[i + 1].point)

    # Construct a mesh base, or a proxy mesh
    section_mesh = nmv.bmeshi.convert_bmesh_to_mesh(section_bmesh_object, str(section.index))

    section_mesh.modifiers.new(name="Skin", type='SKIN')

    # Activate the arbor mesh
    nmv.scene.set_active_object(section_mesh)

    # Update the radii across the skeleton
    for i in range(0, len(section.samples)):

        # Get the sample radius
        radius = section.samples[i].radius

        # Get a reference to the vertex
        vertex = section_mesh.data.skin_vertices[0].data[i]

        # Update the radius of the vertex
        vertex.radius = radius, radius

    # Apply the operator
    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Skin")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")

    nmv.mesh.smooth_object(mesh_object=section_mesh, level=smoothing_level)

    # Return a reference to the section mesh
    return section_mesh
