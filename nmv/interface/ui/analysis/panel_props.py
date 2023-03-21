####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

# Blender imports
import bpy

####################################################################################################
# Bounding box analysis options
####################################################################################################
bpy.types.Scene.NMV_BBoxPMinX = bpy.props.FloatProperty(
    name="X",
    description="X-coordinate of PMin",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxPMinY = bpy.props.FloatProperty(
    name="Y",
    description="Y-coordinate of PMin",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxPMinZ = bpy.props.FloatProperty(
    name="Z",
    description="Z-coordinate of PMin",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxPMaxX = bpy.props.FloatProperty(
    name="X",
    description="X-coordinate of PMax",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxPMaxY = bpy.props.FloatProperty(
    name="Y",
    description="Y-coordinate of PMax",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxPMaxZ = bpy.props.FloatProperty(
    name="Z",
    description="Z-coordinate of PMax",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxCenterX = bpy.props.FloatProperty(
    name="X",
    description="X-coordinate of center of the morphology",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxCenterY = bpy.props.FloatProperty(
    name="Y",
    description="Y-coordinate of center of the morphology",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BBoxCenterZ = bpy.props.FloatProperty(
    name="Z",
    description="Z-coordinate of center of the morphology",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BoundsX = bpy.props.FloatProperty(
    name="X",
    description="Morphology width",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BoundsY = bpy.props.FloatProperty(
    name="Y",
    description="Morphology height",
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.NMV_BoundsZ = bpy.props.FloatProperty(
    name="Z",
    description="Morphology depth",
    min=-1e10, max=1e10, subtype='FACTOR')

# Analysis time
bpy.types.Scene.NMV_MorphologyAnalysisTime = bpy.props.FloatProperty(
    name="Analysis Time (Sec)",
    default=0, min=0, max=1000000)
