####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv.consts


####################################################################################################
# @load_fonts
####################################################################################################
def load_fonts():
    """Loads all the fonts to the Blender system to be able to use them for the plotting."""

    # Get all the font files in the fonts directory and load them into the scene
    font_files = nmv.file.get_files_in_directory(
        directory=nmv.consts.Paths.FONTS_DIRECTORY, file_extension='ttf')
    for font_file in font_files:
        font = '%s/%s' % (nmv.consts.Paths.FONTS_DIRECTORY, font_file)
        bpy.data.fonts.load(font)
