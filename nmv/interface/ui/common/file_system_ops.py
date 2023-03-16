####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import sys
import os

# Blender imports
import bpy

# Internal imports
import nmv.consts


####################################################################################################
# @configure_output_directory
####################################################################################################
def configure_output_directory(options,
                               context=None):
    """Configures the output directory after loading the data.

    :param options:
        System options.
    :param context:
        Context.
    """

    # If the output directory is not set
    if options.io.output_directory is None:

        # Suggest an output directory at the home folder
        suggested_output_folder = '%s/neuromorphovis-output' % os.path.expanduser('~')

        # Check if the output directory already exists or not
        if os.path.exists(suggested_output_folder):

            # Update the system options
            options.io.output_directory = suggested_output_folder

            # Update the UI
            context.scene.NMV_OutputDirectory = suggested_output_folder

        # Otherwise, create it
        else:

            # Try to create the directory there
            try:

                # Create the directory
                os.mkdir(suggested_output_folder)

                # Update the system options
                options.io.output_directory = suggested_output_folder

                # Update the UI
                context.scene.NMV_OutputDirectory = suggested_output_folder

            # Voila
            except ValueError:
                pass


####################################################################################################
# @validate_output_directory
####################################################################################################
def validate_output_directory(panel,
                              context_scene):
    """Validates the existence of the output directory.

    :param panel:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.

    :return
        True if the output directory is valid or False otherwise.
    """

    # Ensure that there is a valid directory where the images will be written to
    if nmv.interface.ui_options.io.output_directory is None:
        panel.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
        return False

    if not nmv.file.ops.path_exists(context_scene.NMV_OutputDirectory):
        panel.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
        return False

    # The output directory is valid
    return True
