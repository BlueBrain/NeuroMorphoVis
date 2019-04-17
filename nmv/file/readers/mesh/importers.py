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

# System imports
import os

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.scene


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
        data_dst.objects = [i_object for i_object in data_src.objects]

    # Add the group instance to the current scene
    current_scene = bpy.context.scene

    # Link objects to current scene
    for i_object in data_dst.objects:
        if i_object is not None:
            current_scene.objects.link(i_object)

    # Return reference to the objects loaded
    return data_dst.objects
