####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender imports
import bpy
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.enums
import neuromorphovis.interface


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
    bl_context = 'objectmode'
    bl_category = 'NeuroMorphoVis'

    ################################################################################################
    # Panel options
    ################################################################################################
    # Input options (what is the input source)
    bpy.types.Scene.InputSource = EnumProperty(
        items=[(nmv.enums.Input.H5_SWC_FILE,
                'H5 or SWC File',
                'Load individual h5 or swc file without a circuit'),
               (nmv.enums.Input.CIRCUIT_GID,
                'BBP Circuit (GID)',
                'Load a specific GID from the circuit config')], 
        name="Input Source",
        default=nmv.enums.Input.H5_SWC_FILE)
    
    # Morphology file 
    bpy.types.Scene.MorphologyFile = StringProperty(
        name="Morphology File",
        description="Select a specific morphology to mesh",
        default="Select Morphology", maxlen=2048,  subtype='FILE_PATH')
    
    # Morphology directory 
    bpy.types.Scene.MorphologyDirectory = StringProperty(
        name="Morphology Directory",
        description="Select a directory to mesh all the morphologies in it",
        default="Select Directory", maxlen=2048, subtype='DIR_PATH')

    # Circuit file or BlueConfig
    bpy.types.Scene.CircuitFile = StringProperty(
        name="Circuit File",
        description="Select a BBP circuit file (or blue config)",
        default="Select Circuit File", maxlen=2048, subtype='FILE_PATH')

    # Circuit target 
    bpy.types.Scene.Target = StringProperty(
        name="Target",
        description="Select a specific target that must exist in the circuit",
        default="Add Target", maxlen=1024)

    # Neuron GID
    bpy.types.Scene.Gid = StringProperty(
        name="GID",
        description="Select a specific GID in the circuit",
        default="Add a GID", maxlen=1024)

    # Output directory
    bpy.types.Scene.OutputDirectory = StringProperty(
        name="Output Directory",
        description="Select a directory where the results will be generated",
        default="Select Directory", maxlen=5000, subtype='DIR_PATH')

    # Use default paths for the artifacts
    bpy.types.Scene.DefaultArtifactsRelativePath = BoolProperty(
        name="Use Default Output Paths",
        description="Use the default sub-paths for the artifacts",
        default=True)

    # Images relative path
    bpy.types.Scene.ImagesPath = StringProperty(
        name="Images",
        description="Relative path where the images will be generated",
        default="images", maxlen=1000)

    # Sequences relative path
    bpy.types.Scene.SequencesPath = StringProperty(
        name="Sequences",
        description="Relative path where the sequences will be generated",
        default="sequences", maxlen=1000)

    # Meshes relative path
    bpy.types.Scene.MeshesPath = StringProperty(
        name="Meshes",
        description="Relative path where the sequences will be generated",
        default="meshes", maxlen=1000)

    # Morphologies relative path
    bpy.types.Scene.MorphologiesPath = StringProperty(
        name="Morphologies",
        description="Relative path where the morphologies will be generated",
        default="morphologies", maxlen=1000)

    # Analysis relative path
    bpy.types.Scene.AnalysisPath = StringProperty(
        name="Analysis",
        description="Relative path where the analysis reports will be generated",
        default="analysis", maxlen=1000)

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
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.register_class(IOPanel)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(IOPanel)
