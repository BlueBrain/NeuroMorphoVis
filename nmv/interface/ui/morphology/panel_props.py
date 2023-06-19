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
import nmv.utilities

####################################################################################################
# Panel options
####################################################################################################
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
    name='Build Axons',
    description='Select this flag to reconstruct the axon',
    default=True)

# Axon branching order
# Since the axon is so complicated, we will set its default branching order to 5
bpy.types.Scene.NMV_AxonsBranchingOrder = bpy.props.IntProperty(
    name='Branching Order',
    description='Branching order for the axon',
    default=nmv.consts.Skeleton.AXON_DEFAULT_BRANCHING_ORDER, min=0, max=1000)

# Build basal dendrites
bpy.types.Scene.NMV_BuildBasalDendrites = bpy.props.BoolProperty(
    name='Build Basal Dendrites',
    description='Select this flag to reconstruct the basal dendrites',
    default=True)

# Basal dendrites branching order
bpy.types.Scene.NMV_BasalDendritesBranchingOrder = bpy.props.IntProperty(
    name='Branching Order',
    description='Branching order for the basal dendrites',
    default=nmv.consts.Skeleton.MAX_BRANCHING_ORDER, min=0, max=1000)

# Build apical dendrite
bpy.types.Scene.NMV_BuildApicalDendrite = bpy.props.BoolProperty(
    name='Build Apical Dendrites',
    description='Select this flag to reconstruct the apical dendrite (if exists)',
    default=True)

# Apical dendrite branching order
bpy.types.Scene.NMV_ApicalDendritesBranchingOrder = bpy.props.IntProperty(
    name='Branching Order',
    description='Branching order for the apical dendrite',
    default=nmv.consts.Skeleton.MAX_BRANCHING_ORDER, min=0, max=1000)

# Morphology material or shading
bpy.types.Scene.NMV_MorphologyMaterial = bpy.props.EnumProperty(
    items=nmv.enums.Shader.MATERIAL_ITEMS,
    name='',
    default=nmv.enums.Shader.LAMBERT_WARD)

# Per segment color-coding
bpy.types.Scene.NMV_PerSegmentColorCodingBasis = bpy.props.EnumProperty(
    items=nmv.enums.ColorCoding.SEGMENTS_COLOR_CODING_ITEMS,
    name='',
    default=nmv.enums.ColorCoding.DEFAULT_SCHEME)

# Connected object color-coding
bpy.types.Scene.NMV_ConnectedObjectColorCodingBasis = bpy.props.EnumProperty(
    items=nmv.enums.ColorCoding.CONNECTED_OBJECT_COLOR_CODING_ITEMS,
    name='',
    default=nmv.enums.ColorCoding.DEFAULT_SCHEME)


# Per-section color-coding
bpy.types.Scene.NMV_PerSectionColorCodingBasis = bpy.props.EnumProperty(
    items=nmv.enums.ColorCoding.SECTIONS_COLOR_CODING_ITEMS,
    name='',
    default=nmv.enums.ColorCoding.DEFAULT_SCHEME)

# The alternative color used to color every second object in the morphology
bpy.types.Scene.NMV_MorphologyColor = bpy.props.FloatVectorProperty(
    name="Color",
    subtype='COLOR', default=nmv.consts.Color.LIGHT_RED, min=0.0, max=1.0,
    description="The color of the entire morphology surface")

# The alternative color used to color every second object in the morphology
bpy.types.Scene.NMV_MorphologyColor1 = bpy.props.FloatVectorProperty(
    name="Color 1",
    subtype='COLOR', default=nmv.consts.Color.LIGHT_RED, min=0.0, max=1.0,
    description="The first alternating color of the morphology")

# The alternative color used to color every second object in the morphology
bpy.types.Scene.NMV_MorphologyColor2 = bpy.props.FloatVectorProperty(
    name="Color 2",
    subtype='COLOR', default=nmv.consts.Color.SKY_BLUE, min=0.0, max=1.0,
    description="The second alternating color of the morphology")

# Soma color
bpy.types.Scene.NMV_SomaColor = bpy.props.FloatVectorProperty(
    name='Soma Color',
    subtype='COLOR', default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description='The color of the reconstructed soma')

# Axon color
bpy.types.Scene.NMV_AxonColor = bpy.props.FloatVectorProperty(
    name='Axon Color',
    subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description='The color of the reconstructed axon')

# Basal dendrites color
bpy.types.Scene.NMV_BasalDendritesColor = bpy.props.FloatVectorProperty(
    name='Basal Dendrites  Color',
    subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description='The color of the reconstructed basal dendrites')

