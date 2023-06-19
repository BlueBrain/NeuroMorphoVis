####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    from .panel import NMV_AboutPanel
    from .ops import NMV_Update
    from .ops import NMV_OpenDocumentation
    from .ops import NMV_OpenRepository

    # Panel
    bpy.utils.register_class(NMV_AboutPanel)

    # Buttons
    bpy.utils.register_class(NMV_Update)
    bpy.utils.register_class(NMV_OpenRepository)
    bpy.utils.register_class(NMV_OpenDocumentation)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_AboutPanel
    from .panel import NMV_AboutPanel
    from .ops import NMV_Update
    from .ops import NMV_OpenDocumentation
    from .ops import NMV_OpenRepository

    # Panel
    bpy.utils.unregister_class(NMV_AboutPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_Update)
    bpy.utils.unregister_class(NMV_OpenRepository)
    bpy.utils.unregister_class(NMV_OpenDocumentation)
