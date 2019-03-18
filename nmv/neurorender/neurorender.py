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

# Blender imports
import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

import nmv
import nmv.enums
import nmv.shading
import nmv.scene


####################################################################################################
# @NeuroRender
####################################################################################################
class NeuroRender(bpy.types.Panel):
    """NeuroRender panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'NeuroRender'
    bl_category = 'NeuroRender'

    bpy.types.Scene.RenderMaterial = EnumProperty(
        items=nmv.enums.Shading.MATERIAL_ITEMS,
        name="Material",
        default=nmv.enums.Shading.LAMBERT_WARD)

    # Material color
    bpy.types.Scene.MaterialColor = FloatVectorProperty(
        name="Material Color", subtype='COLOR',
        default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
        description="The color of the material")

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel

        :param context:
            Rendering context
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Mesh material
        render_material_row = layout.row()
        render_material_row.prop(context.scene, 'RenderMaterial')

        # Material color
        material_color_row = layout.row()
        material_color_row .prop(context.scene, 'MaterialColor')

        # Rendering view
        apply_material_button_row = layout.row()
        apply_material_button_row.operator('apply_material.to_selected', icon='AXIS_FRONT')



####################################################################################################
# @RenderMeshFront
####################################################################################################
class ApplyMaterialToSelectedMesh(bpy.types.Operator):
    """Applies material to selected mesh"""

    # Operator parameters
    bl_idname = "apply_material.to_selected"
    bl_label = "Apply Material"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator

        :param context:
            Rendering Context.
        :return:
            'FINISHED'
        """

        # Get the selected mesh
        selected_mesh = bpy.context.scene.objects.active

        # If no selected mesh, report it
        if selected_mesh is None:

            # Report the issue in the UI
            self.report({'INFO'}, 'No selected meshes to apply material')

            # Confirm operation done
            return {'FINISHED'}

        if not (selected_mesh.type == 'MESH' or selected_mesh.type == 'CURVE'):

            # Report the issue in the UI
            self.report({'INFO'}, 'Selected object is not a mesh neither a curve')

            # Confirm operation done
            return {'FINISHED'}

        # Clear all the lights
        for scene_object in bpy.context.scene.objects:
            if scene_object.type == 'LAMP':
                nmv.scene.delete_object_in_scene(scene_object)

        bpy.context.object.data.use_auto_texspace = False
        bpy.context.object.data.texspace_size[0] = 5
        bpy.context.object.data.texspace_size[1] = 5
        bpy.context.object.data.texspace_size[2] = 5

        # Get the material color
        material_color = Vector((context.scene.MaterialColor.r,
                                 context.scene.MaterialColor.g,
                                 context.scene.MaterialColor.b))

        # Create the material with its properties and lights
        material = nmv.shading.create_material(
            name='%s_material' % selected_mesh.name, color=material_color,
            material_type=context.scene.RenderMaterial)

        # Apply the material
        nmv.shading.set_material_to_object(selected_mesh, material)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Material applied')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """
    Registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.register_class(NeuroRender)

    # Morphology analysis button
    bpy.utils.register_class(ApplyMaterialToSelectedMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """
    Un-registers all the classes in this panel.
    """

    # Morphology analysis panel
    bpy.utils.unregister_class(NeuroRender)

    # Morphology analysis button
    bpy.utils.unregister_class(ApplyMaterialToSelectedMesh)
