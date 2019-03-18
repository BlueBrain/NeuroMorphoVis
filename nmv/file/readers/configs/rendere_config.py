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

# Internal imports
import nmv
import nmv.scene


####################################################################################################
# @read_neurorender_config
####################################################################################################
def read_neurorender_config(config_file_path):
    """Read a neurorender configuration file and return a list of data.

    :param config_file_path:
        The path to the configuration file.
    :return:
        A list of all the structures that will be rendered.
    """

    # Load the config file into a list
    config_data = list()
    file_handle = open(config_file_path, 'r')
    for line in file_handle: config_data.append(line)
    file_handle.close()

    neurorender_data = list()

    # Iterate on the list and parse the objects
    index = 0
    while True:

        if 'Neuron' in config_data[index]:

            # Get the neuron data object and append it to the list

            pass

    return neurorender_data

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


