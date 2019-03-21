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
import os, sys, copy, random, math, numpy

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import nmv
import nmv.bmeshi
import nmv.enums
import nmv.consts
import nmv.geometry
import nmv.mesh
import nmv.skeleton

# A global variable for the recursive progressive rendering, 0 is left for the soma
progressive_frame_index = 1


####################################################################################################
# @draw_section_from_poly_line_data
####################################################################################################
def draw_section_from_poly_line_data(data,
                                     name,
                                     material=None,
                                     color=None,
                                     bevel_object=None,
                                     caps=False):
    """Draw a morphological section as a poly-line (or tube) object and returns a reference to it.

    :param data:
        Section data in poly-line format.
    :param name:
        The name of the section object in the scene, for referencing.
    :param material:
        Section material.
    :param color:
        Section color.
    :param bevel_object:
        A given bevel object to scale the section.
    :param caps:
        A flag to close the caps of the section sides or keep them open.
    :return:
        A reference to the drawn section.
    """

    # If the data list has less than two samples, then report the error
    if len(data) < 2:
        nmv.logger.log('\t\t* ERROR: Drawn section [%s] has less than two samples' % name)

    # Append a '_section' keyword after the section name to be able to recognize it later
    section_name = '%s_section' % name

    # Draw the section from the given data in poly-line format
    section_object = nmv.geometry.draw_poly_line(poly_line_data=data, name=section_name,
        material=material, color=color, bevel_object=bevel_object, caps=caps)

    # Return a reference to the drawn section object
    return section_object


####################################################################################################
# @extrude_section_from_poly_line_data
####################################################################################################
def extrude_section_from_poly_line_data(data,
                                        name,
                                        bmesh_base):
    """

    :param data:
    :param name:
    :param bmesh_base:
    :return:
    """
    point = Vector((data[1][0][0], data[1][0][1], data[1][0][2]))
    face_index = nmv.bmeshi.ops.get_nearest_face_index(bmesh_base, point)

    point = Vector((data[1][0][0], data[1][0][1], data[1][0][2]))
    radius = data[1][1]

    face_index = nmv.bmeshi.ops.extrude_face_to_point(bmesh_base, face_index, point)

    # set face radius
    nmv.bmeshi.ops.set_face_radius(bmesh_base, face_index, radius)

    for i in range(2, len(data)):
        point = Vector((data[i][0][0], data[i][0][1], data[i][0][2]))
        radius = data[i][1]

        face_index = nmv.bmeshi.ops.extrude_face_to_point(bmesh_base, face_index, point)
        #nmv.bmeshi.ops.scale_face(bmesh_base, face_index, radius * math.sqrt(2))

        # set face radius
        # nmv.bmeshi.ops.set_face_radius(bmesh_base, face_index, radius)

    return bmesh_base


