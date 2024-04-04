####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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
import os
import sys
import ntpath

# Blender imports
import bpy

# INternal imports
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
import scene_utilities


####################################################################################################
# @import_obj_file
####################################################################################################
def import_obj_file(file_path):
    """Imports an OBJ file.

    :param file_path:
        The path to the mesh file
    :return:
        A reference to the loaded mesh in Blender.
    """

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        print('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    scene_utilities.deselect_all()

    print('Loading [%s]' % file_path)
    bpy.ops.import_scene.obj(filepath=file_path)

    # Get the file name to rename the object
    input_file_name = ntpath.basename(file_path)

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
def import_ply_file(file_path):
    """Import an .OBJ file into the scene, and return a reference to it.

    :param file_path:
        The mesh path.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        print('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    scene_utilities.deselect_all()

    print('Loading [%s]' % file_path)
    bpy.ops.import_mesh.ply(filepath=file_path)

    # Get the file name to rename the object
    input_file_name = ntpath.basename(file_path)

    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # Return a reference to the object
    return mesh_object


####################################################################################################
# @import_mesh
####################################################################################################
def import_mesh(file_path):
    """Imports a mesh into the Blender context.

    :param file_path:
        The absolute path to the mesh file.
    :return:
        A reference to the loaded mesh.
    """

    # Get the file name and extension
    file_name, file_extension = os.path.splitext(file_path)

    # Import the file
    if '.ply' in file_extension.lower():
        return import_ply_file(file_path)
    elif '.obj' in file_extension.lower():
        return import_obj_file(file_path)
    else:
        print('Unsupported file format! Exiting')
        exit(0)

