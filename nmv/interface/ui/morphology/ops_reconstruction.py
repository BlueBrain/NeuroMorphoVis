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

# System imports
import time

# Blender imports
import bpy

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.utilities
import nmv.rendering
import nmv.geometry


####################################################################################################
# NMV_ReconstructMorphologyOperator
####################################################################################################
class NMV_ReconstructMorphologyOperator(bpy.types.Operator):
    """Reconstruct & Draw the Morphology Skeleton for Visualization"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_morphology"
    bl_label = bpy.types.Scene.NMV_MorphologyButtonLabel

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        # Clear the scene
        nmv.scene.clear_scene(deep_delete=True)

        # If no morphology file is loaded, load the morphology file
        if nmv.interface.ui_morphology is None:
            loading_result = nmv.interface.ui.load_morphology(self, context.scene)
            if loading_result is None:
                self.report({'ERROR'}, 'Please select a morphology file')
                return {'FINISHED'}

        # Create a skeleton builder object to build the morphology skeleton
        start_time = time.time()
        method = nmv.interface.ui_options.morphology.reconstruction_method
        if method == nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS:
            nmv.interface.ui_morphology_builder = nmv.builders.DisconnectedSegmentsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology as a set of disconnected tubes, where each SECTION is a tube
        elif method == nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS or \
                method == nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            nmv.interface.ui_morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology as a set of spheres, where each SPHERE represents a sample
        elif method == nmv.enums.Skeleton.Method.SAMPLES:
            nmv.interface.ui_morphology_builder = nmv.builders.SamplesBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.CONNECTED_SECTIONS:
            nmv.interface.ui_morphology_builder = nmv.builders.ConnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.PROGRESSIVE:
            nmv.interface.ui_morphology_builder = nmv.builders.ProgressiveBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        elif method == nmv.enums.Skeleton.Method.DENDROGRAM:
            nmv.interface.ui_morphology_builder = nmv.builders.DendrogramBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Default: DisconnectedSectionsBuilder
        else:
            nmv.interface.ui_morphology_builder = nmv.builders.DisconnectedSectionsBuilder(
                morphology=nmv.interface.ui_morphology, options=nmv.interface.ui_options)

        # Draw the morphology skeleton and return a list of all the reconstructed objects
        nmv.interface.ui_reconstructed_skeleton = \
            nmv.interface.ui_morphology_builder.draw_morphology_skeleton(context=context)
        reconstruction_time = time.time()
        nmv.interface.ui_morphology_reconstructed = True

        context.scene.NMV_MorphologyReconstructionTime = reconstruction_time - start_time
        nmv.logger.statistics('Morphology reconstructed in [%f] seconds' %
                              context.scene.NMV_MorphologyReconstructionTime)

        # Interpolations
        scale = float(context.scene.NMV_MaximumValue) - float(context.scene.NMV_MinimumValue)
        delta = scale / float(nmv.consts.Color.COLORMAP_RESOLUTION)

        # Fill the colors list
        for color_index in range(nmv.consts.Color.COLORMAP_RESOLUTION):
            r0_value = float(context.scene.NMV_MinimumValue) + (color_index * delta)
            r1_value = float(context.scene.NMV_MinimumValue) + ((color_index + 1) * delta)
            setattr(context.scene, 'NMV_R0_Value%d' % color_index, r0_value)
            setattr(context.scene, 'NMV_R1_Value%d' % color_index, r1_value)

        # Deselect everything in the scene to be able to see the morphology
        nmv.scene.deselect_all()

        # Confirm operation done
        return {'FINISHED'}