####################################################################################################
# @draw_connected_sections
####################################################################################################
def extrude_connected_sections(section,
                               name,
                               section_objects,
                               poly_line_data=[],
                               secondary_sections=[],
                               branching_level=0,
                               max_branching_level=nmv.consts.Math.INFINITY,
                               material_list=None,
                               bevel_object=None,
                               fixed_radius=None,
                               transform=None,
                               repair_morphology=False,
                               caps=False,
                               render_frame=False,
                               frame_destination=None,
                               camera=None,
                               roots_connection=nmv.enums.Arbors.Roots.CONNECTED_TO_SOMA):
    """Draw a list of sections connected together as a poly-line.

    :param section:
        Section root.
    :param poly_line_data:
        A list of lists containing the data of the poly-line format.
    :param bmesh_base:
        A bmesh base object that will get extruded and extruded until the construction of the
        full branch.
    :param secondary_sections:
        A list of the secondary sections along the arbor.
    :param branching_level:
        Current branching level.
    :param max_branching_level:
        Maximum branching level the section can grow up to, infinity.
    :param name:
        Section name.
    :param material_list:
        A list of materials for random coloring of the section.
    :param bevel_object:
        A given bevel object to scale the section.
    :param fixed_radius:
        A fixed radius for each sample in the section, or None.
    :param transform:
        Transform from local and circuit coordinates.
    :param repair_morphology:
        Apply some filters to repair the morphology during the poly-line construction.
    :param caps:
        A flag to close the section caps or not.
    :param render_frame:
        A flag to render a progressive frame.
    :param frame_destination:
        The directory where the frame will be dumped.
    :param camera:
        A given camera to render the frame.
    :param connect_to_soma:
        Connect the section to the soma origin, False by default.
    :param bridge_to_soma:
        Bridge the root section to the soma.
    """

    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_level += 1

    # Verify if this is the last section along the arbor or not
    is_last_section = False
    if branching_level >= max_branching_level or not section.has_children():
        is_last_section = True

    # Verify if this a continuous section or not
    is_continuous = True
    if len(poly_line_data) == 0:
        is_continuous = False
        secondary_sections.append(section)

    # Get a list of all the poly-line that corresponds to the given section
    section_data = nmv.skeleton.ops.get_connected_sections_poly_line(
        section=section, roots_connection=roots_connection, is_continuous=is_continuous,
        is_last_section=is_last_section,
        process_section_terminals=repair_morphology)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_data)

    # If the section does not have any children, then draw the section and clean the
    # poly_line_data list
    if not section.has_children() or branching_level >= max_branching_level:

        # Section material
        section_material = None
        if material_list is not None:
            if section.id % 2 == 0:
                section_material = material_list[0]
            else:
                section_material = material_list[1]

        # Section name
        section_name = '%s_%d' % (name, section.id)

        base_mesh = section_objects[0]
        # Draw the extruded section and return a reference to it
        base_mesh = extrude_section_from_poly_line_data(data=poly_line_data, name=section_name,
            bmesh_base=base_mesh)

        section_objects[0] = base_mesh

        # Draw the section
        #section_object = draw_section_from_poly_line_data(
        #    data=poly_line_data, name=section_name, material=section_material,
        #    bevel_object=bevel_object, caps=caps)

        # Add the section object to the sections_objects list
        #sections_objects.append(section_object)

        # Clean the polyline samples list
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        # Draw the children sections
        extrude_connected_sections(
            section=child,
            name=name,
            section_objects=section_objects,
            poly_line_data=poly_line_data,
            secondary_sections=secondary_sections,
            branching_level=branching_level,
            max_branching_level=max_branching_level,
            material_list=material_list,
            bevel_object=bevel_object,
            fixed_radius=fixed_radius,
            transform=transform,
            repair_morphology=repair_morphology,
            caps=caps,
            render_frame=render_frame,
            frame_destination=frame_destination,
            camera=camera,
            roots_connection=roots_connection)


def get_connected_sections_poly_line_recursively(section,
                                                 poly_lines_data=[],
                                                 poly_line_data=[],
                                                 branching_level=0,
                                                 max_branching_level=nmv.consts.Math.INFINITY):
    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_level += 1

    # Get a list of all the poly-line that corresponds to the given section
    section_poly_line = nmv.skeleton.ops.get_section_poly_line(section=section)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_poly_line)

    # If the section does not have any children, then draw the section and clean the list
    if not section.has_children() or branching_level >= max_branching_level:

        # Polyline name
        poly_line_name = '%s_%d' % (section.get_type_prefix(), section.id)

        # Append the polyline to the list, and copy the data before clearing the list
        poly_lines_data.append([copy.deepcopy(poly_line_data), poly_line_name])

        # Clean @poly_line_data to collect the data from the remaining sections
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        get_connected_sections_poly_line_recursively(
            section=child, poly_lines_data=poly_lines_data, poly_line_data=poly_line_data,
            branching_level=branching_level, max_branching_level=max_branching_level)


