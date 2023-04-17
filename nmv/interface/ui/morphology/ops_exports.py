
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
import nmv.interface


####################################################################################################
# @NMV_ExportMorphologySWC
####################################################################################################
class NMV_ExportMorphologySWC(bpy.types.Operator):
    """Export the morphology to an SWC file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_swc"
    bl_label = "SWC (.swc)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.write_morphology_to_swc_file(
            nmv.interface.ui_morphology,
            nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @NMV_ExportMorphologySegments
####################################################################################################
class NMV_ExportMorphologySegments(bpy.types.Operator):
    """Export the morphology as a list of segments into file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_segments"
    bl_label = "Segments (.segments)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.write_morphology_to_segments_file(
            nmv.interface.ui_morphology,
            nmv.interface.ui_options.io.morphologies_directory)

        return {'FINISHED'}


####################################################################################################
# @NMV_ExportMorphologyBLEND
####################################################################################################
class NMV_ExportMorphologyBLEND(bpy.types.Operator):
    """Save the reconstructed morphology in a blender file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_blend"
    bl_label = "Blender Format (.blend)"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Verify the output directory
        if not nmv.interface.validate_output_directory(self, context.scene):
            return {'FINISHED'}

        # Create the meshes directory if it does not exist
        if not nmv.file.ops.path_exists(nmv.interface.ui_options.io.morphologies_directory):
            nmv.file.ops.clean_and_create_directory(
                nmv.interface.ui_options.io.morphologies_directory)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.export_scene_to_blend_file(
            output_directory=nmv.interface.ui_options.io.morphologies_directory,
            output_file_name=nmv.interface.ui_morphology.label)

        return {'FINISHED'}
