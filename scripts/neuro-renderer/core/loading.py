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


####################################################################################################
# @import_obj_file
####################################################################################################
def load_obj_file(input_directory,
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
    file_path = input_directory + '/' + input_file_name

    # Raise a warning if the file doesn't exist
    if not os.path.isfile(file_path):
        print('WARNING: File [%s] does NOT exist, Skipping ...' % file_path)
        return None

    print('Importing [%s]' % file_path)
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
# @import_obj_file
####################################################################################################
def load_ply_file(input_directory,
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
    file_path = input_directory + '/' + input_file_name

    # Raise a warning if the file doesn't exist
    if not os.path.isfile(file_path):
        print('WARNING: File [%s] does NOT exist, Skipping ...' % file_path)
        return None

    print('Importing [%s]' % file_path)
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
# @import_object_from_blend_file
####################################################################################################
def load_object_from_blend_file(input_directory,
                                input_file_name):
    """Import a list of objects that correspond to a neuron object from a blend file and
    return a reference to them.

    :param input_directory:
        Input directory.
    :param input_file_name:
        Input .blend file name.
    :return:
        A reference to the data loaded from the blender object
    """

    # File path
    file_path = input_directory + '/' + input_file_name

    # Raise a warning if the file doesn't exist
    if not os.path.isfile(file_path):
        print('WARNING: File [%s] does NOT exist, Skipping ...' % file_path)
        return None

    # Append all groups from the .blend file
    print('Importing [%s]' % file_path)
    with bpy.data.libraries.load(file_path, link=False) as (data_src, data_dst):
        data_dst.objects = [i_object for i_object in data_src.objects]

    # Add the group instance to the scene
    scene = bpy.context.scene

    objects = list()

    # link objects to current scene
    for i_object in data_dst.objects:
        if i_object is not None:

            if not ('soma' in i_object.name or 'cs' in i_object.name):

                # Adjust the texture UV mapping
                # i_object.data.texspace_size[0] = 10.0
                # i_object.data.texspace_size[1] = 10.0
                # i_object.data.texspace_size[2] = 10.0
                None

            # Append the objects to the scene
            scene.objects.link(i_object)
            objects.append(i_object)

    # Return reference to the loaded objects
    return objects


################################################################################
# @ load_neurons
################################################################################
def load_neurons_membrane_meshes_into_scene(input_directory,
                                            neurons_list,
                                            input_type,
                                            transform=False):
    """Loads the meshes of the membranes of the neurons only into the scene.

    :param input_directory:
        The input directory where the meshes are located.
    :param neurons_list:
        A list of all the neurons parsed from the configuration file.
    :param input_type:
        The types of the input meshes, 'blend', 'ply' or 'obj' .
    """

    # Get the neurons meshes
    for neuron in neurons_list:

        # .blend neurons
        if input_type == 'blend':
            input_file_name = 'neuron_%s.blend' % str(neuron.gid)
            neuron.membrane_meshes = load_object_from_blend_file(input_directory, input_file_name)

        # .ply neurons
        elif input_type == 'ply':
            input_file_name = 'neuron_%s.ply' % str(neuron.gid)
            neuron.membrane_meshes = [load_ply_file(input_directory, input_file_name)]

        # .obj neurons
        elif input_type == 'obj':
            input_file_name = 'neuron_%s.obj' % str(neuron.gid)
            neuron.membrane_meshes = [load_obj_file(input_directory, input_file_name)]

        else:
            print('ERROR: Unrecognized input type [%s]' % input_type)

    if transform:
        print('Transforming')
        for i_neuron in neurons_list:
            for i_object in i_neuron.membrane_meshes:
                for vertex in i_object.data.vertices:
                    vertex.co = i_neuron.transform * vertex.co