def draw_connected_sections_poly_lines(arbor,
                                       bevel_object,
                                       caps=True,
                                       max_branching_level=nmv.consts.Math.INFINITY):

    # A list that will contain all the poly-lines gathered from traversing the arbor tree with
    # depth-first traversal
    poly_lines_data = list()

    # Construct the poly-lines
    get_connected_sections_poly_line_recursively(
        section=arbor, poly_lines_data=poly_lines_data, max_branching_level=max_branching_level)

    # A list that will contain all the drawn poly-lines to be able to access them later, although
    # we can access them by name
    poly_lines_objects = list()

    # For each poly-line in the list, draw it
    for i, poly_line_data in enumerate(poly_lines_data):

        # Draw the section, and append the result to the objects list
        poly_lines_objects.append(draw_section_from_poly_line_data(
            data=poly_line_data[0], name=poly_line_data[1], bevel_object=bevel_object, caps=caps))

    # Return the list
    return poly_lines_objects


####################################################################################################
# @draw_connected_sections
####################################################################################################
def draw_connected_sections(section, name,
                            poly_line_data=[],
                            sections_objects=[],
                            secondary_sections=[],
                            branching_level=0,
                            max_branching_level=nmv.consts.Math.INFINITY,
                            material_list=None,
                            bevel_object=None,
                            fixed_radius=None,
                            transform=None,
                            repair_morphology=False,
                            caps=False,
                            render_frame=False,
                            frame_destination=None,
                            camera=None,
                            ignore_branching_samples=False,
                            roots_connection=nmv.enums.Arbors.Roots.DISCONNECTED_FROM_SOMA):
    """Draw a list of sections connected together as a poly-line.

    :param section:
        Section root.
    :param poly_line_data:
        A list of lists containing the data of the poly-line format.
    :param sections_objects:
        A list that should contain all the drawn section objects.
    :param secondary_sections:
        A list of the secondary sections along the arbor.
    :param branching_level:
        Current branching level.
    :param max_branching_level:
        Maximum branching level the section can grow up to, infinity.
    :param name:
        Section name.
    :param material_list:
        A list of materials for random coloring of the section.
    :param bevel_object:
        A given bevel object to scale the section.
    :param fixed_radius:
        A fixed radius for each sample in the section, or None.
    :param transform:
        Transform from local and circuit coordinates.
    :param repair_morphology:
        Apply some filters to repair the morphology during the poly-line construction.
    :param caps:
        A flag to close the section caps or not.
    :param render_frame:
        A flag to render a progressive frame.
    :param frame_destination:
        The directory where the frame will be dumped.
    :param camera:
        A given camera to render the frame.
    :param ignore_branching_samples:
        Ignore fetching the branching samples from the morphology skeleton.
    :param roots_connection:
        How the root sections are connected to the soma.
    """

    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_level += 1

    # Verify if this is the last section along the arbor or not
    is_last_section = False
    if branching_level >= max_branching_level or not section.has_children():
        is_last_section = True

    # Verify if this a continuous section or not
    is_continuous = True
    if len(poly_line_data) == 0:
        is_continuous = False
        secondary_sections.append(section)

    # Get a list of all the poly-line that corresponds to the given section
    section_data = nmv.skeleton.ops.get_connected_sections_poly_line(
        section=section,
        roots_connection=roots_connection,
        is_continuous=is_continuous,
        is_last_section=is_last_section,
        ignore_branching_samples=ignore_branching_samples,
        process_section_terminals=repair_morphology)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_data)

    # If the section does not have any children, then draw the section and clean the
    # poly_line_data list
    if (not section.has_children()) or (branching_level >= max_branching_level):

        # Section material
        section_material = None
        if material_list is not None:
            if section.id % 2 == 0:
                section_material = material_list[0]
            else:
                section_material = material_list[1]

        # Section name
        section_name = '%s_%d' % (name, section.id)

        # Draw the section
        section_object = draw_section_from_poly_line_data(
            data=poly_line_data, name=section_name, material=section_material,
            bevel_object=bevel_object, caps=caps)

        # Render frame for progressive rendering
        if render_frame:

            global progressive_frame_index

            # The file path of the frame
            frame_file_path = '%s/frame_%s' % (
                frame_destination, '{0:05d}'.format(progressive_frame_index))

            # Render the image to film
            # camera_ops.render_scene_to_image(camera, frame_file_path)

            # Increment the progressive frame index
            progressive_frame_index += 1

        # Add the section object to the sections_objects list
        sections_objects.append(section_object)

        # Clean the polyline samples list
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        # Draw the children sections
        draw_connected_sections(
            section=child, name=name, poly_line_data=poly_line_data,
            sections_objects=sections_objects, secondary_sections=secondary_sections,
            branching_level=branching_level, max_branching_level=max_branching_level,
            material_list=material_list, bevel_object=bevel_object, fixed_radius=fixed_radius,
            transform=transform, repair_morphology=repair_morphology, caps=caps,
            render_frame=render_frame, frame_destination=frame_destination, camera=camera,
            roots_connection=roots_connection)


