####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
from mathutils import Vector

# Internal imports
import nmv.utilities
import nmv.enums
import nmv.consts
import nmv.interface


####################################################################################################
# @ColorMapOperator
####################################################################################################
class ColorMapOperator(bpy.types.Operator):
    """Color-map operator for interactively changing the color-map in the UI"""

    ################################################################################################
    # Operator parameters
    ################################################################################################
    bl_idname = "nmv_operator.pick_colormap"
    bl_label = "Select ColorMap"
    bl_options = {'REGISTER', 'INTERNAL'}

    ################################################################################################
    # @update_ui_colors
    ################################################################################################
    def update_ui_colors(self,
                         context):

        # Get a list of initial colors from the selected colormap
        colors = nmv.utilities.create_colormap_from_hex_list(
            nmv.enums.ColorMaps.get_hex_color_list(context.scene.NMV_ColorMap),
            nmv.consts.Color.COLORMAP_RESOLUTION)

        for i in range(nmv.consts.Color.COLORMAP_RESOLUTION):
            setattr(context.scene, 'NMV_Color%d' % i, colors[i])


        if False: # vmv.interface.ui.morphology_skeleton is not None:

            # Interpolate
            colors = nmv.utilities.create_colormap_from_color_list(
                nmv.interface.ui_options.morphology.color_map_colors,
                number_colors=nmv.interface.ui_options.morphology.COLORMAP_RESOLUTION)

            for i in range(len(nmv.interface.ui.morphology_skeleton.material_slots)):
                nmv.interface.ui.morphology_skeleton.active_material_index = i

                if bpy.context.scene.render.engine == 'CYCLES':
                    material_nodes = nmv.interface.ui.morphology_skeleton.active_material.node_tree
                    color_1 = material_nodes.nodes['ColorRamp'].color_ramp.elements[0].color
                    color_2 = material_nodes.nodes['ColorRamp'].color_ramp.elements[1].color
                    for j in range(3):
                        color_1[j] = colors[i][j]
                        color_2[j] = 0.5 * colors[i][j]
                else:
                    nmv.interface.ui.morphology_skeleton.active_material.diffuse_color = \
                        Vector((colors[i][0], colors[i][1], colors[i][2], 1.0))

    # A list of all the color maps available in NeuroMorphoVis
    # Note that once a new colormap is selected, the corresponding colors will be set in the UI
    bpy.types.Scene.NMV_ColorMap = bpy.props.EnumProperty(
        items=nmv.enums.ColorMaps.COLOR_MAPS,
        name="ColorMap",
        default=nmv.enums.ColorMaps.GNU_PLOT,
        update=update_ui_colors)

    # Create a list of colors from the selected colormap
    colors = nmv.utilities.create_colormap_from_hex_list(
        nmv.enums.ColorMaps.get_hex_color_list(bpy.types.Scene.NMV_ColorMap),
        nmv.consts.Color.COLORMAP_RESOLUTION)

    # UI color elements for the color map
    for i in range(nmv.consts.Color.COLORMAP_RESOLUTION):
        setattr(bpy.types.Scene, 'NMV_Color%d' % i, bpy.props.FloatVectorProperty(
            name='', subtype='COLOR', default=colors[i], min=0.0, max=1.0, description=''))

    ################################################################################################
    # @poll
    ################################################################################################
    @classmethod
    def poll(cls, context):
        return True

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        return {'FINISHED'}

    ################################################################################################
    # @invoke
    ################################################################################################
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        # A reference to the layout
        layout = self.layout

        # Color map
        color_map = layout.row()
        color_map.prop(context.scene, 'NMV_ColorMap')

        # Its resolution
        colormap_resolution = layout.row()
        colormap_resolution.prop(context.scene, 'NMV_ColorMapResolution')
        nmv.interface.ui_options.shading.morphology_colormap_resolution = context.scene.NMV_ColorMapResolution

        # Clear the color map passed to VMV if it is full
        if len(nmv.interface.ui_options.shading.morphology_colormap_list) > 0:
            nmv.interface.ui_options.shading.morphology_colormap_list.clear()

        # UI color elements
        colors = layout.row()
        for i in range(nmv.consts.Color.COLORMAP_RESOLUTION):

            # Add the color to the interface
            colors.prop(context.scene, 'NMV_Color%d' % i)

            # Get the color value
            color = getattr(context.scene, 'NMV_Color%d' % i)

            print('*' + str(color))
            # Send it to VMV parameters
            nmv.interface.ui_options.shading.morphology_colormap_list.append(color)

