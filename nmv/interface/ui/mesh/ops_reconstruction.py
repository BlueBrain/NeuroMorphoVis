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

# System imports
import time

# Blender imports
import bpy

# Internal imports
import nmv.scene
import nmv.enums
import nmv.builders
import nmv.interface


####################################################################################################
# @NMV_ReconstructNeuronMesh
####################################################################################################
class NMV_ReconstructNeuronMesh(bpy.types.Operator):
    """Reconstructs the mesh of the neuron"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_mesh"
    bl_label = "Reconstruct Mesh"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Clear the scene
        nmv.scene.clear_scene()

        # If no morphology file is loaded, load the morphology file
        if nmv.interface.ui_morphology is None:
            loading_result = nmv.interface.ui.load_morphology(self, context.scene)
            if loading_result is None:
                self.report({'ERROR'}, 'Please select a morphology file')
                return {'FINISHED'}

        # Meshing technique
        meshing_technique = nmv.interface.ui_options.mesh.meshing_technique

        # Start reconstruction
        start_time = time.time()

        # Piece-wise watertight meshing
        if meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            mesh_builder = nmv.builders.PiecewiseBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == nmv.enums.Meshing.Technique.VOXELIZATION:
            mesh_builder = nmv.builders.VoxelizationBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == nmv.enums.Meshing.Technique.UNION:
            mesh_builder = nmv.builders.UnionBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Skinning
        elif meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
            mesh_builder = nmv.builders.SkinningBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Meta Balls
        elif meshing_technique == nmv.enums.Meshing.Technique.META_OBJECTS:
            mesh_builder = nmv.builders.MetaBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)
            nmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        else:

            # Invalid method
            self.report({'ERROR'}, 'Invalid Meshing Technique')
            return {'FINISHED'}

        # Update the timing
        reconstruction_time = time.time()
        nmv.interface.ui_mesh_reconstructed = True
        context.scene.NMV_MeshReconstructionTime = reconstruction_time - start_time
        nmv.logger.statistics('Mesh reconstructed in [%f] seconds' %
                              context.scene.NMV_MeshReconstructionTime)

        # Deselect everything in the scene to be able to see the morphology
        nmv.scene.deselect_all()

        # Operation done
        return {'FINISHED'}





