####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @draw_colors_header
####################################################################################################
def draw_colors_header(layout):

    row = layout.row()
    row.label(text='Colors & Materials', icon='COLOR')


####################################################################################################
# @draw_soma_color
####################################################################################################
def draw_soma_color(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaBaseColor')
    options.shading.soma_color = scene.NMV_SomaBaseColor


####################################################################################################
# @draw_soma_material
####################################################################################################
def draw_soma_material_option(layout, scene, options):

    row = layout.row()
    row.prop(scene, 'NMV_SomaMaterial')
    options.shading.soma_material = scene.NMV_SomaMaterial


####################################################################################################
# @draw_soma_color_options
####################################################################################################
def draw_soma_color_options(panel, scene, options):

    draw_colors_header(layout=panel.layout)
    draw_soma_color(layout=panel.layout, scene=scene, options=options)
    draw_soma_material_option(layout=panel.layout, scene=scene, options=options)