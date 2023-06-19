####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import os

# Blender imports
import bpy

# Internal imports
import nmv.scene
import nmv.mesh


####################################################################################################
# @import_obj_file
####################################################################################################
def import_obj_file(input_directory,
                    input_file_name):
    """Import an .OBJ file into the scene, and return a reference to it.

    :param input_directory:
        The directory that is supposed to have the mesh.
    :param input_file_name:
        The name of the mesh file.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # File path
    file_path = "%s/%s" % (input_directory, input_file_name)

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        nmv.logger.log('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    nmv.logger.log('Loading [%s]' % file_path)
    bpy.ops.import_scene.obj(filepath=file_path)

    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # NOTE: Blender always loads the OBJ meshes with a 90 degrees rotation, so we must rotate the
    # mesh object to adjust the orientation in front of the camera
    nmv.scene.rotate_object(mesh_object, 0, 0, 0)

    # Return a reference to the object
    return mesh_object


####################################################################################################
# @import_ply_file
####################################################################################################
def import_ply_file(input_directory,
                    input_file_name):
    """Import an .OBJ file into the scene, and return a reference to it.

    :param input_directory:
        The directory that is supposed to have the mesh.
    :param input_file_name:
        The name of the mesh file.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # File path
    file_path = "%s/%s" % (input_directory, input_file_name)

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        nmv.logger.log('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    nmv.logger.log('Loading [%s]' % file_path)
    bpy.ops.import_mesh.ply(filepath=file_path)

    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # Return a reference to the object
    return mesh_object


####################################################################################################
# @import_stl_file
####################################################################################################
def import_stl_file(input_directory,
                    input_file_name):
    """Import an .STL file into the scene, and return a reference to it.

    :param input_directory:
        The directory that is supposed to have the mesh.
    :param input_file_name:
        The name of the mesh file.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # File path
    file_path = "%s/%s" % (input_directory, input_file_name)

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        nmv.logger.log('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    nmv.logger.log('Loading [%s]' % file_path)
    bpy.ops.import_mesh.stl(filepath=file_path)

    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # Return a reference to the object
    return mesh_object


####################################################################################################
# @import_object_from_blend_file
####################################################################################################
def import_object_from_blend_file(input_directory,
                                  input_file_name):
    """Import the objects from a blend file and return a reference to them.

    :param input_directory:
        The directory that is supposed to have the mesh.
    :param input_file_name:
        The name of the mesh file.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # Build file path
    file_path = input_directory + '/' + input_file_name
    nmv.logger.log('Importing [%s]' % file_path)

    # Append all groups from the .blend file
    with bpy.data.libraries.load(file_path, link=False) as (data_src, data_dst):
        for i_object in data_src.objects:
            data_dst.objects.append(i_object)

    # Add the group instance to the current scene
    current_scene = bpy.context.scene

    # Link objects to current scene
    for i_object in data_dst.objects:
        if i_object is not None:
            nmv.scene.link_object_to_scene(i_object)

    # Return reference to the objects loaded
    return data_dst.objects


####################################################################################################
# @import_mesh
####################################################################################################
def import_mesh(mesh_file_path):
    """Import a mesh file into Blender.

    :param mesh_file_path:
        The path to the mesh file.
    :return:
        Either a reference to the imported mesh, or None if the file does not exist.
    """

    # Get the extension
    file_prefix, file_extension = os.path.splitext(mesh_file_path)

    # Get the directory and file name
    file_name = os.path.basename(mesh_file_path)
    directory = os.path.dirname(mesh_file_path)

    if 'obj' in file_extension or 'OBJ' in file_extension or 'Obj' in file_extension:
        return import_obj_file(directory, file_name)
    elif 'ply' in file_extension or 'PLY' in file_extension or 'Ply' in file_extension:
        return import_ply_file(directory, file_name)
    elif 'stl' in file_extension or 'STL' in file_extension or 'Stl' in file_extension:
        return import_stl_file(directory, file_name)

    # Otherwise, return None
    return None


####################################################################################################
# @import_mesh_list
####################################################################################################
def import_mesh_list(files_paths):
    """Imports a list of meshes into the scene all at once.

    :param files_paths:
        A list of all the file paths.
    :return:
        A list of all the loaded meshes.
    """

    # A list fo all the mesh objects loaded in the scene
    mesh_objects_list = list()
    for file_path in files_paths:
        mesh_objects_list.append(import_mesh(mesh_file_path=file_path))

    # Return the list
    return mesh_objects_list


####################################################################################################
# @import_mesh_list_into_single_mesh
####################################################################################################
def import_mesh_list_into_single_mesh(files_paths,
                                      mesh_name):
    """Imports a list of meshes into a single mesh object with multiple partitions.

    :param files_paths:
        A list of all the file paths.
    :param mesh_name:
        The name of the final mesh.
    :return:
        A reference to the mesh object.
    """

    # Load the mesh objects
    mesh_list = import_mesh_list(files_paths)

    # Join them into a single mesh
    return nmv.mesh.join_mesh_objects(mesh_list=mesh_list, name=mesh_name)
