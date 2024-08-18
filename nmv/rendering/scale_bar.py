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

# System imports
import copy

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading
import nmv.rendering

def add_scale_bar(scale_bar_value,
                  scale_bar_size):

    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = "my text"
    font_obj = bpy.data.objects.new("Font Object", font_curve)
    bpy.context.scene.collection.objects.link(font_obj)



