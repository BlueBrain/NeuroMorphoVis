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

    from .panel import NMV_MorphologyPanel
    from .ops_documentation import NMV_MorphologyReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructMorphologyOperator
    from .ops_render_view import NMV_RenderMorphologyFront
    from .ops_render_view import NMV_RenderMorphologySide
    from .ops_render_view import NMV_RenderMorphologyTop
    from .ops_render_360 import NMV_RenderMorphology360
    from .ops_render_progressive import NMV_RenderMorphologyProgressive
    from .ops_exports import NMV_ExportMorphologySWC
    from .ops_exports import NMV_ExportMorphologySegments
    from .ops_exports import NMV_ExportMorphologyBLEND

    # Soma reconstruction panel
    bpy.utils.register_class(NMV_MorphologyPanel)

    # Buttons
    bpy.utils.register_class(NMV_MorphologyReconstructionDocumentation)
    bpy.utils.register_class(NMV_ReconstructMorphologyOperator)
    bpy.utils.register_class(NMV_RenderMorphologyFront)
    bpy.utils.register_class(NMV_RenderMorphologySide)
    bpy.utils.register_class(NMV_RenderMorphologyTop)
    bpy.utils.register_class(NMV_RenderMorphology360)
    bpy.utils.register_class(NMV_RenderMorphologyProgressive)
    bpy.utils.register_class(NMV_ExportMorphologySWC)
    bpy.utils.register_class(NMV_ExportMorphologySegments)
    bpy.utils.register_class(NMV_ExportMorphologyBLEND)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_MorphologyPanel
    from .ops_documentation import NMV_MorphologyReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructMorphologyOperator
    from .ops_render_view import NMV_RenderMorphologyFront
    from .ops_render_view import NMV_RenderMorphologySide
    from .ops_render_view import NMV_RenderMorphologyTop
    from .ops_render_360 import NMV_RenderMorphology360
    from .ops_render_progressive import NMV_RenderMorphologyProgressive
    from .ops_exports import NMV_ExportMorphologySWC
    from .ops_exports import NMV_ExportMorphologySegments
    from .ops_exports import NMV_ExportMorphologyBLEND

    # Morphology reconstruction panel
    bpy.utils.unregister_class(NMV_MorphologyPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_MorphologyReconstructionDocumentation)
    bpy.utils.unregister_class(NMV_ReconstructMorphologyOperator)
    bpy.utils.unregister_class(NMV_RenderMorphologyTop)
    bpy.utils.unregister_class(NMV_RenderMorphologySide)
    bpy.utils.unregister_class(NMV_RenderMorphologyFront)
    bpy.utils.unregister_class(NMV_RenderMorphology360)
    bpy.utils.unregister_class(NMV_RenderMorphologyProgressive)
    bpy.utils.unregister_class(NMV_ExportMorphologySWC)
    bpy.utils.unregister_class(NMV_ExportMorphologySegments)
    bpy.utils.unregister_class(NMV_ExportMorphologyBLEND)

