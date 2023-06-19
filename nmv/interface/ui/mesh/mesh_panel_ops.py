####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @draw_soma_to_arbors_connectivity
####################################################################################################
def draw_soma_to_arbors_connectivity(panel,
                                     scene):
    """Draws the options of the soma to arbors connectivity.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Meshing options reference
    meshing_options = nmv.interface.ui_options.mesh

    # The soft body soma must be used to connect the arbors
    if meshing_options.soma_type == nmv.enums.Soma.Representation.SOFT_BODY:
        soma_connection_row = panel.layout.row()
        soma_connection_row.label(text='Arbors to Soma:')
        soma_connection_row.prop(scene, 'NMV_SomaArborsConnection', expand=True)
        meshing_options.soma_connection = scene.NMV_SomaArborsConnection
    else:
        meshing_options.soma_connection = nmv.enums.Meshing.SomaConnection.DISCONNECTED


####################################################################################################
# @draw_mesh_connectivity_options
####################################################################################################
def draw_mesh_connectivity_options(panel,
                                   scene):
    """Draws the mesh connectivity options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Meshing options reference
    meshing_options = nmv.interface.ui_options.mesh

    # If the soma is connected, then by default, the arbors are connected
    if meshing_options.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
        meshing_options.neuron_objects_connection = nmv.enums.Meshing.ObjectsConnection.CONNECTED

    else:
        mesh_objects_connection_row = panel.layout.row()
        mesh_objects_connection_row.label(text='Skeleton Objects:')
        mesh_objects_connection_row.prop(scene, 'NMV_MeshObjectsConnection', expand=True)
        meshing_options.neuron_objects_connection = scene.NMV_MeshObjectsConnection





