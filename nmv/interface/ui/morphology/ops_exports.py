
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

# Internal imports
import nmv.interface
import nmv.builders
import nmv.mesh
import nmv.scene


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
# @NMV_ExportMorphologyExtendedSWC
####################################################################################################
class NMV_ExportMorphologyExtendedSWC(bpy.types.Operator):
    """Export the morphology to an extended SWC file"""

    # Operator parameters
    bl_idname = "nmv.save_morphology_eswc"
    bl_label = "Extended SWC (.swc)"

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

        builder = nmv.builders.SomaMetaBuilder(morphology=nmv.interface.ui_morphology,
                                               options=nmv.interface.ui_options)
        soma_mesh = builder.reconstruct_soma_mesh(apply_shader=False, soma_name='SWC_SOMA')

        # The soma object is contained in the self.mesh, so triangulate it
        nmv.mesh.triangulate_mesh(mesh_object=soma_mesh)

        # Get a list of faces (triangles) and their corresponding vertices
        triangles = soma_mesh.data.polygons

        # Create the list of vertices in the profile_3d data
        for triangle in triangles:
            v1 = soma_mesh.data.vertices[triangle.vertices[0]]
            profile_v1 = [v1.co.x, v1.co.y, v1.co.z]
            nmv.interface.ui_morphology.soma.profile_3d.append(profile_v1)

            v2 = soma_mesh.data.vertices[triangle.vertices[1]]
            profile_v2 = [v2.co.x, v2.co.y, v2.co.z]
            nmv.interface.ui_morphology.soma.profile_3d.append(profile_v2)

            v3 = soma_mesh.data.vertices[triangle.vertices[2]]
            profile_v3 = [v3.co.x, v3.co.y, v3.co.z]
            nmv.interface.ui_morphology.soma.profile_3d.append(profile_v3)

        # Delete the temporary soma mesh
        nmv.scene.delete_object_in_scene(scene_object=soma_mesh)

        # Export the reconstructed morphology as an .blend file
        # NOTE: Since we don't have meshes, then the mesh_object argument will be set to None and
        # the exported blender file will contain all the morphology objects.
        nmv.file.write_morphology_to_extended_swc_file(
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
