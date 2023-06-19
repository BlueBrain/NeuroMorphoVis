####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.interface
import nmv.file
import nmv.scene


####################################################################################################
# @NMV_ExportMesh
####################################################################################################
class NMV_ExportMesh(bpy.types.Operator):
    """Exports the reconstructed mesh"""

    # Operator parameters
    bl_idname = "nmv.export_mesh"
    bl_label = "Export"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Validate the output directory
        nmv.interface.ui.validate_output_directory(panel=self, context_scene=context.scene)

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Get a list of all the meshes in the scene
        mesh_objects = nmv.scene.get_list_of_meshes_in_scene()

        # Export
        nmv.file.export_mesh_objects_to_file(mesh_objects,
                                             nmv.interface.ui_options.io.meshes_directory,
                                             nmv.interface.ui_morphology.label,
                                             context.scene.NMV_ExportedMeshFormat,
                                             context.scene.NMV_ExportIndividuals)

        return {'FINISHED'}


