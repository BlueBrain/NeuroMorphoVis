####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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
import nmv
import nmv.scene
import nmv.geometry
import nmv.enums


####################################################################################################
# @sample_to_point
####################################################################################################
def sample_to_point(sample):
    """Converts a point from the poly-line format to the Vector format

    :param sample:
        A given sample along the poly-line.
    :return:
        A point in a Vector format.
    """

    return Vector((sample[0][0], sample[0][1], sample[0][2]))


####################################################################################################
# @get_sample_radius
####################################################################################################
def get_sample_radius(sample):
    """Returns the sample radius in float from the poly-line structure.

    :param sample:
        The given sample.
    :return:
        The radius in float.
    """

    return sample[1]


####################################################################################################
# @point_to_sample
####################################################################################################
def point_to_sample(point,
                    radius=0.0):
    """Converts a point to a poly-line sample.

    :param point:
        A given XYZ point.
    :param radius:
        The sample radius.
    :return:
        The sample in the poly-line format.
    """

    return [(point[0], point[1], point[2], 1), radius]


####################################################################################################
# @compute_poly_line_length
####################################################################################################
def compute_poly_line_length(poly_line):
    """
    Computes the length of a given poly-line.

    :param poly_line:
        A given poly-line to compute its length.
    :return:
        Poly-line total length in microns.
    """

    # Section length
    poly_line_length = 0.0

    # If the section has less than two samples, then report the error
    if len(poly_line.samples) < 2:
        # Return 0
        return poly_line_length

    # Integrate the distance between each two successive samples
    for i in range(len(poly_line.samples) - 1):
        # Retrieve the points along each segment on the section
        point_0 = Vector((poly_line.samples[i][0][0],
                          poly_line.samples[i][0][1],
                          poly_line.samples[i][0][2]))
        point_1 = Vector((poly_line.samples[i + 1][0][0],
                          poly_line.samples[i + 1][0][1],
                          poly_line.samples[i + 1][0][2]))

        # Update the section length
        poly_line_length += (sample_to_point(poly_line.samples[i + 1]) -
                             sample_to_point(poly_line.samples[i])).length

    # Return the section length
    return poly_line_length


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
# @draw_poly_line
####################################################################################################
def draw_poly_line(poly_line_data,
                   name='poly_line',
                   format='SOLID',
                   material=None,
                   color=None,
                   bevel_object=None,
                   caps=True,
                   curve_style='POLY'):
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

    # Add the points along the poly-line
    # NOTE: add n-1 points to the array, because once the poly-line is created it has already one
    # point added.
    # Options: ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS']
    poly_line_strip = line_data.splines.new(curve_style)
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


####################################################################################################
# @draw_poly_lines_in_single_object
####################################################################################################
def draw_poly_lines_in_single_object(poly_lines,
                                     object_name='poly_lines',
                                     edges=nmv.enums.Arbors.Edges.SHARP,
                                     bevel_object=None,
                                     materials=None,
                                     poly_line_caps=True,
                                     texture_size=5.0):
    """Draws a list of poly-lines in a single Blender object to reduce the overhead of having
    multiple objects in the scene.

    :param poly_lines:
        A list of poly-lines of type PolyLine.
    :param object_name:
        The name of the drawn object.
    :param edges:
        The type of the poly-line: ['POLY', 'BEZIER', 'BSPLINE', 'CARDINAL', 'NURBS']
    :param bevel_object:
        A given bevel object to shape the cross-section of the poly-lines.
    :param materials:
        A list of materials.
    :param poly_line_caps:
        A flag to indicate whether the poly-lines are closed or open at the terminals.
    :param texture_size:
        For UV mapping.
    :return:
        A reference to the drawn poly-lines object.
    """

    # Create the object as a new curve
    poly_lines_object = bpy.data.curves.new(name=object_name, type='CURVE')

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
    poly_lines_object.use_fill_caps = poly_line_caps

    # If a bevel object is given, use it for scaling the diameter of the poly-line
    if bevel_object is not None:
        poly_lines_object.bevel_object = bevel_object

    # If a list of materials is given, then append it to the skeleton object
    if materials is not None:
        for material in materials:
            poly_lines_object.materials.append(material)

    if edges == nmv.enums.Arbors.Edges.SHARP:
        poly_line_type = 'POLY'
    else:
        poly_line_type = 'NURBS'

    # Append the poly-lines
    for poly_line in poly_lines:
        append_poly_line_to_base_object(
            base_object=poly_lines_object, poly_line=poly_line, poly_line_type=poly_line_type)

    # Create the aggregate object to be linked to the scene later
    aggregate_poly_lines_object = bpy.data.objects.new(
        object_name, poly_lines_object)

    if poly_line_type == 'NURBS':
        aggregate_poly_lines_object.data.splines[0].order_u = 6
        aggregate_poly_lines_object.data.splines[0].use_endpoint_u = True

    # Link this object to the scene
    bpy.context.scene.collection.objects.link(aggregate_poly_lines_object)

    # Return a reference to the created poly-lines object
    return aggregate_poly_lines_object


