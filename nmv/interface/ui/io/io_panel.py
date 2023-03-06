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
import copy
import time

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.interface
import nmv.scene
import nmv.utilities
from .io_panel_options import *
from .io_panel_ops import *


####################################################################################################
# @NMV_IOPanel
####################################################################################################
class NMV_IOPanel(bpy.types.Panel):
    """The input and output data panel of NeuroMorphoVis"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_IO"
    bl_label = 'Input / Output'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Blender context.
        """

        # Draw the documentation button
        documentation_button_row = self.layout.column()
        documentation_button_row.operator('nmv.documentation_io', icon='URL')
        documentation_button_row.separator()

        # Draw the input options
        draw_input_options(panel=self, scene=context.scene, options=nmv.interface.ui_options)

        # Draw the morphology loading button
        draw_morphology_loading_button(panel=self)

        # Draw the morphology loading statistics elements, if possible after loading the morphology
        draw_morphology_loading_statistics(
            panel=self, scene=context.scene, morphology_object=nmv.interface.ui_morphology)

        # Draw the output options
        draw_output_options(panel=self, scene=context.scene, options=nmv.interface.ui_options)


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
    def execute(self,
                context):
        """Execute the button, or the operator. Note that the analysis of the loaded morphology
        is executed in the background.

        :param context:
            Blender context
        :return:
             {'RUNNING_MODAL'}
        """

        # Clear the scene
        import nmv.scene
        nmv.scene.clear_scene()

        # By default, set the background to transparent
        nmv.scene.set_transparent_background()

        # Load the images
        logo_tex = bpy.data.textures.new("nmv-logo", "IMAGE")
        logo_tex.image = bpy.data.images.load(
            "%s/%s" % (nmv.consts.Paths.IMAGES_PATH, 'nmv-logo.png'))
        logo_tex.extension = 'CLIP'

        # Initialize all the operations that needs to run once and for all
        import nmv.interface
        if not nmv.interface.ui.Globals.nmv_initialized:
            nmv.interface.load_fonts()

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
        options.morphology.set_default()
        options.shading.set_default()

        # Use branching order of 2 for the axons to ensure that we can see the whole morphology,
        # while use the entire branching order for the astrocytes to ensure that it is connected
        if nmv.interface.ui_morphology.is_astrocyte:
            options.morphology.axon_branch_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
        else:
            options.morphology.axon_branch_order = 2

        # Create the builder
        builder = nmv.builders.DisconnectedSectionsBuilder(
            morphology=nmv.interface.ui_morphology, options=options, force_meta_ball_soma=False)
        nmv.interface.ui_reconstructed_skeleton = builder.draw_morphology_skeleton()

        drawing_time = time.time()
        context.scene.NMV_MorphologyDrawingTime = drawing_time - loading_time

        nmv.logger.header('Stats.')
        nmv.logger.info('Morphology drawn in [%f] seconds' %
                        context.scene.NMV_MorphologyDrawingTime)

        # Switch to the top view
        nmv.scene.view_axis()

        # View all the objects in the scene
        # if not nmv.interface.ui.Globals.nmv_initialized:
        nmv.scene.ops.view_all_scene()

        # Configure the output directory
        nmv.interface.configure_output_directory(options=nmv.interface.ui_options, context=context)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        # self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        #
        if not nmv.interface.ui.Globals.nmv_initialized:
            nmv.interface.ui.Globals.nmv_initialized = True





        from mathutils import Vector
        from random import uniform

        # UI color elements for the color map
        if nmv.consts.Circuit.MTYPES is not None:
            for i in range(len(nmv.consts.Circuit.MTYPES)):
                r = uniform(0, 1)
                g = uniform(0, 1)
                b = uniform(0, 1)

                setattr(bpy.types.Scene, 'NMV_MtypeColor_%d' % i,
                        bpy.props.FloatVectorProperty(
                            name='%s' % nmv.consts.Circuit.MTYPES[i],
                            subtype='COLOR', default=Vector((r, g, b)), min=0.0, max=1.0,
                            description=''))

        # UI color elements for the color map
        if nmv.consts.Circuit.ETYPES is not None:
            for i in range(len(nmv.consts.Circuit.ETYPES)):
                r = uniform(0, 1)
                g = uniform(0, 1)
                b = uniform(0, 1)

                setattr(bpy.types.Scene, 'NMV_EtypeColor_%d' % i,
                        bpy.props.FloatVectorProperty(
                            name='%s' % nmv.consts.Circuit.ETYPES[i],
                            subtype='COLOR', default=Vector((r, g, b)), min=0.0, max=1.0,
                            description=''))





        # Modal
        return {'RUNNING_MODAL'}

    ###############################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """Threading and non-blocking handling.

        :param context:
            The Blender context.
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
    def cancel(self,
               context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context:
            The Blender context.
        """

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
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            The Blender context.
        :return:
            {'FINISHED'}
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Input-&-Output')
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Once loaded, activate the mode rendering mode in the viewport
    nmv.scene.activate_neuromorphovis_mode()

    # Input/Output panel
    bpy.utils.register_class(NMV_IOPanel)

    # Buttons
    bpy.utils.register_class(NMV_InputOutputDocumentation)
    bpy.utils.register_class(NMV_LoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Get back to the original theme
    nmv.scene.deactivate_neuromorphovis_mode()

    # Input/Output panel
    bpy.utils.unregister_class(NMV_IOPanel)

    # Buttons
    bpy.utils.unregister_class(NMV_InputOutputDocumentation)
    bpy.utils.unregister_class(NMV_LoadMorphology)
