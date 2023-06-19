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

# System imports
import time

# Blender imports
import bpy

# Internal modules
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.utilities


####################################################################################################
# @NMV_ExportSomaMesh
####################################################################################################
class NMV_ExportSomaMesh(bpy.types.Operator):
    """Exports the reconstructed soma mesh"""

    # Operator parameters
    bl_idname = "nmv.export_soma_mesh"
    bl_label = "Export Mesh"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # If no morphology is loaded, report it
        if nmv.interface.ui_morphology is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.meshes_directory):
            nmv.file.ops.clean_and_create_directory(nmv.interface.ui_options.io.meshes_directory)

        # Export
        nmv.file.export_mesh_object_to_file(nmv.interface.ui_soma_mesh,
                                            nmv.interface.ui_options.io.meshes_directory,
                                            nmv.interface.ui_morphology.label,
                                            context.scene.NMV_ExportedSomaMeshFormat)

        # Finished
        return {'FINISHED'}