####################################################################################################
# @draw_poly_lines_in_multiple_objects
####################################################################################################
def draw_poly_lines_in_multiple_objects(poly_lines,
                                        prefix='poly-lines',
                                        poly_line_type='POLY',
                                        bevel_object=None,
                                        materials=None,
                                        poly_line_caps=True,
                                        texture_size=5.0):
    # A list of all the drawn poly-lines
    poly_lines_list = list()

    # Poly-line by poly-line
    # for poly_line in poly_lines:
    #    poly_lines_list.append(draw_poly_line(poly_line), )


####################################################################################################
# @resample_poly_line_at_fixed_step
####################################################################################################
def resample_poly_line_at_fixed_step(poly_line,
                                     sampling_step=1.0):
    """Resamples a poly-line (the samples list of the poly-line) at a fixed step.
    If the poly-line has only two samples, it will never get resampled. If its length is smaller
    than the sampling step, a convenient sampling step will be computed and used.

    :param poly_line:
        A given poly-line to be resampled.
    :param sampling_step:
        The resampling step, by default 1.0 um.
    """

    # If the poly-line has no samples, report this as an error and ignore this filter
    if len(poly_line.samples) == 0:
        nmv.logger.error('Poly-line [%s] has NO samples, cannot be re-sampled' % poly_line.name)
        return

    # If the poly-line has ONLY one sample, report this as an error and ignore this filter
    elif len(poly_line.samples) == 1:
        nmv.logger.error('Poly-line [%s] has ONE sample, cannot be re-sampled' % poly_line.name)
        return

    # If the poly-line length is less than the sampling step, then adaptively resample it
    poly_line_length = compute_poly_line_length(poly_line=poly_line)
    if poly_line_length < sampling_step:
        # Get a good sampling step that would match this small poly-line
        number_samples = len(poly_line.samples)
        convenient_step = poly_line_length / number_samples

        # Resample the poly-line at this sampling step
        resample_poly_line_at_fixed_step(poly_line=poly_line, sampling_step=convenient_step)
        return

    # Sample index
    i = 0

    # Just keep moving along the poly-line till you hit the last sample
    while True:

        # Break if we reach the last sample
        if i >= len(poly_line.samples) - 1:
            break

        # Compute the distance between the current sample and the next one
        distance = (sample_to_point(poly_line.samples[i + 1]) -
                    sample_to_point(poly_line.samples[i])).length

        # If the distance is less than the resampling step, then remove this sample at [i + 1]
        if distance < sampling_step:

            # If this is the last sample, then terminate as we cannot remove the last sample
            if i >= len(poly_line.samples) - 2:
                break

            # Remove the sample
            poly_line.samples.remove(poly_line.samples[i + 1])

            # Proceed to the next sample
            continue

        # If the sample is at a greater step, then add a new sample exactly at the current step
        else:

            # Compute the auxiliary sample radius based on the previous and next samples
            radius = (get_sample_radius(poly_line.samples[i + 1]) +
                      get_sample_radius(poly_line.samples[i])) / 2.0

            # Compute the direction
            direction = (sample_to_point(poly_line.samples[i + 1]) -
                         sample_to_point(poly_line.samples[i])).normalized()

            # Compute the auxiliary sample point, use epsilon for floating point comparison
            point = sample_to_point(poly_line.samples[i]) + (direction * sampling_step)

            # Update the samples list
            poly_line.samples.insert(i + 1, point_to_sample(point, radius))

            # Move to the nex sample
            i += 1

            # Break if we reach the last sample
            if i >= len(poly_line.samples) - 1:
                break