# Apical dendrite color
bpy.types.Scene.NMV_ApicalDendriteColor = bpy.props.FloatVectorProperty(
    name='Apical Dendrite Color',
    subtype='COLOR', default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
    description='The color of the reconstructed apical dendrite')

# Articulation color
bpy.types.Scene.NMV_ArticulationColor = bpy.props.FloatVectorProperty(
    name='Articulation Color',
    subtype='COLOR', default=nmv.enums.Color.ARTICULATION, min=0.0, max=1.0,
    description='The color of the articulations in the Articulated Section mode')

# Endfeet color
bpy.types.Scene.NMV_EndfeetColor = bpy.props.FloatVectorProperty(
    name='Endfeet Color',
    subtype='COLOR', default=nmv.enums.Color.ENDFEET, min=0.0, max=1.0,
    description='The color of the endfeet if the loaded morphology is an astrocyte')


# Use single color for the all the objects in the morphology
bpy.types.Scene.NMV_MorphologyHomogeneousColor = bpy.props.BoolProperty(
    name='Homogeneous Color',
    description='Use a single color for rendering all the objects of the morphology',
    default=False)

# Reconstruction method
bpy.types.Scene.NMV_MorphologyReconstructionTechnique = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Method.DISCONNECTED_SEGMENTS,
            'Disconnected Segments',
            'Each segment is an independent object (this approach is time consuming)'),
           (nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS,
            'Disconnected Sections',
            'Each section is an independent object'),
           (nmv.enums.Skeleton.Method.PROGRESSIVE,
            'Progressive',
            'Progressive reconstruction of the morphology'),
           (nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS,
            'Articulated Sections',
            'Each section is an independent object, but connected with a pivot'),
           (nmv.enums.Skeleton.Method.SAMPLES,
            'Samples',
            'Each sample is drawn as a sphere (this approach is very time consuming)'),
           (nmv.enums.Skeleton.Method.CONNECTED_SECTIONS,
            'Connected Sections',
            'The sections of a single arbor are connected together'),
           (nmv.enums.Skeleton.Method.DENDROGRAM,
            'Dendrogram',
            'Draw the morphology skeleton as a dendrogram, where you can visualize it in 3D.'
            'This mode helps to analyse complex morphology skeletons')],
    name='Method',
    default=nmv.enums.Skeleton.Method.DISCONNECTED_SECTIONS)

# Arbors style
bpy.types.Scene.NMV_ArborsStyle = bpy.props.EnumProperty(
    items=nmv.enums.Skeleton.Style.MORPHOLOGY_STYLE_ITEMS,
    name="",
    default=nmv.enums.Skeleton.Style.ORIGINAL)

# Branching, is it based on angles or radii
bpy.types.Scene.NMV_MorphologyBranching = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Branching.ANGLES,
            'Angles',
            'Make the branching based on the angles at branching points'),
           (nmv.enums.Skeleton.Branching.RADII,
            'Radii',
            'Make the branching based on the radii of the children at the branching points')],
    name='Branching Style',
    default=nmv.enums.Skeleton.Branching.ANGLES)

# Soma connection to roots
bpy.types.Scene.NMV_SomaConnectionToRoot = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN,
            'Connect Connected',
            'Connect all the arbors that are physically connected to the origin of the soma'),
           (nmv.enums.Skeleton.Roots.ALL_CONNECTED,
            'All Connected',
            'Connect all the arbors to the origin of the soma even if they intersect or too far '
            'away from the soma'),
           (nmv.enums.Skeleton.Roots.ALL_DISCONNECTED,
            'All Disconnected',
            'Disconnect all the arbors from the soma')],
    name='',
    default=nmv.enums.Skeleton.Roots.CONNECT_CONNECTED_TO_ORIGIN)

# Arbor quality
bpy.types.Scene.NMV_ArborQuality = bpy.props.IntProperty(
    name='Quality',
    description='The tubular quality of the branches.',
    default=3, min=1, max=64)

# Section radius
bpy.types.Scene.NMV_SectionsRadii = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Radii.ORIGINAL,
            'Original',
            'Set the radii of the samples to the original ones reported in the morphology file'),
           (nmv.enums.Skeleton.Radii.UNIFIED,
            'Unified',
            'Set the radii of all the samples in the entire morphology to a unified value given '
            'by the user'),
           (nmv.enums.Skeleton.Radii.UNIFIED_PER_ARBOR_TYPE,
            'Type Unified',
            'Set the radii of all the samples in the (axon, apical dendrite and basal dendrites) '
            'to a unified value (to axon, apical dendrite and basal dendrites) given by the user'),
           (nmv.enums.Skeleton.Radii.SCALED,
            'Scaled',
            'Scale the radii of all the samples in the morphology with a scale factor given '
            'by the user'),
           (nmv.enums.Skeleton.Radii.FILTERED,
            'Filtered',
            'Filter the samples with radii lower than a given threshold'), ],
    name="",
    default=nmv.enums.Skeleton.Radii.ORIGINAL)

