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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.utilities

# Rendering resolution
bpy.types.Scene.NMV_ResolutionBasis = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.Resolution.FIXED,
            'Fixed',
            'Render an image at a specific resolution, for example: 1024 or 2048 pixels'),
           (nmv.enums.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'The resolution of the final image is a multiple factor of the exact scale of the '
            'morphology in microns')],
    name='Type',
    default=nmv.enums.Rendering.Resolution.FIXED)

# Rendering view, for the Synaptics and Mesh Reconstruction panels
bpy.types.Scene.NMV_RenderingView = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.View.WIDE_SHOT,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Rendering.View.CLOSEUP,
            'Closeup',
            'Renders a closeup image the focuses on the soma of the chosen morphology')],
    name='View',
    default=nmv.enums.Rendering.View.WIDE_SHOT)

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.NMV_RenderScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Render the scale bar on the rendered image',
    default=False)

# Image format
bpy.types.Scene.NMV_ImageFormat = bpy.props.EnumProperty(
    items=nmv.enums.Image.Extension.IMAGE_EXTENSION_ITEMS,
    name='',
    default=nmv.enums.Image.Extension.PNG)

# Image resolution
bpy.types.Scene.NMV_FrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image to be rendered',
    default=nmv.consts.Image.DEFAULT_RESOLUTION, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option'
bpy.types.Scene.NMV_ResolutionScaleFactor = bpy.props.FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a scene to scale")

# The dimensions of the closeup view in microns
bpy.types.Scene.NMV_CloseupDimensions = bpy.props.FloatProperty(
    name='Size',
    description='The dimensions of the closeup view in microns',
    default=20, min=5, max=100)

