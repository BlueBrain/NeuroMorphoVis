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

# Internal modules
import nmv
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.mesh
import nmv.utilities


####################################################################################################
# @export_scene_to_blend_file
####################################################################################################
def export_scene_to_blend_file(output_directory,
                               output_file_name):
    """Exports the current scene to a binary .blend file.

    :param output_directory:
        The output directory where the mesh will be saved.
    :param output_file_name:
        The name of the output mesh.
    """

    # Construct the name of the exported mesh.
    output_file_path = "%s/%s.blend" % (output_directory, output_file_name)

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Export the mesh object to a binary STL file
    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    bpy.ops.wm.save_as_mainfile(filepath=output_file_path, check_existing=True)

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_mesh_object_to_file
####################################################################################################
def export_mesh_object_to_file(mesh_object,
                               output_directory,
                               output_file_name,
                               file_format=nmv.enums.Meshing.ExportFormat.PLY):
    """Exports a mesh object to a file with a specific file format.

    :param mesh_object:
        A selected mesh object in the scene.
    :param output_directory:
        The output directory where the mesh will be saved.
    :param output_file_name:
        The name of the output mesh.
    :param file_format:
        The file format of the mesh.
    """

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the target mesh and set it to be the only active object
    nmv.scene.ops.set_active_object(mesh_object)

    if file_format == nmv.enums.Meshing.ExportFormat.PLY:
        output_file_path = "%s/%s%s" % (
            output_directory, str(output_file_name), nmv.consts.Meshing.PLY_EXTENSION)

    elif file_format == nmv.enums.Meshing.ExportFormat.OBJ:
        output_file_path = "%s/%s%s" % (
            output_directory, str(output_file_name), nmv.consts.Meshing.OBJ_EXTENSION)

    elif file_format == nmv.enums.Meshing.ExportFormat.STL:
        output_file_path = "%s/%s%s" % (
            output_directory, str(output_file_name), nmv.consts.Meshing.STL_EXTENSION)

    else:
        nmv.logger.log('Error: Unknown mesh format')
        return

    # Export the mesh object to an OBJ file
    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    if file_format == nmv.enums.Meshing.ExportFormat.PLY:
        bpy.ops.export_mesh.ply(filepath=output_file_path, check_existing=True)

    elif file_format == nmv.enums.Meshing.ExportFormat.OBJ:
        bpy.ops.export_scene.obj(
            filepath=output_file_path, check_existing=True, axis_forward='-Z', axis_up='Y',
            use_selection=True, use_smooth_groups=True, use_smooth_groups_bitflags=False,
            use_normals=True, use_triangles=True, path_mode='AUTO')

    elif file_format == nmv.enums.Meshing.ExportFormat.STL:
        bpy.ops.export_mesh.stl(
            filepath=output_file_path, use_selection=True, check_existing=True, ascii=False)

    else:
        nmv.logger.log('Error: Unknown mesh format')

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_mesh_objects_to_file
####################################################################################################
def export_mesh_objects_to_file(mesh_objects,
                                output_directory,
                                output_file_name,
                                file_format=nmv.enums.Meshing.ExportFormat.PLY,
                                export_individual_meshes=False):
    """Exports a list of mesh objects as an individual mesh or separate objects.

    :param mesh_objects:
        A list of mesh objects in the scene to be exported.
    :param output_directory:
        The output directory where the mesh(es) will be saved.
    :param output_file_name:
        The name of the output mesh.
    :param file_format:
        The file format of the exported mesh.
    :param export_individual_meshes:
        Export the individual meshes in the list.
    """

    # Blend files are exported once whatever the selection is
    if file_format == nmv.enums.Meshing.ExportFormat.BLEND:

        # Export the cloned file
        export_scene_to_blend_file(output_directory, output_file_name)

    # Other file formats have the same approach
    else:

        # Export each component in the mesh
        if export_individual_meshes:

            # Create a directory with the name of the mesh
            mesh_directory = '%s/%s' % (output_directory, output_file_name)
            nmv.file.ops.clean_and_create_directory(mesh_directory)

            # Export each mesh in the given list
            for mesh_object in mesh_objects:
                export_mesh_object_to_file(
                    mesh_object, mesh_directory, mesh_object.name, file_format)
        else:

            # Clone all the mesh objects
            joint_mesh_object = nmv.scene.ops.clone_mesh_objects_into_joint_mesh(mesh_objects)

            # Export the cloned file
            export_mesh_object_to_file(
                joint_mesh_object, output_directory, output_file_name, file_format)

            # Delete the cloned object
            nmv.scene.ops.delete_list_objects([joint_mesh_object])


####################################################################################################
# @export_mesh_object
####################################################################################################
def export_mesh_object(mesh_object,
                       output_directory,
                       file_name,
                       obj=False, ply=False, stl=False, blend=False):
    """Exports the mesh in one line in different file formats.

    :param mesh_object:
        An input mesh object to export to a file.
    :param output_directory:
        Output directory where the meshes will be saved.
    :param file_name:
        Mesh prefix.
    :param obj:
        Flag to export to .obj format.
    :param ply:
        Flag to export to .ply format.
    :param stl:
        Flag to export to .stl format.
    :param blend:
        Flag to export to .blend format.
    """

    # To .obj format
    if obj:
        export_mesh_object_to_file(
            mesh_object, output_directory, file_name, nmv.enums.Meshing.ExportFormat.OBJ)

    # To .ply format
    if ply:
        export_mesh_object_to_file(
            mesh_object, output_directory, file_name, nmv.enums.Meshing.ExportFormat.PLY)

    # .To stl format
    if stl:
        export_mesh_object_to_file(
            mesh_object, output_directory, file_name, nmv.enums.Meshing.ExportFormat.STL)

    # To .blend format
    if blend:
        export_scene_to_blend_file(output_directory, file_name)