# Unified radius value
bpy.types.Scene.NMV_UnifiedRadiusValue = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The value of the unified radius in microns between (0.05 and 5.0) microns',
    default=1.0, min=0.05, max=5.0)

# Unified radius value for the axon
bpy.types.Scene.NMV_AxonUnifiedRadiusValue = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The value of the radius in microns between (0.05 and 5.0) microns',
    default=1.0, min=0.05, max=5.0)

# Unified radius value for the apical dendrite
bpy.types.Scene.NMV_ApicalDendriteUnifiedRadiusValue = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The value of the radius in microns between (0.05 and 5.0) microns',
    default=1.0, min=0.05, max=5.0)

# Unified radius value for the basal dendrites
bpy.types.Scene.NMV_BasalDendritesUnifiedRadiusValue = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The value of the radius in microns between (0.05 and 5.0) microns',
    default=1.0, min=0.05, max=5.0)

# Unified radius value for the axon
bpy.types.Scene.NMV_AxonUnifiedRadiusValue = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The value of the radius in microns between (0.05 and 5.0) microns',
    default=1.0, min=0.05, max=5.0)

# Minimum radius value
bpy.types.Scene.NMV_MinimumRadiusThreshold = bpy.props.FloatProperty(
    name='Minimum',
    description='Any sample with smaller radius than this value will be ignored',
    default=1e-5, min=0.005, max=5.0)

# Maximum radius value
bpy.types.Scene.NMV_MaximumRadiusThreshold = bpy.props.FloatProperty(
    name='Maximum',
    description='Any sample with larger radius than this value will be ignored',
    default=10, min=0.5, max=20)

# Global radius scale value
bpy.types.Scene.NMV_RadiusScaleValue = bpy.props.FloatProperty(
    name='Scale',
    description='A scale factor for scaling the radii of the arbors between (0.01 and 5.0)',
    default=1.0, min=0.01, max=5.0)

# Resampling
bpy.types.Scene.NMV_MorphologyResampling = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Resampling.NONE,
            'None',
            'Do not resample the section at all'),
           (nmv.enums.Skeleton.Resampling.ADAPTIVE_RELAXED,
            'Adaptive Relaxed',
            'Use adaptive resampling to resample the section and remove the unwanted samples '
            'while preserving the spatial features of the section. The new samples will not be '
            'touching each other, that is why it is called relaxed'),
           (nmv.enums.Skeleton.Resampling.ADAPTIVE_PACKED,
            'Adaptive Packed',
            'Use adaptive resampling to resample the section and remove the unwanted samples '
            'while preserving the spatial features of the section. The new samples will overlap '
            'as if they pack the section to fill it entirely, and that is why it is called packed'),
           (nmv.enums.Skeleton.Resampling.FIXED_STEP,
            'Fixed Step',
            'Use fixed resampling step to resample the section. '
            'With high resampling steps, some of the spatial features of the sections could '
            'be gone')],
    name='',
    default=nmv.enums.Skeleton.Resampling.NONE)

# Resampling step
bpy.types.Scene.NMV_MorphologyResamplingStep = bpy.props.FloatProperty(
    name='Value (μm)',
    description='The resampling step in case the Fixed Step method is selected',
    default=1.0, min=0.05, max=10.0)

# Skeleton style
bpy.types.Scene.SkeletonizationTechnique = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Style.ORIGINAL,
            'Original',
            'Use the original morphology skeleton'),
           (nmv.enums.Skeleton.Style.TAPERED,
            'Tapered',
            'Create a tapered morphology skeleton (for artistic purposes).'),
           (nmv.enums.Skeleton.Style.ZIGZAG,
            'Zigzag',
            'Create a zigzagged skeleton (to simulate the way the neurons look under the '
            'microscope when the intracellular space if filled with some stain). This style is '
            'recommended to create meshes that can be used for machine learning applications.'),
           (nmv.enums.Skeleton.Style.TAPERED_ZIGZAG,
            'Tapered Zigzag',
            'Create a zigzagged and tapered skeleton.')],
    name='Skeleton', default=nmv.enums.Skeleton.Style.ORIGINAL)

