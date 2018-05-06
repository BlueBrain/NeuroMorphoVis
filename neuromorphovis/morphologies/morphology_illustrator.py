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


# System imports
import os, sys, random, math

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal modules
import meshy_modules
import morphology


####################################################################################################
# @draw_section_as_line
####################################################################################################
def draw_section_as_line(section,
                         line_thickness=1,
                         color=(1, 1, 1)):
    """
    Draws the section as a simple line.

    :param section: A given section.
    :param line_thickness: The thickness of the section.
    :param color: The color of the section.
    :return: A reference to the drawn section.
    """

    # Setup curve data
    curve_data = bpy.data.curves.new(name='section_%d' % 1, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.fill_mode = 'FULL'
    curve_data.bevel_depth = line_thickness

    # Add the samples to a poly-line strip
    number_segments = len(section.samples)
    poly_line_strip = curve_data.splines.new('POLY')
    poly_line_strip.points.add(number_segments - 1)

    # Add the samples of the different segments composing the section
    for idx in range(number_segments):

        # Add the segment points to the curve
        poly_line_strip.points[idx].co = (section.samples[idx].point[0],
        section.samples[idx].point[1], section.samples[idx].point[2]) + (1.0,)

        # Set the radius
        poly_line_strip.points[idx].radius = section.samples[idx].radius

    # Create a curve that uses the curve_data.
    line_strip = bpy.data.objects.new('curve.%d' % 1, curve_data)
    bpy.context.scene.objects.link(line_strip)
    line_strip.location = (0.0, 0.0, 0.0)

    # Setup a simple material.
    line_material = bpy.data.materials.new('material.%d' % 1)
    line_material.diffuse_color = color
    line_material.use_shadeless = True
    line_strip.data.materials.append(line_material)

    # Return a reference to the drawn section.
    return line_strip


####################################################################################################
# @draw_arbor
####################################################################################################
def draw_arbor(root):
    """
    This function draws a single arbor.

    :param root: Arbor root
    """
    # Make sure that the arbor exists.
    if root is not None:

        # Draw the section as a line
        draw_section_as_line(root)

        # Do it for the children as well
        for child in root.children:

            # Child by child
            draw_arbor(child)


####################################################################################################
# @draw_morphology
####################################################################################################
def draw_morphology(morphology_skeleton):
    """
    This function draws the morphological skeleton.

    :param morphology_skeleton: A given morphology skeleton to draw.
    """

    # Draw the axon
    draw_arbor(morphology_skeleton.axon)

    # Draw the basal dendrites
    for basal_dendrite in morphology_skeleton.dendrites:
        draw_arbor(basal_dendrite)

    # Draw the apical dendrite
    draw_arbor(morphology_skeleton.apical_dendrite)