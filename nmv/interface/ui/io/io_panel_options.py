####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv.enums
import nmv.scene

# Input options (what is the input source)
bpy.types.Scene.NMV_InputSource = bpy.props.EnumProperty(
    items=[(nmv.enums.Input.MORPHOLOGY_FILE,
            'H5, SWC or ASC File',
            'Load individual .h5, .swc or .asc file without a circuit'),
           (nmv.enums.Input.CIRCUIT_GID,
            'BBP Circuit (GID)',
            'Load a specific GID from the circuit config')],
    name="Input Source",
    default=nmv.enums.Input.MORPHOLOGY_FILE)

# Center the loaded morphology at the origin
bpy.types.Scene.NMV_CenterMorphologyAtOrigin = bpy.props.BoolProperty(
    name='Center At Origin',
    description='Center the loaded morphology at the origin irrespective to its actual center',
    default=True)

# Morphology file
bpy.types.Scene.NMV_MorphologyFile = bpy.props.StringProperty(
    name="Morphology File",
    description="Select a specific morphology to load, visualize or to mesh",
    default='Select File', maxlen=2048, subtype='FILE_PATH')

# Morphology directory
bpy.types.Scene.NMV_MorphologyDirectory = bpy.props.StringProperty(
    name="Morphology Directory",
    description="Select a directory to mesh all the morphologies in it",
    default="Select Directory", maxlen=2048, subtype='DIR_PATH')

# Circuit file or BlueConfig
bpy.types.Scene.NMV_CircuitFile = bpy.props.StringProperty(
    name="Circuit File",
    description="Select a BBP circuit file (or blue config)",
    default="Select Circuit File", maxlen=2048, subtype='FILE_PATH')

# Circuit target
bpy.types.Scene.NMV_Target = bpy.props.StringProperty(
    name="Target",
    description="Select a specific target that must exist in the circuit",
    default="Add Target", maxlen=1024)

# Neuron GID
bpy.types.Scene.NMV_Gid = bpy.props.StringProperty(
    name="GID",
    description="Select a specific GID in the circuit",
    default="Add a GID", maxlen=1024)

# Loading time
bpy.types.Scene.NMV_MorphologyLoadingTime = bpy.props.FloatProperty(
    name="Loading Morphology (Sec)",
    description="The time it takes to load the morphology from file and draw it to the viewport",
    default=0, min=0, max=1000000)

# Drawing time
bpy.types.Scene.NMV_MorphologyDrawingTime = bpy.props.FloatProperty(
    name="Drawing Morphology (Sec)",
    description="The time it takes to draw the morphology after loading it",
    default=0, min=0, max=1000000)

# Output directory
bpy.types.Scene.NMV_OutputDirectory = bpy.props.StringProperty(
    name="Output Directory",
    description="Select a directory where the results will be generated",
    default="Select Directory", maxlen=5000, subtype='DIR_PATH')

# Use default paths for the artifacts
bpy.types.Scene.NMV_DefaultArtifactsRelativePath = bpy.props.BoolProperty(
    name="Use Default Output Paths",
    description="Use the default sub-paths for the artifacts",
    default=True)

# Images relative path
bpy.types.Scene.NMV_ImagesPath = bpy.props.StringProperty(
    name="Images",
    description="Relative path where the images will be generated",
    default="images", maxlen=1000)

# Sequences relative path
bpy.types.Scene.NMV_SequencesPath = bpy.props.StringProperty(
    name="Sequences",
    description="Relative path where the sequences will be generated",
    default="sequences", maxlen=1000)

# Meshes relative path
bpy.types.Scene.NMV_MeshesPath = bpy.props.StringProperty(
    name="Meshes",
    description="Relative path where the sequences will be generated",
    default="meshes", maxlen=1000)

# Morphologies relative path
bpy.types.Scene.NMV_MorphologiesPath = bpy.props.StringProperty(
    name="Morphologies",
    description="Relative path where the morphologies will be generated",
    default="morphologies", maxlen=1000)

# Analysis relative path
bpy.types.Scene.NMV_AnalysisPath = bpy.props.StringProperty(
    name="Analysis",
    description="Relative path where the analysis reports will be generated",
    default="analysis", maxlen=1000)

# Stats. relative path
bpy.types.Scene.NMV_StatisticsPath = bpy.props.StringProperty(
    name="Statistics",
    description="Relative path where the statistics files will be generated",
    default="statistics", maxlen=1000)
