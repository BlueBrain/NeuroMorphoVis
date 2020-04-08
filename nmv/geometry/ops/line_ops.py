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

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal modules
import nmv.scene
import nmv.geometry


####################################################################################################
# @compute_section_centroid_from_poly_line_data
####################################################################################################
def compute_section_centroid_from_poly_line_data(poly_line_data):
    """Compute the centroid of a series of points given in the format of a poly-line data.

    :param poly_line_data:
        Section data in poly-line format.
    :return:
        The centroid of all the given points.
    """

    # Data centroid
    centroid = Vector((0, 0, 0))

    # Add the weights
    for point in poly_line_data:

        # Get the section center
        section_center = Vector((point[0][0], point[0][1], point[0][2]))

        # Add the weight
        centroid += section_center

    # Normalize
    centroid /= len(poly_line_data)

    # Return the centroid
    return centroid


####################################################################################################
# @create_poly_lines_object_base
####################################################################################################
def create_poly_lines_object_base(name='poly_lines',
                                  bevel_object=None,
                                  materials_list=None,
                                  caps=True,
                                  texture_size=5.0):
    """Creates an empty object that can be used to append multiple poly-lines and draw them in a
    single step very efficiently.

    NOTE: The poly-lines will be added later to the resulting object, this is just the base object.

    :param name:
        Poly-line object name.
    :param bevel_object:
        A given bevel object used to solidify the poly-line.
    :param materials_list:
        A list of all the skeleton materials.
    :param caps:
        A flag indicating whether the caps will be closed or open.
    :param texture_size:
        The size of the bump map of the assigned texture.
    :return:
        A reference to the created poly-lines object.
    """
    # Create the object as a new curve
    poly_lines_object = bpy.data.curves.new(name=name, type='CURVE')

    # The line is drawn in 3D
    poly_lines_object.dimensions = '3D'

    # Fill the line
    poly_lines_object.fill_mode = 'FULL'

    # The thickness of the line should be by default set to 1.0. This value will be scaled later
    # at the two points of the line.
    poly_lines_object.bevel_depth = 1.0

    # Adjust the texture coordinates of the poly-line
    # NOTE: The value 5 has been chosen after trial-and-error
    poly_lines_object.use_auto_texspace = False
    poly_lines_object.texspace_size[0] = texture_size
    poly_lines_object.texspace_size[1] = texture_size
    poly_lines_object.texspace_size[2] = texture_size

    # Use caps if requested
    poly_lines_object.use_fill_caps = caps

    # If a bevel object is given, use it for scaling the diameter of the poly-line
    if bevel_object is not None:
        poly_lines_object.bevel_object = bevel_object

    # If a list of materials is given, then append it to the skeleton object
    if materials_list is not None:
        for material in materials_list:
            poly_lines_object.materials.append(material)

    # Return a reference to the created object
    return poly_lines_object


####################################################################################################
# @append_poly_line_to_base_object
####################################################################################################
def append_poly_line_to_base_object(base_object,
                                    poly_line,
                                    poly_line_type='POLY'):
    """Creates a poly-line object and appends to the aggregate poly-lines-object that is created
    before.

    :param base_object:
        A previously created poly-lines object where we going to append a new poly-line object
        constructed from the given poly_line_data.
    :param poly_line:
        The new poly-line data that will be used to create the new poly-line object that will be
        appended to the given base_object.
    :param poly_line_type:
        The type of the poly-line: ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS']
    """

    # Create a new poly-line object integrated into the base object
    poly_line_object = base_object.splines.new(poly_line_type)

    # Define the number of samples of the poly-line object
    # NOTE: Use n-1 points because once the poly-line is created it has already one point added

    poly_line_object.points.add(len(poly_line.samples) - 1)

    # Define the material for this poly-line
    poly_line_object.material_index = poly_line.material_index

    # Add the points (or the samples) and their radii to the poly-line curve object
    for i, poly_line_sample in enumerate(poly_line.samples):

        # Sample coordinates
        poly_line_object.points[i].co = poly_line_sample[0]

        # Sample radius
        poly_line_object.points[i].radius = poly_line_sample[1]


