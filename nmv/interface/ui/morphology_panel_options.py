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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums


################################################################################################
# Panel options
################################################################################################
# Build soma
bpy.types.Scene.NMV_BuildSoma = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Representation.IGNORE,
            'Ignore',
            'Ignore soma reconstruction'),
           (nmv.enums.Soma.Representation.SPHERE,
            'Sphere',
            'Represent the soma by a sphere'),
           (nmv.enums.Soma.Representation.META_BALLS,
            'MetaBalls',
            'Reconstruct a rough shape of the soma using MetaBalls. '
            'This approach is real-time and can reconstruct good shapes for the somata, but '
            'more accurate profiles could be reconstructed with the Soft Body option'),
           (nmv.enums.Soma.Representation.SOFT_BODY,
            'SoftBody',
            'Reconstruct a 3D profile of the soma using Soft Body physics.'
            'This method takes few seconds to reconstruct a soma mesh')],
    name='',
    default=nmv.enums.Soma.Representation.META_BALLS)

# Build axon
bpy.types.Scene.NMV_BuildAxon = bpy.props.BoolProperty(
    name="Build Axon",
    description="Select this flag to reconstruct the axon",
    default=True)

# Axon branching order
# Since the axon is so complicated, we will set its default branching order to 5
bpy.types.Scene.NMV_AxonBranchingLevel = bpy.props.IntProperty(
    name="Branching Order",
    description="Branching order for the axon",
    default=nmv.consts.Arbors.AXON_DEFAULT_BRANCHING_ORDER, min=0, max=100)

# Build basal dendrites
bpy.types.Scene.NMV_BuildBasalDendrites = bpy.props.BoolProperty(
    name="Build Basal Dendrites",
    description="Select this flag to reconstruct the basal dendrites",
    default=True)

# Basal dendrites branching order
bpy.types.Scene.NMV_BasalDendritesBranchingLevel = bpy.props.IntProperty(
    name="Branching Order",
    description="Branching order for the basal dendrites",
    default=nmv.consts.Arbors.MAX_BRANCHING_ORDER, min=0, max=100)

# Build apical dendrite
bpy.types.Scene.NMV_BuildApicalDendrite = bpy.props.BoolProperty(
    name="Build Apical Dendrites",
    description="Select this flag to reconstruct the apical dendrite (if exists)",
    default=True)

# Apical dendrite branching order
bpy.types.Scene.NMV_ApicalDendriteBranchingLevel = bpy.props.IntProperty(
    name="Branching Order",
    description="Branching order for the apical dendrite",
    default=nmv.consts.Arbors.MAX_BRANCHING_ORDER, min=0, max=100)

# Morphology material
bpy.types.Scene.NMV_MorphologyMaterial = bpy.props.EnumProperty(
    items=nmv.enums.Shading.MATERIAL_ITEMS,
    name="Material",
    default=nmv.enums.Shading.LAMBERT_WARD)

# Color arbor by part
bpy.types.Scene.NMV_ColorArborByPart = bpy.props.BoolProperty(
    name="Color Arbor By Part",
    description="Each component of the arbor will be assigned a different color",
    default=False)

# Color arbor using black and white alternatives
bpy.types.Scene.NMV_ColorArborBlackAndWhite = bpy.props.BoolProperty(
    name="Black / White",
    description="Each component of the arbor will be assigned a either black or white",
    default=False)

# Use single color for the all the objects in the morphology
bpy.types.Scene.NMV_MorphologyHomogeneousColor = bpy.props.BoolProperty(
    name="Homogeneous Color",
    description="Use a single color for rendering all the objects of the morphology",
    default=False)

