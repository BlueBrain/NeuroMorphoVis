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


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    from .panel import NMV_SynapticsPanel
    from .ops_reconstruction import NMV_ReconstructSynaptics
    from .ops_rendering import NMV_RenderSynapticsFront
    from .ops_rendering import NMV_RenderSynapticsSide
    from .ops_rendering import NMV_RenderSynapticsTop

    # Panel
    bpy.utils.register_class(NMV_SynapticsPanel)

    # Button(s)
    bpy.utils.register_class(NMV_ReconstructSynaptics)
    bpy.utils.register_class(NMV_RenderSynapticsFront)
    bpy.utils.register_class(NMV_RenderSynapticsSide)
    bpy.utils.register_class(NMV_RenderSynapticsTop)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_SynapticsPanel
    from .ops_reconstruction import NMV_ReconstructSynaptics
    from .ops_rendering import NMV_RenderSynapticsFront
    from .ops_rendering import NMV_RenderSynapticsSide
    from .ops_rendering import NMV_RenderSynapticsTop

    # Panel
    bpy.utils.unregister_class(NMV_SynapticsPanel)

    # Button(s)
    bpy.utils.unregister_class(NMV_ReconstructSynaptics)
    bpy.utils.unregister_class(NMV_RenderSynapticsFront)
    bpy.utils.unregister_class(NMV_RenderSynapticsSide)
    bpy.utils.unregister_class(NMV_RenderSynapticsTop)

