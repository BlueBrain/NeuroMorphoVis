####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
import copy
import time

# Blender imports
import bpy

# Internal imports
import nmv.enums
import nmv.interface
import nmv.scene
import nmv.utilities
import nmv.consts
from .io_panel_options import *


####################################################################################################
# @IOPanel
####################################################################################################
class IOPanel(bpy.types.Panel):
    """Input and output data panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if nmv.utilities.is_blender_280() else 'TOOLS'
    bl_idname = "OBJECT_PT_NMV_IO"
    bl_label = 'Input / Output'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Documentation button
        documentation_button = layout.column()
        documentation_button.operator('nmv.documentation_io', icon='URL')
        documentation_button.separator()

        # Input data options
        input_data_options_row = layout.row()
        input_data_options_row.label(text='Input Data Options:', icon='LIBRARY_DATA_DIRECT')

        # Input source
        input_source_row = layout.row()
        input_source_row.prop(scene, 'NMV_InputSource')

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.NMV_InputSource == nmv.enums.Input.H5_SWC_FILE:
            morphology_file_row = layout.row()
            morphology_file_row.prop(scene, 'NMV_MorphologyFile')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:

            blue_config_row = layout.row()
            blue_config_row.prop(scene, 'NMV_CircuitFile')
            gid_row = layout.row()
            gid_row.prop(scene, 'NMV_Gid')

        # Otherwise, ERROR
        else:

            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')

        import_button = layout.column()
        import_button.operator('nmv.load_morphology', icon='ANIM_DATA')
        import_button.separator()

        # Stats
        if nmv.interface.ui_morphology is not None:
            morphology_stats_row = layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            loading_time_row = layout.row()
            loading_time_row.prop(scene, 'NMV_MorphologyLoadingTime')
            loading_time_row.enabled = False

            drawing_time_row = layout.row()
            drawing_time_row.prop(scene, 'NMV_MorphologyDrawingTime')
            drawing_time_row.enabled = False

        # Output options
        output_data_options_row = layout.row()
        output_data_options_row.label(text='Output Options:', icon='SCRIPT')

        # Output directory
        output_directory_row = layout.row()
        output_directory_row.prop(scene, 'NMV_OutputDirectory')

        # Default paths
        default_paths_row = layout.row()
        default_paths_row.prop(scene, 'NMV_DefaultArtifactsRelativePath')

        # Images path
        images_path_row = layout.row()
        images_path_row.prop(scene, 'NMV_ImagesPath')

        # Sequences path
        sequences_path_row = layout.row()
        sequences_path_row.prop(scene, 'NMV_SequencesPath')

        # Meshes path
        meshes_path_row = layout.row()
        meshes_path_row.prop(scene, 'NMV_MeshesPath')

        # Morphologies path
        morphologies_path_row = layout.row()
        morphologies_path_row.prop(scene, 'NMV_MorphologiesPath')

        # Analysis path
        analysis_path_row = layout.row()
        analysis_path_row.prop(scene, 'NMV_AnalysisPath')

        # Disable the default paths selection if the use default paths flag is set
        if scene.NMV_DefaultArtifactsRelativePath:
            images_path_row.enabled = False
            sequences_path_row.enabled = False
            meshes_path_row.enabled = False
            morphologies_path_row.enabled = False
            analysis_path_row.enabled = False

        # Pass options from UI to system
        if 'Select Directory' in scene.NMV_OutputDirectory:
            nmv.interface.ui_options.io.output_directory = None
        else:
            nmv.interface.ui_options.io.output_directory = \
                scene.NMV_OutputDirectory
            nmv.interface.ui_options.io.images_directory = \
                '%s/%s' % (scene.NMV_OutputDirectory, scene.NMV_ImagesPath)
            nmv.interface.ui_options.io.sequences_directory = \
                '%s/%s' % (scene.NMV_OutputDirectory, scene.NMV_SequencesPath)
            nmv.interface.ui_options.io.morphologies_directory = \
                '%s/%s' % (scene.NMV_OutputDirectory, scene.NMV_MorphologiesPath)
            nmv.interface.ui_options.io.meshes_directory = \
                '%s/%s' % (scene.NMV_OutputDirectory, scene.NMV_MeshesPath)
            nmv.interface.ui_options.io.analysis_directory = \
                '%s/%s' % (scene.NMV_OutputDirectory, scene.NMV_AnalysisPath)


####################################################################################################
# @SketchSkeleton
####################################################################################################
class LoadMorphology(bpy.types.Operator):
    """Loads morphology
    """

    # Operator parameters
    bl_idname = "nmv.load_morphology"
    bl_label = "Load"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Rendering context
        :return:
            'FINISHED'
        """

        # Clear the scene
        import nmv.scene
        nmv.scene.ops.clear_scene()

        # By default set the background to transparent
        nmv.scene.set_transparent_background()

        # Load the images
        logo_tex = bpy.data.textures.new("nmv-logo", "IMAGE")
        logo_tex.image = bpy.data.images.load("%s/%s" % (nmv.consts.Paths.IMAGES_PATH,
                                                         'nmv-logo.png'))
        logo_tex.extension = 'CLIP'

        # Load the morphology file
        start_time = time.time()
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)
        loading_time = time.time()
        context.scene.NMV_MorphologyLoadingTime = loading_time - start_time

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        nmv.logger.header('Loading Morphology')
        nmv.logger.info('Morphology: %s' % nmv.interface.ui_morphology.label)
        nmv.logger.info('Morphology loaded in [%f] seconds' %
                        context.scene.NMV_MorphologyLoadingTime)

        # Clear the scene
        import nmv.scene
        nmv.scene.clear_scene()

        # Create a builder object to build the morphology skeleton
        import nmv.builders

        # Always use meta builder to reconstruct the initial soma
        options = copy.deepcopy(nmv.interface.ui_options)
        options.shading.set_default()

        # Create the builder
        builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=nmv.interface.ui_morphology, options=options, force_meta_ball_soma=True)
        nmv.interface.ui_reconstructed_skeleton = builder.draw_morphology_skeleton()

        drawing_time = time.time()
        context.scene.NMV_MorphologyDrawingTime = drawing_time - loading_time

        nmv.logger.header('Stats.')
        nmv.logger.info('Morphology drawn in [%f] seconds' %
                        context.scene.NMV_MorphologyDrawingTime)

        # Switch to the top view
        nmv.scene.view_axis()

        # View all the objects in the scene
        nmv.scene.ops.view_all_scene()

        # Configure the output directory
        nmv.interface.configure_output_directory(options=nmv.interface.ui_options, context=context)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        # self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Modal
        return {'RUNNING_MODAL'}

    ###############################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """
        Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

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
        """
        Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Finished
        return {'FINISHED'}


####################################################################################################
# @InputOutputDocumentation
####################################################################################################
class InputOutputDocumentation(bpy.types.Operator):
    """Open the online documentation page of the IO panel."""

    # Operator parameters
    bl_idname = "nmv.documentation_io"
    bl_label = "Online User Guide"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Input-&-Output')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Once loaded activate the mode
    nmv.scene.activate_neuromorphovis_mode()

    # InputOutput data
    bpy.utils.register_class(IOPanel)

    # Buttons
    bpy.utils.register_class(InputOutputDocumentation)
    bpy.utils.register_class(LoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Get back to the original theme
    nmv.scene.deactivate_neuromorphovis_mode()

    # InputOutput data
    bpy.utils.unregister_class(IOPanel)

    # Buttons
    bpy.utils.unregister_class(InputOutputDocumentation)
    bpy.utils.unregister_class(LoadMorphology)
