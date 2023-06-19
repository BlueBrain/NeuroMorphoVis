###################################################################################################
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

# System imports
import os

# Blender imports
import bpy

# Internal imports
import nmv.interface


####################################################################################################
# @load_icons
####################################################################################################
def load_icons():
    """Loads the external icons to Blender to be able to use them on the panel interface."""

    nmv.interface.ui_icons = bpy.utils.previews.new()
    images_path = '%s/../../../../data/images' % os.path.dirname(os.path.realpath(__file__))
    nmv.interface.ui_icons.load("github", os.path.join(images_path, "github-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("bbp", os.path.join(images_path, "bbp-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("epfl", os.path.join(images_path, "epfl-logo.png"), 'IMAGE')
    nmv.interface.ui_icons.load("nmv", os.path.join(images_path, "nmv-logo.png"), 'IMAGE')


####################################################################################################
# @unload_icons
####################################################################################################
def unload_icons():
    """Unloads the external icons, after loading them to Blender."""

    bpy.utils.previews.remove(nmv.interface.ui_icons)