####################################################################################################
# @draw_disconnected_sections
####################################################################################################
def draw_disconnected_skeleton_sections(section,
                                        name,
                                        poly_line_data=[],
                                        sections_objects=[],
                                        secondary_sections=[],
                                        branching_level=0,
                                        max_branching_level=nmv.consts.Math.INFINITY,
                                        material_list=None,
                                        bevel_object=None,
                                        fixed_radius=None,
                                        transform=None,
                                        repair_morphology=False,
                                        caps=False,
                                        render_frame=False,
                                        frame_destination=None,
                                        camera=None,
                                        extend_to_soma_origin=True):
    """Draw a list of sections connected together as a poly-line, however, disconnected at the
    secondary branches.

    :param section:
        Section root.
    :param poly_line_data:
        A list of lists containing the data of the poly-line format.
    :param sections_objects:
        A list that should contain all the drawn section objects.
    :param secondary_sections:
        A list of the secondary sections along the arbor.
    :param branching_level:
        Current branching level.
    :param max_branching_level:
        Maximum branching level the section can grow up to, infinity.
    :param name:
        Section name.
    :param material_list:
        A list of materials for random coloring of the section.
    :param bevel_object:
        A given bevel object to scale the section.
    :param fixed_radius:
        A fixed radius for each sample in the section, or None.
    :param transform:
        Transform from local and circuit coordinates.
    :param repair_morphology:
        Apply some filters to repair the morphology during the poly-line construction.
    :param caps:
        A flag to close the section caps or not.
    :param render_frame:
        A flag to render a progressive frame.
    :param frame_destination:
        The directory where the frame will be dumped.
    :param camera:
        A given camera to render the frame.
    :param extend_to_soma_origin:
        If this flag is set to True, the first samples of the root arbors will be connected to the
        origin of the soma, because the arbor will not be 'physically' connected to the soma mesh.
        On the other hand, if this Flag is set to False, we will only add an auxiliary sample
        before the initial segment of the root section to allow BRIDGING the arbor to the soma
        later during the mesh reconstruction operation.
    """

    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_level += 1

    # Verify if this is the last section along the arbor or not
    is_last_section = False
    if branching_level >= max_branching_level or not section.has_children():
        is_last_section = True

    # Verify if this a continuous section or not
    is_continuous = True
    if len(poly_line_data) == 0:
        is_continuous = False
        secondary_sections.append(section)

    # Get a list of all the poly-line that corresponds to the given section
    section_data = nmv.skeleton.ops.get_disconnected_skeleton_sections_poly_line(
        section=section, is_continuous=is_continuous, is_last_section=is_last_section,
        fixed_radius=fixed_radius, transform=transform, process_terminals=repair_morphology,
        extend_to_soma_origin=extend_to_soma_origin)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_data)

    # If the section does not have any children, then draw the section and clean the
    # poly_line_data list
    if not section.has_children() or branching_level >= max_branching_level:

        # Section material
        section_material = None
        if material_list is not None:
            if section.id % 2 == 0:
                section_material = material_list[0]
            else:
                section_material = material_list[1]

        # Section name
        section_name = '%s_%d' % (name, section.id)

        # Draw the section
        section_object = draw_section_from_poly_line_data(
            data=poly_line_data, name=section_name, material=section_material,
            bevel_object=bevel_object, caps=caps)

        # Render frame for progressive rendering
        if render_frame:
            global progressive_frame_index

            # The file path of the frame
            frame_file_path = '%s/frame_%s' % (
                frame_destination, '{0:05d}'.format(progressive_frame_index))

            # Render the image to film
            # camera_ops.render_scene_to_image(camera, frame_file_path)

            # Increment the progressive frame index
            progressive_frame_index += 1

        # Add the section object to the sections_objects list
        sections_objects.append(section_object)

        # Clean the polyline samples list
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        # Draw the children sections
        draw_disconnected_skeleton_sections(
            section=child,
            name=name,
            poly_line_data=poly_line_data,
            sections_objects=sections_objects,
            secondary_sections=secondary_sections,
            branching_level=branching_level,
            max_branching_level=max_branching_level,
            material_list=material_list,
            bevel_object=bevel_object,
            fixed_radius=fixed_radius,
            transform=transform,
            repair_morphology=repair_morphology,
            caps=caps,
            render_frame=render_frame,
            frame_destination=frame_destination,
            camera=camera,
            extend_to_soma_origin=extend_to_soma_origin)