# Dendrogram type
bpy.types.Scene.NMV_DendrogramType = bpy.props.EnumProperty(
    items=[(nmv.enums.Dendrogram.Type.SIMPLIFIED,
            'Simplified',
            'Draw a simplified dendrogram with a fixed radius at all the samples'),
           (nmv.enums.Dendrogram.Type.DETAILED,
            'Detailed',
            'Draw a detailed dendrogram with varying radii to see the frequency of the tapering')],
    name='Type',
    default=nmv.enums.Dendrogram.Type.SIMPLIFIED)


# Rendering type
bpy.types.Scene.NMV_RenderingType = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.Resolution.FIXED,
            'Fixed Resolution',
            'Renders a full view of the morphology at a specified resolution'),
           (nmv.enums.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image of the full view at the right scale in (um)')],
    name='Type',
    default=nmv.enums.Rendering.Resolution.FIXED)

# Rendering view
bpy.types.Scene.NMV_MorphologyRenderingView = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.View.WIDE_SHOT,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Rendering.View.MID_SHOT,
            'Mid Shot',
            'Renders an image of the reconstructed arbors only'),
           (nmv.enums.Rendering.View.CLOSEUP,
            'Close Up',
            'Renders a close up image the focuses on the soma')],
    name='View',
    default=nmv.enums.Rendering.View.MID_SHOT)

# Image format
bpy.types.Scene.NMV_MorphologyImageFormat = bpy.props.EnumProperty(
    items=nmv.enums.Image.Extension.IMAGE_EXTENSION_ITEMS,
    name='',
    default=nmv.enums.Image.Extension.PNG)

# Frame resolution
bpy.types.Scene.NMV_MorphologyFrameResolution = bpy.props.IntProperty(
    name='',
    default=nmv.consts.Image.DEFAULT_RESOLUTION, min=128, max=1024 * 10,
    description='The resolution of the image generated from rendering the morphology')

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_MorphologyFrameScaleFactor = bpy.props.FloatProperty(
    name='Scale',
    default=1.0, min=1.0, max=100.0,
    description='The scale factor for rendering a morphology to scale')

# Morphology close up dimensions
bpy.types.Scene.NMV_MorphologyCloseUpDimensions = bpy.props.FloatProperty(
    name='Dimensions',
    default=20, min=5, max=100,
    description='The dimensions of the view that will be rendered in microns')

# Morphology rendering progress
bpy.types.Scene.NMV_MorphologyRenderingProgress = bpy.props.IntProperty(
    name='Rendering Progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.NMV_RenderMorphologyScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Render the scale bar on the resulting image automatically',
    default=False)

# Reconstruction time
bpy.types.Scene.NMV_MorphologyReconstructionTime = bpy.props.FloatProperty(
    name='Reconstruction Time (Sec)',
    description='The time it takes to reconstruct the morphology and draw it to the viewport',
    default=0, min=0, max=1000000)

# Rendering time
bpy.types.Scene.NMV_MorphologyRenderingTime = bpy.props.FloatProperty(
    name='Rendering Time (Sec)',
    description='The time it takes to render the morphology into an image',
    default=0, min=0, max=1000000)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_ColorMapResolution = bpy.props.IntProperty(
    name="Resolution", default=nmv.consts.Color.COLORMAP_RESOLUTION, min=4, max=128,
    description="The resolution of the color-map. Range [4 - 128] samples.")

# The minimum value associated with the color map
bpy.types.Scene.NMV_MinimumValue = bpy.props.StringProperty(
    name='', description='', default='0', maxlen=10)

# The maximum value associated with the color map
bpy.types.Scene.NMV_MaximumValue = bpy.props.StringProperty(
    name='', description='', default='100', maxlen=10)

# UI color elements for the color map
for i in range(nmv.consts.Color.COLORMAP_RESOLUTION):
    delta = 100.0 / float(nmv.consts.Color.COLORMAP_RESOLUTION)
    setattr(bpy.types.Scene, 'NMV_R0_Value%d' % i, bpy.props.FloatProperty(
        name='', default=i * delta,
        min=0.0, max=1e10, description=''))
    setattr(bpy.types.Scene, 'NMV_R1_Value%d' % i, bpy.props.FloatProperty(
        name='', default=(i + 1) * delta,
        min=0.0, max=1e10, description=''))

# By default, it is 'Reconstruct Morphology' unless otherwise specified
bpy.types.Scene.NMV_MorphologyButtonLabel = 'Reconstruct Morphology'
