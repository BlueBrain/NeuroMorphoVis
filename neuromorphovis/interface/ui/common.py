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
import neuromorphovis as nmv
import neuromorphovis.enums
import neuromorphovis.interface

# A global variable to notify us if a new morphology has been loaded to the system or not
current_morphology_label = None


####################################################################################################
# @load_morphology
####################################################################################################
def load_morphology(panel_object,
                    context_scene):
    """Load a given morphology from file.

    :param panel_object:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.
    """

    global current_morphology_label
    # Read the data from a given morphology file either in .h5 or .swc formats
    if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:

        # Pass options from UI to system
        nmv.interface.ui_options.morphology.morphology_file_path = context_scene.MorphologyFile

        # Update the morphology label
        nmv.interface.ui_options.morphology.label = nmv.file.ops.get_file_name_from_path(
            context_scene.MorphologyFile)

        # Check if the morphology is loaded before or not
        if current_morphology_label is None:
            current_morphology_label = nmv.interface.ui_options.morphology.label
        else:
            if current_morphology_label == nmv.interface.ui_options.morphology.label:
                return

        # Load the morphology from the file
        loading_flag, morphology_object = nmv.file.readers.read_morphology_from_file(
            options=nmv.interface.ui_options)

        # Verify the loading operation
        if loading_flag:

            # Update the morphology
            nmv.interface.ui_morphology = morphology_object

        # Otherwise, report an ERROR
        else:
            panel_object.report({'ERROR'}, 'Invalid Morphology File')

    # Read the data from a specific gid in a given circuit
    elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:

        # Pass options from UI to system
        nmv.interface.ui_options.morphology.blue_config = context_scene.CircuitFile
        nmv.interface.ui_options.morphology.gid = context_scene.Gid

        # Update the morphology label
        nmv.interface.ui_options.morphology.label = 'neuron_' + str(context_scene.Gid)

        # Check if the morphology is loaded before or not
        if current_morphology_label is None:
            current_morphology_label = nmv.interface.ui_options.morphology.label
        else:
            if current_morphology_label == nmv.interface.ui_options.morphology.label:
                return

        # Load the morphology from the circuit
        loading_flag, morphology_object = nmv.file.readers.BBPReader.load_morphology_from_circuit(
                blue_config=nmv.interface.ui_options.morphology.blue_config,
                gid=nmv.interface.ui_options.morphology.gid)

        # Verify the loading operation
        if loading_flag:

            # Update the morphology
            nmv.interface.ui_morphology = morphology_object

        # Otherwise, report an ERROR
        else:
            panel_object.report({'ERROR'}, 'Cannot Load Morphology from Circuit')

    else:
        # Report an invalid input source
        panel_object.report({'ERROR'}, 'Invalid Input Source')