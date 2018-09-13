####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
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

# System imports
import h5py

# Blender imports
import bpy
from mathutils import Vector

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.mesh
import neuromorphovis.scene


def draw_poly_line(poly_line_data,
                   format='SOLID',
                   name='poly_line',
                   material=None,
                   color=None,
                   bevel_object=None,
                   caps=True):
    """Draw a poly line (connected segments of lines) with multiple formats.

    :param poly_line_data:
        The data of the poly-line such as its points and radii.
    :param format:
        The format can be SIMPLE or SOLID.
    :param name:
        The name of the line.
    :param material:
        The material of the line.
    :param color:
        The color of the poly-line.
    :param bevel_object:
        A given bevel object that would scale the diameter of the poly-line.
    :param caps:
        A flag to indicate the line terminals are filled with caps or not.
    :return:
        A reference to the line object.
    """

    # Setup line data
    line_data = bpy.data.curves.new(name=name, type='CURVE')

    # The line is drawn in 3D
    line_data.dimensions = '3D'

    # Fill the line
    line_data.fill_mode = 'FULL'

    # Setup the spatial data of a SOLID line
    if format == 'SOLID':

        # The thickness of the line should be by default set to 1.0. This value will be scaled later
        # at the two points of the line.
        line_data.bevel_depth = 1.0

        # Adjust the texture coordinates of the poly-line.
        line_data.use_auto_texspace = False
        line_data.texspace_size[0] = 5
        line_data.texspace_size[1] = 5
        line_data.texspace_size[2] = 5

        # If a bevel object is given, use it for scaling the diameter of the poly-line
        if bevel_object is not None:
            line_data.bevel_object = bevel_object
            line_data.use_fill_caps = caps

    # Setup the spatial data of a SIMPLE line
    else:

        # The thickness of medium line can be set to 0.1
        line_data.bevel_depth = 0.1

    # If a material is given, then use it directly
    if material is not None:
        # Assign it directly to the line data
        line_data.materials.append(material)

    # Otherwise, check if a color is given.
    else:

        # Create a material from a given color
        if color is not None:
            # Create a new material (color) and assign it to the line
            line_material = bpy.data.materials.new('color.%s' % name)
            line_material.diffuse_color = color
            line_data.materials.append(line_material)

    # Add the points along the poly-line
    # NOTE: add n-1 points to the array, becuase once the poly-line is created it has already one
    # point added.
    # Options: ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS']
    poly_line_strip = line_data.splines.new('POLY')
    poly_line_strip.points.add(len(poly_line_data) - 1)

    # Add the points (or the samples) and their radii to the poly-line curve
    for i, point in enumerate(poly_line_data):
        poly_line_strip.points[i].co = point[0]
        poly_line_strip.points[i].radius = point[1]

    # Create a curve that uses the curve_data.
    line_strip = bpy.data.objects.new(str(name), line_data)

    # Link this curve to the scene
    bpy.context.scene.objects.link(line_strip)

    # Assume that the location of the line is set at the origin until further notice
    line_strip.location = Vector((0, 0, 0))

    # Return a reference to it
    return line_strip


def draw_section(section, bevel_object):
    # Construct a polyline list
    poly_line = list()

    # For each sample in the section, append it to the poly-line list
    for sample in section.samples_list:
        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius])

    # Draw the polyline
    draw_poly_line(poly_line_data=poly_line, bevel_object=bevel_object)


nmv.scene.ops.clear_scene()

morphology_file = '/data/morphologies/vasculature/vasculature-datas-set-2.h5'

# Read the h5 file using the python module into a data array
data = h5py.File(morphology_file, 'r')

# A list of all the samples in the data set
raw_samples_list = data['points'].value

# A list of all the edges or 'segments' in the data set
raw_segments_list = data['edges'].value

# A list of all the sections (called structures) in the data set
raw_sections_list = data['chains']['structure'].value

# A list of all the connections between the different sections in the data set
raw_connectivity_list = data['chains']['connectivity'].value

# A structural linear list of all the sections in the data set
sections_list = list()

print('Preparing the sections')

# Parse the data set
for i_section in range(len(raw_sections_list) - 1):

    # The index of the first segment (or edge) along the section
    starting_segment_index = raw_sections_list[i_section]

    # The index of the last segment (or edge) along the section
    ending_segment_index = raw_sections_list[i_section + 1]

    # A list that has all the samples of the section
    section_samples_list = list()

    # Get the samples along the section
    for i_segment in range(starting_segment_index, ending_segment_index):
        # The index of the first sample
        first_sample_index = raw_segments_list[i_segment][0]

        # The coordinates of the first sample
        first_sample_x = raw_samples_list[first_sample_index][0]
        first_sample_y = raw_samples_list[first_sample_index][1]
        first_sample_z = raw_samples_list[first_sample_index][2]

        # The cartesian coordinates of the sample
        first_sample_point = Vector((first_sample_x, first_sample_y, first_sample_z))

        # The radius of the first sample
        first_sample_radius = raw_samples_list[first_sample_index][3]

        # Construct a new sample
        first_sample = Sample(first_sample_index, first_sample_point, first_sample_radius)

        # Add the sample to the samples list
        section_samples_list.append(first_sample)

        """
        # Add the last sample at the end of the section
        if i_segment == ending_segment_index:

            # The index of the last sample
            last_sample_index = raw_segments_list[i_segment][1]

            # The coordinates of the last sample
            last_sample_x = raw_samples_list[last_sample_index][0]
            last_sample_y = raw_samples_list[last_sample_index][1]
            last_sample_z = raw_samples_list[last_sample_index][2]

            # The cartesian coordinates of the sample
            last_sample_point = Vector((last_sample_x, last_sample_y, last_sample_z))

            # The radius of the first sample
            last_sample_radius = raw_samples_list[last_sample_index][3]

            # Construct a new sample
            last_sample = Sample(last_sample_index, last_sample_point, last_sample_radius)

            # Add the sample to the samples list
            section_samples_list.append(last_sample)
        """

    # Construct a section
    section = Section(i_section, section_samples_list)

    # Add the section to the sections list
    sections_list.append(section)

print('Connecting the sections')

for i_connection in range(len(raw_connectivity_list)):
    parent_index = raw_connectivity_list[i_connection][0]
    child_index = raw_connectivity_list[i_connection][1]

    # Add the child
    sections_list[parent_index].children.append(sections_list[child_index])

    if sections_list[child_index].parent is None:
        sections_list[child_index].parent = sections_list[parent_index]

print('Done parsing the morphology .. Drawing ..')

bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=8, name='bevel')

for i, section in enumerate(sections_list):

    if i > 100:
        break

    print('%d/%d' % (i, len(sections_list)))

    draw_section(section, bevel_object)

print('Done drawing morphology ..')







