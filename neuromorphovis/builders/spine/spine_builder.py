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
import random

# Blender imports
import bpy
from mathutils import Vector
from mathutils import Matrix

# Internal modules
#import file_ops
#import importers
#import scene_ops
#import time_line
#import timer
#import utilities

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.file
import neuromorphovis.scene
import neuromorphovis.utilities

####################################################################################################
# @load_spine
####################################################################################################
def load_spine(spines_directory,
               spine_file):
    """Load a spine mesh to the scene from a given directory and returns a reference to it.

    :param spines_directory:
        A given directory of spines.
    :param spine_file:
        A given spine file.
    :return:
        A reference to the loaded spine into the scene.
    """

    # Load the spine into a blender object
    spine_object = nmv.file.import_obj_file( spines_directory, spine_file)

    # Return a reference to it
    return spine_object


####################################################################################################
# @load_spines
####################################################################################################
def load_spines(spines_directory):
    """Load all the spines in a certain directory and return a list of all of them.

    :param spines_directory:
        A given directory where the spines are located.
    :return:
        A list of all the loaded spines.
    """

    # List all the obj files in the directory
    spines_files = nmv.file.ops.get_files_in_directory(spines_directory, file_extension='.obj')

    # Load the spines, one by one into a list
    spines_objects_list = []

    # Load spine by spine
    for spine_file in spines_files:

        # Load the spine
        spine_object = load_spine(spines_directory, spine_file)

        # TODO: Tessellate the spines if needed

        # Append the spine to the list
        spines_objects_list.append(spine_object)

    # Return the spines list
    return spines_objects_list


####################################################################################################
# @emanate_a_spine
####################################################################################################
def emanate_a_spine(spines_list,
                    post_synaptic_position,
                    pre_synaptic_position,
                    id):
    """Emanate a spine at the specified position and towards the direction given by the pre and post
    synaptic positions.

    :param spines_list:
        A list of all the loaded spines
    :param post_synaptic_position:
        The post-synaptic position of the spine.
    :param pre_synaptic_position:
        The pre-synaptic position of the spine.
    :param id :
        The spine identifier.
    :return:
        A reference to the spine object.
    """

    # Select a random spine from the spines list
    spine_template = random.choice(spines_list)

    # Get a copy of the template and update it
    spine_object = nmv.scene.ops.duplicate_object(spine_template, id)

    # Scale the spine
    nmv.scene.ops.scale_object_uniformly(spine_object, random.uniform(0.6, 1.25))

    # Translate the spine to the post synaptic position
    nmv.scene.ops.set_object_location(spine_object, post_synaptic_position)

    # Rotate the spine towards the pre-synaptic point
    nmv.scene.ops.rotate_object_towards_target(
        spine_object, post_synaptic_position, pre_synaptic_position)

    # Return a reference to the spine
    return spine_object


####################################################################################################
# @build_circuit_spines
####################################################################################################
def build_circuit_spines(morphology,
                         blue_config,
                         gid):
    """Builds all the spines on a spiny neuron using a BBP circuit.

    :param morphology:
        A given morphology.
    :param blue_config:
        BBP circuit configuration file.
    :param gid:
        Neuron gid.
    :return:
        A list of all the reconstructed spines along the neuron.
    """

    # Keep a list of all the spines objects
    spines_objects = []

    # Import brain
    import brain

    # Load the circuit, silently please
    circuit = brain.Circuit(blue_config)

    # Get all the synapses for the corresponding gid.
    synapses = circuit.afferent_synapses({int(gid)})

    # Load all the template spines and ignore the verbose messages of loading
    templates_spines_list = load_spines(nmv.consts.Paths.SPINES_MESHES_DIRECTORY)

    # Get the local to global transforms
    local_to_global_transform = circuit.transforms({int(gid)})[0]

    # Print(local_to_global_transform)
    transformation_matrix = Matrix()
    for i in range(4):
        transformation_matrix[i][:] = local_to_global_transform[i]

    # Invert the transformation matrix
    transformation_matrix = transformation_matrix.inverted()

    # Create a timer to report the performance
    building_timer = nmv.utilities.timer.Timer()

    nmv.logger.log('Building spines')
    building_timer.start()

    # Load the synapses from the file
    number_spines = len(synapses)
    for i, synapse in enumerate(synapses):

        # Show progress
        nmv.utilities.time_line.show_iteration_progress('Spines', i, number_spines)

        """ Ignore soma synapses """
        # If the post-synaptic section id is zero, then revoke it, and continue
        post_section_id = synapse.post_section()
        if post_section_id == 0: continue

        # Get the pre-and post-positions in the global coordinates
        pre_position = synapse.pre_surface_position()
        post_position = synapse.post_surface_position()

        # Convert them to a mathutils.Vector
        """
        pre_position = Vector((pre_position.x(), pre_position.y(), pre_position.z()))
        post_position = Vector((post_position.x(), post_position.y(), post_position.z()))
        """

        # Transform the spine positions to the circuit coordinates
        pre_position = Vector((pre_position[0], pre_position[1], pre_position[2]))
        post_position = Vector((post_position[0], post_position[1], post_position[2]))
        post_position = transformation_matrix * post_position
        pre_position = transformation_matrix * pre_position

        # Emanate a spine
        spine_object = emanate_a_spine(templates_spines_list, post_position, pre_position, i)

        # Add the object to the list
        spines_objects.append(spine_object)

    # Done
    nmv.utilities.time_line.show_iteration_progress('Spines', number_spines, number_spines, done=True)

    # Report the time
    building_timer.end()
    nmv.logger.log('\t Spines: [%f] seconds' % building_timer.duration())

    # Delete the template spines
    nmv.scene.ops.delete_list_objects(templates_spines_list)

    # Return the spines objects list
    return spines_objects

