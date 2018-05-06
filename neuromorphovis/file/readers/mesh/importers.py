####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender imports
import bpy

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.scene


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

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Build full obj file path
    obj_file_path = "%s/%s" % (input_directory, input_file_name)

    # Try importing the mesh
    try:
        bpy.ops.import_scene.obj(filepath=obj_file_path)

    # Issue an error message if failing
    except:
        nmv.logger.log('LOADING ERROR: cannot load [%s]' % obj_file_path)

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