####################################################################################################
# @draw_line
####################################################################################################
def draw_line(point1=Vector((0, 0, 0)),
              point2=Vector((1, 1, 1)),
              format='SOLID',
              thickness=1.0,
              material=None,
              color=None,
              name='line'):
    """Draws a line between two connected points in the space and returns a reference to it.
    NOTE: If you want to have a thin line, use 0.1 for the thickness and if you want to set it
    to scale, use 1.0.

    :param point1: Starting point of the line.
    :param point2: End point of the line.
    :param format: The format of the line, can be SIMPLE or SOLID.
    :param thickness: The thickness of the line (between 0.1 and 1.0).
    :param material: The material of the line.
    :param color: The color of the line, in case no material is given.
    :param name: The name of the line.
    :return: A reference to the create line.
    """

    # Setup line data
    # Create a curve object
    line_data = bpy.data.curves.new(name=name, type='CURVE')

    # The line is drawn in 3D
    line_data.dimensions = '3D'

    # Fill the line
    line_data.fill_mode = 'FULL'

    # Set the thickness of the line.
    line_data.bevel_depth = thickness

    # For a solid line, the caps are always filled in contrast to the thin line
    if format == 'SOLID':
        line_data.use_fill_caps = True

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

    # Create a line object and link it to the scene
    line_object = nmv.geometry.create_line_object_from_data(
        data=line_data, point1=point1, point2=point2, name=name)

    # Return a reference to the line object
    return line_object


####################################################################################################
# @draw_cone_line
####################################################################################################
def draw_cone_line(point1=Vector((0, 0, 0)),
                   point2=Vector((1, 1, 1)),
                   point1_radius=0.0,
                   point2_radius=1.0,
                   color=(1, 1, 1),
                   name='line',
                   smoothness_factor=1):
    """Draw a cone line between two points, with different radii at the beginning and the end of
    the line.

    :param point1:
        Starting point of the line.
    :param point2:
        End point of the line.
    :param point1_radius:
        The radius of the line at the starting point.
    :param point2_radius:
        The radius of the line at the end point.
    :param color:
        The color of the line
    :param name:
        The name of the line.
    :param smoothness_factor:
        Smoothing the created line (1 - 5), by default set to 1.
    :return:
        A reference to the create line.
    """

    # Setup line data
    # Create a curve object
    line_data = bpy.data.curves.new(name=name, type='CURVE')

    # The line is drawn in 3D
    line_data.dimensions = '3D'

    # Fill the line
    line_data.fill_mode = 'FULL'

    # The thickness of the line should be by default set to 1.0. This value will be scaled later
    # at the two points of the line.
    line_data.bevel_depth = 1.0

    # For a thick line, the caps are always filled in contrast to the thin line
    line_data.use_fill_caps = True

    # Create a new material (color) and assign it to the line
    line_material = bpy.data.materials.new('color.%s' % name)
    line_material.diffuse_color = color
    line_data.materials.append(line_material)

    # Create a line object and link it to the scene
    line_object = bpy.data.objects.new(str(name), line_data)
    bpy.context.scene.objects.link(line_object)

    # Add the two points to the line object and scale their radii
    line_strip = line_data.splines.new('NURBS')
    line_strip.points.add(1)
    line_strip.points[0].co = (point1[0], point1[1], point1[2]) + (1.0,)
    line_strip.points[1].co = (point2[0], point2[1], point2[2]) + (1.0,)
    line_strip.points[0].radius = point1_radius
    line_strip.points[1].radius = point2_radius
    line_strip.order_u = 1

    # Convert the cone to a mesh object and smooth it using a given smoothness factor
    line_object = nmv.scene.ops.convert_object_to_mesh(line_object)
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subsurf"].levels = smoothness_factor

    # Return a reference to the line object
    return line_object





####################################################################################################
# @draw_poly_lines_as_single_object
####################################################################################################
def draw_poly_lines_as_single_object(poly_lines_data,
                                     format='SOLID',
                                     name='poly_line',
                                     material=None,
                                     color=None,
                                     bevel_object=None,
                                     caps=True,
                                     curve_style='POLY'):
    """Draw a poly line (connected segments of lines) with multiple formats.

    :param poly_lines_data:
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
    :param curve_style:
        A parameter to select amongst the following options:
            ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS'], by default POLY.
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

    for poly_line_data in poly_lines_data:

        # Add the points along the poly-line
        # NOTE: add n-1 points to the array, becuase once the poly-line is created it has already
        # one point added.
        # Options: ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS']
        poly_line_strip = line_data.splines.new('POLY')
        poly_line_strip.points.add(len(poly_line_data) - 1)

        # Add the points (or the samples) and their radii to the poly-line curve
        for i, point in enumerate(poly_line_data):

            poly_line_strip.points[i].co = point[0]
            poly_line_strip.points[i].radius = point[1]

    # Create a curve that uses the curve_data.
    line_strip = bpy.data.objects.new(str(name), line_data)

    # For the NURBS, add the end point and use a high interpolation order, 6
    if curve_style == 'NURBS':
        line_strip.data.splines[0].order_u = 6
        line_strip.data.splines[0].use_endpoint_u = True

    # Link this curve to the scene
    nmv.scene.link_object_to_scene(line_strip)

    # Assume that the location of the line is set at the origin until further notice
    line_strip.location = Vector((0, 0, 0))

    # Return a reference to it
    return line_strip