####################################################################################################
# @draw_section_as_disconnected_segments
####################################################################################################
def draw_disconnected_segments(section,
                               name,
                               material_list=None,
                               bevel_object=None,
                               fixed_radius=None,
                               transform=None,
                               render_frame=False,
                               frame_destination=None,
                               camera=None):
    """Draw a given morphological section as a series of disconnected segments, where each segment
    is represented by a unique cylinder.

    :param section:
        The geometry of a morphological section.
    :param name:
        The name of the section.
    :param material_list:
        A set of materials for alternating the colors of the segments.
    :param bevel_object:
        A given bevel object to scale the section.
    :param fixed_radius:
        A fixed radius for each sample in the section, or None.
    :param transform:
        Transform from local and circuit coordinates.
    :param render_frame:
        A flag to render a progressive frame.
    :param frame_destination:
        The directory where the frame will be dumped.
    :param camera:
        A given camera to render the frame.
    :return:
        A list of all the segments.
    """

    # A list of all the created segments in the section
    segments_objects = []

    # Get the poly-line format of the section
    section_data = nmv.skeleton.ops.get_section_poly_line(section=section, transform=transform)

    # Draw the section segment by segment
    for i in range(len(section_data) - 1):

        # Make a list of two points
        segment_data = [None] * 2
        segment_data[0] = section_data[i]
        segment_data[1] = section_data[i + 1]

        # Segment name
        # Append a '_segment' keyword after the section name to be able to recognize it later
        segment_name='%s_%d_segment' % (name, i)

        # Segment material
        segment_material = None
        if material_list is not None:
            if i % 2 == 0:
                segment_material = material_list[0]
            else:
                segment_material = material_list[1]

        # Draw the segment
        created_segments = nmv.geometry.ops.draw_poly_line(
            poly_line_data=segment_data, name=segment_name, material=segment_material,
            bevel_object=bevel_object)

        """
        # Render frame for progressive rendering
        if render_frame:
            global progressive_frame_index

            # The file path of the frame
            frame_file_path = '%s/frame_%s' % (
                frame_destination, '{0:05d}'.format(progressive_frame_index))

            # Render the image to film
            # camera_ops.render_scene_to_image(camera, frame_file_path)

            # Increment the progressive frame index
            progressive_frame_index += 1
        """

        # Add the created segments to the list
        segments_objects.append(created_segments)

    # Return a reference to the list that contains all the segments of the section
    return segments_objects


####################################################################################################
# @visualize_extrusion_connection
####################################################################################################
def visualize_extrusion_connection(point,
                                   radius,
                                   connection_id):
    """A utility function for the visual verification of the extrusion point. It adds a sphere with
    the same radius of the branch at the extrusion point along the connection between the soma and
    the branch.

    :param point:
        Connection spatial coordinates.
    :param radius:
        Connection radius.
    :param connection_id:
        Connection identifier or index.
    :return:
        A reference to the sphere created at the connection site.
    """

    # Create a connection sphere, as a bmesh object
    connection_sphere = nmv.mesh.create_uv_sphere(
        radius=radius, location=point, subdivisions=16, name=connection_id)

    # Return a reference to the connection sphere
    return connection_sphere
