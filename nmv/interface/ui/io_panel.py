####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import os

# Blender imports
import bpy
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty

# Internal imports
import nmv
import nmv.enums
import nmv.interface
import nmv.scene
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
    bl_region_type = 'TOOLS'
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

        # Input data options
        input_data_options_row = layout.row()
        input_data_options_row.label(text='Input Data Options:', icon='LIBRARY_DATA_DIRECT')

        # Input source
        input_source_row = layout.row()
        input_source_row.prop(scene, 'InputSource')

        # Read the data from a given morphology file either in .h5 or .swc formats
        if bpy.context.scene.InputSource == nmv.enums.Input.H5_SWC_FILE:
            morphology_file_row = layout.row()
            morphology_file_row.prop(scene, 'MorphologyFile')

        # Read the data from a specific gid in a given circuit
        elif bpy.context.scene.InputSource == nmv.enums.Input.CIRCUIT_GID:

            blue_config_row = layout.row()
            blue_config_row.prop(scene, 'CircuitFile')
            gid_row = layout.row()
            gid_row.prop(scene, 'Gid')

        # Otherwise, ERROR
        else:

            # Report an invalid input source
            self.report({'ERROR'}, 'Invalid Input Source')

        import_button = layout.column()
        import_button.operator('load.morphology', icon='ANIM_DATA')
        import_button.separator()

        # Output options
        output_data_options_row = layout.row()
        output_data_options_row.label(text='Output Options:', icon='SCRIPT')

        # Output directory
        output_directory_row = layout.row()
        output_directory_row.prop(scene, 'OutputDirectory')

        # Default paths
        default_paths_row = layout.row()
        default_paths_row.prop(scene, 'DefaultArtifactsRelativePath')

        # Images path
        images_path_row = layout.row()
        images_path_row.prop(scene, 'ImagesPath')

        # Sequences path
        sequences_path_row = layout.row()
        sequences_path_row.prop(scene, 'SequencesPath')

        # Meshes path
        meshes_path_row = layout.row()
        meshes_path_row.prop(scene, 'MeshesPath')

        # Morphologies path
        morphologies_path_row = layout.row()
        morphologies_path_row.prop(scene, 'MorphologiesPath')

        # Analysis path
        analysis_path_row = layout.row()
        analysis_path_row.prop(scene, 'AnalysisPath')

        # Disable the default paths selection if the use default paths flag is set
        if scene.DefaultArtifactsRelativePath:
            images_path_row.enabled = False
            sequences_path_row.enabled = False
            meshes_path_row.enabled = False
            morphologies_path_row.enabled = False
            analysis_path_row.enabled = False

        # Pass options from UI to system
        if 'Select Directory' in scene.OutputDirectory:
            nmv.interface.ui_options.io.output_directory = None
        else:
            nmv.interface.ui_options.io.output_directory = \
                scene.OutputDirectory
            nmv.interface.ui_options.io.images_directory = \
                '%s/%s' % (scene.OutputDirectory, scene.ImagesPath)
            nmv.interface.ui_options.io.sequences_directory = \
                '%s/%s' % (scene.OutputDirectory, scene.SequencesPath)
            nmv.interface.ui_options.io.morphologies_directory = \
                '%s/%s' % (scene.OutputDirectory, scene.MorphologiesPath)
            nmv.interface.ui_options.io.meshes_directory = \
                '%s/%s' % (scene.OutputDirectory, scene.MeshesPath)
            nmv.interface.ui_options.io.analysis_directory = \
                '%s/%s' % (scene.OutputDirectory, scene.AnalysisPath)


####################################################################################################
# @SketchSkeleton
####################################################################################################
class LoadMorphology(bpy.types.Operator):
    """Loads morphology
    """

    # Operator parameters
    bl_idname = "load.morphology"
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
        nmv.scene.ops.clear_scene()

        # Load the images
        images_path = '%s/../../../data/images' % os.path.dirname(os.path.realpath(__file__))
        nmv_logo_tex = bpy.data.textures.new("nmv-logo", "IMAGE")
        nmv_logo_tex.image = bpy.data.images.load("%s/%s" % (images_path, 'nmv-logo.png'))
        nmv_logo_tex.extension = 'CLIP'

        # Load the morphology file
        loading_result = nmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Plot the morphology (whatever issues it contains)
        nmv.interface.ui_options.morphology.reconstruction_method = \
            nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS
        nmv.interface.ui.sketch_morphology_skeleton_guide(
            morphology=nmv.interface.ui_morphology,
            options=copy.deepcopy(nmv.interface.ui_options))

        # Switch to the orthographic mode
        bpy.ops.view3d.view_persportho()

        # Switch to the top view
        bpy.ops.view3d.viewnumpad(type='TOP')

        # View all the objects in the scene
        bpy.ops.view3d.view_all()

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Load the icons
    nmv.interface.load_icons()

    # InputOutput data
    bpy.utils.register_class(IOPanel)

    # Buttons
    bpy.utils.register_class(LoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Unload the icons
    nmv.interface.unload_icons()

    # InputOutput data
    bpy.utils.unregister_class(IOPanel)

    # Buttons
    bpy.utils.unregister_class(LoadMorphology)
