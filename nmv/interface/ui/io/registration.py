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

# Blender imports
import bpy

# Internal imports
import nmv.scene


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Once loaded, activate the mode rendering mode in the viewport
    nmv.scene.activate_neuromorphovis_mode()

    from .panel import NMV_IOPanel
    from .ops import NMV_InputOutputDocumentation
    from .ops import NMV_LoadMorphology

    # Input/Output panel
    bpy.utils.register_class(NMV_IOPanel)

    # Buttons
    bpy.utils.register_class(NMV_InputOutputDocumentation)
    bpy.utils.register_class(NMV_LoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Get back to the original theme
    nmv.scene.deactivate_neuromorphovis_mode()

    from .panel import NMV_IOPanel
    from .ops import NMV_InputOutputDocumentation
    from .ops import NMV_LoadMorphology

    # Input/Output panel
    bpy.utils.unregister_class(NMV_IOPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_InputOutputDocumentation)
    bpy.utils.unregister_class(NMV_LoadMorphology)