# A homogeneous color for all the objects of the morphology
bpy.types.Scene.NMV_NeuronMorphologyColor = bpy.props.FloatVectorProperty(
    name="Membrane Color",
    subtype='COLOR', default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The homogeneous color of the reconstructed morphology membrane")

# Soma color
bpy.types.Scene.NMV_SomaColor = bpy.props.FloatVectorProperty(
    name="Soma Color",
    subtype='COLOR', default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The color of the reconstructed soma")

# Axon color
bpy.types.Scene.NMV_AxonColor = bpy.props.FloatVectorProperty(
    name="Axon Color",
    subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description="The color of the reconstructed axon")

# Basal dendrites color
bpy.types.Scene.NMV_BasalDendritesColor = bpy.props.FloatVectorProperty(
    name="Basal Dendrites  Color",
    subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed basal dendrites")

# Apical dendrite color
bpy.types.Scene.NMV_ApicalDendriteColor = bpy.props.FloatVectorProperty(
    name="Apical Dendrite Color",
    subtype='COLOR', default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed apical dendrite")

# Articulation color
bpy.types.Scene.NMV_ArticulationColor = bpy.props.FloatVectorProperty(
    name="Articulation Color",
    subtype='COLOR', default=nmv.enums.Color.ARTICULATION, min=0.0, max=1.0,
    description="The color of the articulations in the Articulated Section mode")

# Reconstruction method
bpy.types.Scene.NMV_MorphologyReconstructionTechnique = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.Method.DISCONNECTED_SEGMENTS,
            'Disconnected Segments',
            "Each segment is an independent object (this approach is time consuming)"),
           (nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS,
            'Disconnected Sections',
            "Each section is an independent object"),
           (nmv.enums.Skeletonization.Method.ARTICULATED_SECTIONS,
            'Articulated Sections',
            "Each section is an independent object, but connected with a pivot"),
           (nmv.enums.Skeletonization.Method.SAMPLES,
            'Samples',
            "Each sample is drawn as a sphere (this approach is very time consuming)"),
           (nmv.enums.Skeletonization.Method.CONNECTED_SECTIONS,
            'Connected Sections',
            "The sections of a single arbor are connected together")],
    name="Method",
    default=nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS)

# Arbors style
bpy.types.Scene.NMV_ArborsStyle = bpy.props.EnumProperty(
    items=nmv.enums.Arbors.Style.MORPHOLOGY_STYLE_ITEMS,
    name="",
    default=nmv.enums.Arbors.Style.ORIGINAL)

# Branching, is it based on angles or radii
bpy.types.Scene.NMV_MorphologyBranching = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.Branching.ANGLES,
            'Angles',
            'Make the branching based on the angles at branching points'),
           (nmv.enums.Skeletonization.Branching.RADII,
            'Radii',
            'Make the branching based on the radii of the children at the branching points')],
    name='Branching Style',
    default=nmv.enums.Skeletonization.Branching.ANGLES)

# Soma connection to roots
bpy.types.Scene.NMV_SomaConnectionToRoot = bpy.props.EnumProperty(
    items=[(nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN,
            'Connect Connected',
            'Connect the arbors that are physically connected to the origin of the soma'),
           (nmv.enums.Arbors.Roots.ALL_CONNECTED_TO_ORIGIN,
            'All Connected',
            'Connect the all the arbors to the origin of the soma even if they intersect'),
           (nmv.enums.Arbors.Roots.DISCONNECTED_FROM_SOMA,
            'All Disconnected',
            'Disconnect all the arbors from the soma')],
    name='Arbors To Soma',
    default=nmv.enums.Arbors.Roots.CONNECTED_TO_ORIGIN)

# Arbor quality
bpy.types.Scene.NMV_ArborQuality = bpy.props.IntProperty(
    name="Sides",
    description="Number of vertices of the cross-section of each segment along the arbor",
    default=16, min=4, max=128)

# Section radius
bpy.types.Scene.NMV_SectionsRadii = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED,
            'As Specified in Morphology',
            "Use the cross-sectional radii reported in the morphology file"),
           (nmv.enums.Skeletonization.ArborsRadii.FIXED,
            'At a Fixed Diameter',
            "Set all the arbors to a fixed radius"),
           (nmv.enums.Skeletonization.ArborsRadii.SCALED,
            'With Scale Factor',
            "Scale all the arbors using a specified scale factor"),
           (nmv.enums.Skeletonization.ArborsRadii.FILTERED,
            'Filtered',
            "Filter section with lower values than the threshold"), ],
    name="Radii",
    default=nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED)

# Fixed section radius value
bpy.types.Scene.NMV_FixedRadiusValue = bpy.props.FloatProperty(
    name="Value (μm)",
    description="The value of the radius in microns between (0.05 and 5.0) microns",
    default=1.0, min=0.05, max=5.0)

