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


# System imports
import os

# Blender imports
import bpy

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.file


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
        print('WARNING: File [%s] does NOT exist, Skipping ...')
        return None

    # Append all groups from the .blend file
    print('Importing [%s]' % file_path)
    with bpy.data.libraries.load(file_path, link=False) as (data_src, data_dst):
        data_dst.objects = [i_object for i_object in data_src.objects]

    # Add the group instance to the scene
    scene = bpy.context.scene

    # link objects to current scene
    for i_object in data_dst.objects:
        if i_object is not None:
            if not ('soma' in i_object.name or 'cs' in i_object.name):

                # Adjust the texture UV mapping
                i_object.data.texspace_size[0] = 10.0
                i_object.data.texspace_size[1] = 10.0
                i_object.data.texspace_size[2] = 10.0

            # Append the objects to the scene
            scene.objects.link(i_object)

    # Return reference to the loaded objects
    return data_dst.objects


################################################################################
# @ load_neurons
################################################################################
def load_neurons_membrane_meshes_into_scene(input_directory,
                                            neurons_list,
                                            input_type):
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
            neuron.membrane_meshes = [nmv.file.import_ply_file(input_directory, input_file_name)]

        # .obj neurons
        elif input_type == 'obj':
            input_file_name = 'neuron_%s.obj' % str(neuron.gid)
            neuron.membrane_meshes = [nmv.file.import_ply_file(input_directory, input_file_name)]
