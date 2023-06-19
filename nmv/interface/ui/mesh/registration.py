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

    from .panel import NMV_MeshPanel
    from .ops_documentation import NMV_MeshReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructNeuronMesh
    from .ops_render_view import NMV_RenderMeshFront
    from .ops_render_view import NMV_RenderMeshSide
    from .ops_render_view import NMV_RenderMeshTop
    from .ops_render_360 import NMV_RenderMesh360
    from .ops_exports import NMV_ExportMesh

    # Mesh reconstruction panel
    bpy.utils.register_class(NMV_MeshPanel)

    # Buttons
    bpy.utils.register_class(NMV_MeshReconstructionDocumentation)
    bpy.utils.register_class(NMV_ReconstructNeuronMesh)
    bpy.utils.register_class(NMV_RenderMeshFront)
    bpy.utils.register_class(NMV_RenderMeshSide)
    bpy.utils.register_class(NMV_RenderMeshTop)
    bpy.utils.register_class(NMV_RenderMesh360)
    bpy.utils.register_class(NMV_ExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    from .panel import NMV_MeshPanel
    from .ops_documentation import NMV_MeshReconstructionDocumentation
    from .ops_reconstruction import NMV_ReconstructNeuronMesh
    from .ops_render_view import NMV_RenderMeshFront
    from .ops_render_view import NMV_RenderMeshSide
    from .ops_render_view import NMV_RenderMeshTop
    from .ops_render_360 import NMV_RenderMesh360
    from .ops_exports import NMV_ExportMesh

    # Mesh reconstruction panel
    bpy.utils.unregister_class(NMV_MeshPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_MeshReconstructionDocumentation)
    bpy.utils.unregister_class(NMV_ReconstructNeuronMesh)
    bpy.utils.unregister_class(NMV_RenderMeshFront)
    bpy.utils.unregister_class(NMV_RenderMeshSide)
    bpy.utils.unregister_class(NMV_RenderMeshTop)
    bpy.utils.unregister_class(NMV_RenderMesh360)
    bpy.utils.unregister_class(NMV_ExportMesh)
