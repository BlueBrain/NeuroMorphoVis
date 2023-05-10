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

# Blender imports
import bpy


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    from .panel import NMV_SomaPanel
    from .ops_documentation import SomaReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructSoma

    from .ops_render_view import NMV_RenderSomaFront
    from .ops_render_view import NMV_RenderSomaSide
    from .ops_render_view import NMV_RenderSomaTop
    from .ops_render_360 import NMV_RenderSoma360
    from .ops_render_progressive import NMV_RenderSomaProgressive
    from .ops_export import NMV_ExportSomaMesh

    # Panel
    bpy.utils.register_class(NMV_SomaPanel)

    # Buttons
    bpy.utils.register_class(SomaReconstructionDocumentation)
    bpy.utils.register_class(NMV_ReconstructSoma)
    bpy.utils.register_class(NMV_RenderSomaFront)
    bpy.utils.register_class(NMV_RenderSomaSide)
    bpy.utils.register_class(NMV_RenderSomaTop)
    bpy.utils.register_class(NMV_RenderSoma360)
    bpy.utils.register_class(NMV_RenderSomaProgressive)
    bpy.utils.register_class(NMV_ExportSomaMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_SomaPanel
    from .ops_documentation import SomaReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructSoma
    from .ops_render_view import NMV_RenderSomaFront
    from .ops_render_view import NMV_RenderSomaSide
    from .ops_render_view import NMV_RenderSomaTop
    from .ops_render_360 import NMV_RenderSoma360
    from .ops_render_progressive import NMV_RenderSomaProgressive
    from .ops_export import NMV_ExportSomaMesh

    # Panel
    bpy.utils.unregister_class(NMV_SomaPanel)

    # Buttons
    bpy.utils.unregister_class(SomaReconstructionDocumentation)
    bpy.utils.unregister_class(NMV_ReconstructSoma)
    bpy.utils.unregister_class(NMV_RenderSomaFront)
    bpy.utils.unregister_class(NMV_RenderSomaSide)
    bpy.utils.unregister_class(NMV_RenderSomaTop)
    bpy.utils.unregister_class(NMV_RenderSoma360)
    bpy.utils.unregister_class(NMV_RenderSomaProgressive)
    bpy.utils.unregister_class(NMV_ExportSomaMesh)