# Threshold value for the radius
bpy.types.Scene.NMV_FilteredRadiusThreshold = bpy.props.FloatProperty(
    name="Threshold",
    description="The value of the threshold radius in microns between (0.005 and 5.0) microns",
    default=1.0, min=0.005, max=5.0)

# Global radius scale value
bpy.types.Scene.NMV_RadiusScaleValue = bpy.props.FloatProperty(
    name="Scale",
    description="A scale factor for scaling the radii of the arbors between (0.01 and 5.0)",
    default=1.0, min=0.01, max=5.0)

# Resampling
bpy.types.Scene.NMV_MorphologyResampling = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.Resampling.NONE,
            'None',
            'Do not resample the section at all'),
           (nmv.enums.Skeletonization.Resampling.ADAPTIVE,
            'Adaptive',
            'Use adaptive resampling to resample the section and remove the unwanted samples '
            'while preserving the spatial features of the section'),
           (nmv.enums.Skeletonization.Resampling.FIXED_STEP,
            'Fixed Step',
            'Use fixed resampling step to resample the section. '
            'With high resampling steps, some of the spatial features of the sections could '
            'be gone')],
    name='',
    default=nmv.enums.Skeletonization.Resampling.NONE)

# Resampling step
bpy.types.Scene.NMV_MorphologyResamplingStep = bpy.props.FloatProperty(
    name="Value (μm)",
    description="The resampling step in case the Fixed Step method is selected",
    default=1.0, min=0.05, max=10.0)

# Skeleton style
bpy.types.Scene.SkeletonizationTechnique = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Skeleton.ORIGINAL,
            'Original',
            'Use the original morphology skeleton'),
           (nmv.enums.Meshing.Skeleton.PLANAR,
            'Planar',
            'Project the entire morphology skeleton to XY plane'),
           (nmv.enums.Meshing.Skeleton.PLANAR_ZIGZAG,
            'Planar Zigzag',
            'Project the entire morphology skeleton to XY plane and zigzag it'),
           (nmv.enums.Meshing.Skeleton.TAPERED,
            'Tapered',
            'Create a tapered morphology skeleton (for artistic purposes).'),
           (nmv.enums.Meshing.Skeleton.ZIGZAG,
            'Zigzag',
            'Create a zigzagged skeleton (to simulate the way the neurons look under the '
            'microscope when the intracellular space if filled with some stain). This style is '
            'recommended to create meshes that can be used for machine learning applications.'),
           (nmv.enums.Meshing.Skeleton.TAPERED_ZIGZAG,
            'Tapered Zigzag',
            'Create a zigzagged and tapered skeleton.')],
    name='Skeleton', default=nmv.enums.Meshing.Skeleton.ORIGINAL)

# Rendering type
bpy.types.Scene.NMV_RenderingType = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION,
            'Fixed Resolution',
            'Renders a full view of the morphology at a specified resolution'),
           (nmv.enums.Skeletonization.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image of the full view at the right scale in (um)')],
    name='Type',
    default=nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering view
bpy.types.Scene.NMV_MorphologyRenderingView = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeletonization.Rendering.View.WIDE_SHOT_VIEW,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW,
            'Mid Shot',
            'Renders an image of the reconstructed arbors only'),
           (nmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW,
            'Close Up',
            'Renders a close up image the focuses on the soma')],
    name='View',
    default=nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW)

# Frame resolution
bpy.types.Scene.NMV_MorphologyFrameResolution = bpy.props.IntProperty(
    name="Resolution",
    default=512, min=128, max=1024 * 10,
    description="The resolution of the image generated from rendering the morphology")

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_MorphologyFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale",
    default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a morphology to scale")

# Morphology close up dimensions
bpy.types.Scene.NMV_MorphologyCloseUpDimensions = bpy.props.FloatProperty(
    name="Dimensions",
    default=20, min=5, max=100,
    description="The dimensions of the view that will be rendered in microns")

# Reconstruction time
bpy.types.Scene.NMV_MorphologyReconstructionTime = bpy.props.FloatProperty(
    name="Reconstruction (Sec)",
    description="The time it takes to reconstruct the morphology and draw it to the viewport",
    default=0, min=0, max=1000000)