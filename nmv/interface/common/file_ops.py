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


# Internal imports
import nmv.consts


####################################################################################################
# @verify_output_directory
####################################################################################################
def verify_output_directory(options,
                            panel=None):

    # Ensure that there is a valid directory where the images will be written to
    if options.io.output_directory is None:
        if panel is not None:
            panel.report({'ERROR'}, nmv.consts.Messages.PATH_NOT_SET)
        return False

    if not nmv.file.ops.path_exists(options.io.output_directory):
        if panel is not None:
            panel.report({'ERROR'}, nmv.consts.Messages.INVALID_OUTPUT_PATH)
        return False

    # Otherwise, the output directory is valid
    return True