####################################################################################################
# @resample_poly_line_adaptively
####################################################################################################
def resample_poly_line_adaptively(poly_line):
    """Adaptively resamples the given poly-line. The adaptive sampling scheme removes the
    unnecessary samples along the poly-line, or those that overlap based on their positions and
    radii.

    :param poly_line:
        A given poly-line to be resampled.
    """

    # If the poly-line has no samples, report this as an error and ignore this filter
    if len(poly_line.samples) == 0:
        nmv.logger.error('Poly-line [%s] has NO samples, cannot be re-sampled' % poly_line.name)
        return

    # If the poly-line has ONLY one sample, report this as an error and ignore this filter
    elif len(poly_line.samples) == 1:
        nmv.logger.error('Poly-line [%s] has ONE sample, cannot be re-sampled' % poly_line.name)
        return

    # Sample index
    i = 0

    # Just keep moving along the poly-line till you hit the last sample
    while True:

        # Break if we reach the last sample
        if i >= len(poly_line.samples) - 1:
            break

        # Compute the distance between the current sample and the next one
        distance = (sample_to_point(poly_line.samples[i + 1]) -
                    sample_to_point(poly_line.samples[i])).length

        # Get the extent of the sample, where no other samples should be located
        extent = get_sample_radius(poly_line.samples[i])

        # If the next sample is located within the extent of this sample, then remove it
        if distance < extent:

            # If this is the last sample, then terminate as we cannot remove the last sample
            if i >= len(poly_line.samples) - 2:
                break

            # Remove the sample
            poly_line.samples.remove(poly_line.samples[i + 1])

            # Proceed to the next sample
            continue

        # Otherwise, add a new sample at the radius
        else:

            # Compute the auxiliary sample radius based on the previous and next samples
            radius = (get_sample_radius(poly_line.samples[i + 1]) +
                      get_sample_radius(poly_line.samples[i])) / 2.0

            # Compute the direction
            direction = (sample_to_point(poly_line.samples[i + 1]) -
                         sample_to_point(poly_line.samples[i])).normalized()

            # Compute the auxiliary sample point, use epsilon for floating point comparison
            point = sample_to_point(poly_line.samples[i]) + (direction * extent)

            # Update the samples list
            poly_line.samples.insert(i + 1, point_to_sample(point, radius))

            # Move to the nex sample
            i += 1

            # Break if we reach the last sample
            if i >= len(poly_line.samples) - 1:
                break


####################################################################################################
# @resample_poly_line_adaptively_relaxed
####################################################################################################
def resample_poly_line_adaptively_relaxed(poly_line):
    """Adaptively resamples the given poly-line in a relaxed way.
    This adaptive sampling scheme removes the unnecessary samples along the poly-line, or those
    that overlap based on their positions and the sum of the radii of two consecutive samples.

    :param poly_line:
        A given poly-line to be resampled.
    """

    # If the poly-line has no samples, report this as an error and ignore this filter
    if len(poly_line.samples) == 0:
        nmv.logger.error('Poly-line [%s] has NO samples, cannot be re-sampled' % poly_line.name)
        return

    # If the poly-line has ONLY one sample, report this as an error and ignore this filter
    elif len(poly_line.samples) == 1:
        nmv.logger.error('Poly-line [%s] has ONE sample, cannot be re-sampled' % poly_line.name)
        return

    # Sample index
    i = 0

    # Just keep moving along the poly-line till you hit the last sample
    while True:

        # Break if we reach the last sample
        if i >= len(poly_line.samples) - 1:
            break

        # Compute the distance between the current sample and the next one
        distance = (sample_to_point(poly_line.samples[i + 1]) -
                    sample_to_point(poly_line.samples[i])).length

        # Get the extent of the sample, where no other samples should be located
        extent = get_sample_radius(poly_line.samples[i]) + \
                 get_sample_radius(poly_line.samples[i + 1])

        # If the next sample is located within the extent of this sample, then remove it
        if distance < extent:

            # If this is the last sample, then terminate as we cannot remove the last sample
            if i >= len(poly_line.samples) - 2:
                break

            # Remove the sample
            poly_line.samples.remove(poly_line.samples[i + 1])

            # Proceed to the next sample
            continue

        # Otherwise, add a new sample at the radius
        else:

            # Compute the auxiliary sample radius based on the previous and next samples
            radius = (get_sample_radius(poly_line.samples[i + 1]) +
                      get_sample_radius(poly_line.samples[i])) / 2.0

            # Compute the direction
            direction = (sample_to_point(poly_line.samples[i + 1]) -
                         sample_to_point(poly_line.samples[i])).normalized()

            # Compute the auxiliary sample point, use epsilon for floating point comparison
            point = sample_to_point(poly_line.samples[i]) + (direction * extent)

            # Update the samples list
            poly_line.samples.insert(i + 1, point_to_sample(point, radius))

            # Move to the nex sample
            i += 1

            # Break if we reach the last sample
            if i >= len(poly_line.samples) - 1:
                break
