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

    from .panel import NMV_EditPanel
    from .ops_documentation import NMV_MorphologyEditingDocumentation
    from .ops_edit import NMV_SketchSkeleton
    from .ops_edit import NMV_EditMorphologyCoordinates
    from .ops_edit import NMV_UpdateMorphologyCoordinates
    from .ops_export import NMV_ExportMorphologySWC

    # Morphology analysis panel
    bpy.utils.register_class(NMV_EditPanel)

    # Buttons
    bpy.utils.register_class(NMV_MorphologyEditingDocumentation)
    bpy.utils.register_class(NMV_SketchSkeleton)
    bpy.utils.register_class(NMV_EditMorphologyCoordinates)
    bpy.utils.register_class(NMV_UpdateMorphologyCoordinates)
    bpy.utils.register_class(NMV_ExportMorphologySWC)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_EditPanel
    from .ops_documentation import NMV_MorphologyEditingDocumentation
    from .ops_edit import NMV_SketchSkeleton
    from .ops_edit import NMV_EditMorphologyCoordinates
    from .ops_edit import NMV_UpdateMorphologyCoordinates
    from .ops_export import NMV_ExportMorphologySWC

    # Morphology analysis panel
    bpy.utils.unregister_class(NMV_EditPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_MorphologyEditingDocumentation)
    bpy.utils.unregister_class(NMV_SketchSkeleton)
    bpy.utils.unregister_class(NMV_EditMorphologyCoordinates)
    bpy.utils.unregister_class(NMV_UpdateMorphologyCoordinates)
    bpy.utils.unregister_class(NMV_ExportMorphologySWC)
