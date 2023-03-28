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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.scene


####################################################################################################
# @NMV_LoadMorphology
####################################################################################################
class NMV_LoadMorphology(bpy.types.Operator):
    """Loads the morphology into the Blender scene"""

    # Operator parameters
    bl_idname = "nmv.load_morphology"
    bl_label = "Load Morphology"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        import nmv.interface
        import nmv.builders

        # Load the morphology
        start_time = time.time()
        loading_result = nmv.interface.ui.load_morphology(panel=self, scene=context.scene)
        loading_time = time.time()
        context.scene.NMV_MorphologyLoadingTime = loading_time - start_time

        # If the loading result is None, terminate the loading process, ERROR handling is done
        # within the scope of the function @nmv.interface.ui.load_morphology
        if loading_result is None:
            return {'FINISHED'}

        # If the morphology is successfully loaded
        nmv.logger.header('Loading Morphology')
        nmv.logger.info('Morphology: %s' % nmv.interface.ui_morphology.label)
        nmv.logger.info('Morphology loaded in [%f] seconds' %
                        context.scene.NMV_MorphologyLoadingTime)

        # Get ready to draw the morphology to the scene, therefore clear the scene
        nmv.scene.clear_scene()

        # By default, set the background to transparent
        nmv.scene.set_transparent_background()

        # Initialize all the operations that needs to run once and for all
        if not nmv.interface.ui.globals.nmv_initialized:
            nmv.interface.load_fonts()

        # Always use meta builder to reconstruct the initial soma
        options = copy.deepcopy(nmv.interface.ui_options)
        options.morphology.set_default()
        options.shading.set_default()

        # Use branching order of 2 for the axons to ensure that we can see the whole morphology,
        # while use the entire branching order for the astrocytes to ensure that it is connected
        if nmv.interface.ui_morphology.is_astrocyte:
            options.morphology.axon_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
        else:
            options.morphology.axon_branch_order = 1

        # Create the builder
        builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=nmv.interface.ui_morphology, options=options, force_meta_ball_soma=False)
        nmv.interface.ui_reconstructed_skeleton = builder.draw_morphology_skeleton()

        drawing_time = time.time()
        context.scene.NMV_MorphologyDrawingTime = drawing_time - loading_time

        nmv.logger.header('Stats.')
        nmv.logger.info('Morphology drawn in [%f] seconds' %
                        context.scene.NMV_MorphologyDrawingTime)

        # Switch to the top view, to make the user realize that this is a new morphology
        nmv.scene.view_axis()

        # View all the objects in the scene
        # if not nmv.interface.ui.Globals.nmv_initialized:
        nmv.scene.ops.view_all_scene()

        # Configure the output directory
        nmv.interface.configure_output_directory(options=nmv.interface.ui_options, context=context)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        wm.modal_handler_add(self)

        # Switch the initialization flag to be able to use the add-on in the rest of the panel
        if not nmv.interface.ui.globals.nmv_initialized:
            nmv.interface.ui.globals.nmv_initialized = True

        # Initialize other relevant information that could be required later
        nmv.interface.initialize_relevant_parameters(scene=context.scene)

        # Modal
        return {'RUNNING_MODAL'}

    ###############################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):

        # Analyze the morphology once loaded as well
        analysis_time = time.time()
        nmv.interface.analyze_morphology(morphology=nmv.interface.ui_morphology, context=context)
        nmv.logger.info_done('Morphology analyzed in [%f] seconds' % (time.time() - analysis_time))

        # Done
        return {'FINISHED'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):

        # Finished
        return {'FINISHED'}


####################################################################################################
# @NMV_InputOutputDocumentation
####################################################################################################
class NMV_InputOutputDocumentation(bpy.types.Operator):
    """Open the online documentation page of the IO panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_io"
    bl_label = "Online User Guide"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Input-&-Output')
        return {'FINISHED'}
