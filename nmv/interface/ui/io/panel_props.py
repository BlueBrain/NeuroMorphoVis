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


# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums

# Input options (what is the input source)
bpy.types.Scene.NMV_InputSource = bpy.props.EnumProperty(
    items=[
        (
            nmv.enums.Input.MORPHOLOGY_FILE,
            ".SWC, .ASC or .H5 File",
            "Load individual .SWC, .ASC or .H5 morphology file of a neuron or an astrocyte. "
            "For the astrocyte file format in H5 files, please refer to the paper by "
            "Abdellah et al. 2021",
        ),
        (
            nmv.enums.Input.CIRCUIT_GID,
            "Circuit (GID)",
            "Load the morphology of either a neuron or an astrocyte with a specific GID from "
            "a digitally reconstructed circuit using a circuit configuration file. The current "
            "version of NeuroMorphoVis supports loading libSonata circuits. For details, please "
            "refer to the software suits at https://github.com/BlueBrain",
        ),
        (
            nmv.enums.Input.LIBSONATA_CIRCUIT,
            "libSonata Circuit ",
            "Load a specific GID within a population from a libSonata config",
        ),
    ],
    name="Input Source",
    default=nmv.enums.Input.MORPHOLOGY_FILE)

# Center the loaded morphology at the origin
bpy.types.Scene.NMV_CenterMorphologyAtOrigin = bpy.props.BoolProperty(
    name='Center At Origin',
    description='Center the loaded morphology at the origin irrespective to its actual center. '
                'If the soma is already located at the origin, then checking this checkbox is '
                'irrelevant',
    default=True)

# Morphology file
bpy.types.Scene.NMV_MorphologyFile = bpy.props.StringProperty(
    name="Morphology File",
    description="Select a specific morphology to load, visualize or to mesh",
    default=nmv.consts.Strings.SELECT_FILE, maxlen=2048, subtype='FILE_PATH')

# Morphology directory
bpy.types.Scene.NMV_MorphologyDirectory = bpy.props.StringProperty(
    name="Morphology Directory",
    description="Select a directory to that contains multiple morphology files in it",
    default=nmv.consts.Strings.SELECT_DIRECTORY, maxlen=2048, subtype='DIR_PATH')

# A circuit configuration file
bpy.types.Scene.NMV_CircuitFile = bpy.props.StringProperty(
    name="BBP Circuit Config",
    description="Select a circuit file.",
    default=nmv.consts.Strings.SELECT_CIRCUIT_FILE,
    maxlen=2048,
    subtype="FILE_PATH",
)

# A circuit configuration file
bpy.types.Scene.NMV_LibsonataConfigFile = bpy.props.StringProperty(
    name="libsonata Config",
    description="Select a libsonata config file",
    default=nmv.consts.Strings.SELECT_CIRCUIT_FILE,
    maxlen=2048,
    subtype="FILE_PATH",
)

# libsonata Population
bpy.types.Scene.NMV_LibsonataPopulation = bpy.props.StringProperty(
    name="libsonata Population",
    description="Select a libsonata population",
    default=nmv.consts.Strings.SELECT_POPULATION,
    maxlen=2048,
)

# Circuit target
bpy.types.Scene.NMV_Target = bpy.props.StringProperty(
    name="Target",
    description="Select a specific circuit target that must exist in the circuit and contain "
                "more than a single GID, or at least a single GID",
    default=nmv.consts.Strings.ADD_TARGET, maxlen=1024)

# Neuron GID
bpy.types.Scene.NMV_Gid = bpy.props.StringProperty(
    name="GID",
    description="Select a specific GID in the circuit",
    default=nmv.consts.Strings.ADD_GID, maxlen=1024)

# Loading time
bpy.types.Scene.NMV_MorphologyLoadingTime = bpy.props.FloatProperty(
    name="Loading Morphology (Sec)",
    description="The time to load the morphology from file and draw it to viewport. If the neuron "
                "is loaded from a circuit, it might takes several second depending on the "
                "network performance to load from a remote file system",
    default=0, min=0, max=1000000)

# Drawing time
bpy.types.Scene.NMV_MorphologyDrawingTime = bpy.props.FloatProperty(
    name="Drawing Morphology (Sec)",
    description="The time it takes to draw the morphology after loading it",
    default=0, min=0, max=1000000)

# Output directory
bpy.types.Scene.NMV_OutputDirectory = bpy.props.StringProperty(
    name="Output Directory",
    description="Select a directory where the results (analysis, images, movies, meshes, etc.) "
                "will be generated",
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
