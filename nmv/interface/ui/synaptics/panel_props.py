####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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


# Synaptics use case
bpy.types.Scene.NMV_SynapticsUseCase = bpy.props.EnumProperty(
    items=[(nmv.enums.Synaptics.UseCase.AFFERENT,
            'Afferent Synapses',
            'Visualize the afferent synapses only'),

           (nmv.enums.Synaptics.UseCase.EFFERENT,
            'Efferent Synapses',
            'Visualize the efferent synapses only'),

           (nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT,
            'Afferent and Efferent Synapses',
            'Visualize the afferent and efferent synapses combined'),

           (nmv.enums.Synaptics.UseCase.EXCITATORY,
            'Excitatory Synapses',
            'Visualize the excitatory synapses only'),

           (nmv.enums.Synaptics.UseCase.INHIBITORY,
            'Inhibitory Synapses',
            'Visualize the inhibitory synapses only'),

           (nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY,
            'Excitatory and Inhibitory Synapses',
            'Visualize the inhibitory synapses combined'),

           (nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC,
            'Shared Synapses with a Pre-synaptic Neuron',
            'Visualize the shared synapses with a pre-synaptic neuron'),

           (nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC,
            'Shared Synapses with a Post-synaptic Neuron',
            'Visualize the shared synapses with a post-synaptic neuron'),

           (nmv.enums.Synaptics.UseCase.TARGETS,
            'Customized Synapse List',
            'Visualize a customized color-coded lists of synapses valid only for the input neuron'),

           (nmv.enums.Synaptics.UseCase.PROJECTION_TO_CELL,
            'Projection to Neuron',
            'Visualize a the afferent synapses from a given projection'),

           (nmv.enums.Synaptics.UseCase.NOT_SELECTED,
            'Please select a Use Case',
            'Select a specific use case or configuration to visualize a specific set of synapse')],
    name='Use Case',
    default=nmv.enums.Synaptics.UseCase.NOT_SELECTED)

# Color-coding schemes for the afferent synapses use case
bpy.types.Scene.NMV_AfferentColorCoding = bpy.props.EnumProperty(
    items=[(nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR,
            'Unified Color',
            'Color all the synapses with a single color'),

           (nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED,
            'Pre-synaptic Morphological Type',
            'Color code the synapses based on the morphological type (or m-type) of the connecting'
            'pre-synaptic cell.'),

           (nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED,
            'Pre-synaptic Electrical Type',
            'Color code the synapses based on the electrical type (or e-type) of the connecting'
            'pre-synaptic cell.')],

    name='Color Scheme',
    default=nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR)

# Color-coding schemes for the efferent synapses use case
bpy.types.Scene.NMV_EfferentColorCoding = bpy.props.EnumProperty(
    items=[(nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR,
            'Unified Color',
            'Color all the synapses with a single color'),

           (nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED,
            'Post-synaptic Morphological Type',
            'Color code the synapses based on the morphological type (or m-type) of the connecting'
            'post-synaptic cell.'),

           (nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED,
            'Post-synaptic Electrical Type',
            'Color code the synapses based on the electrical type (or e-type) of the connecting'
            'post-synaptic cell.')],

    name='Color Scheme',
    default=nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR)

# Excitatory synapses color
bpy.types.Scene.NMV_ExcitatorySynapsesColor = bpy.props.FloatVectorProperty(
    name='Excitatory Synapses',
    subtype='COLOR', default=nmv.enums.Color.EXCITATORY_SYNAPSES, min=0.0, max=1.0,
    description='The color of the excitatory synapses')

# Inhibitory synapses color
bpy.types.Scene.NMV_InhibitorySynapsesColor = bpy.props.FloatVectorProperty(
    name='Inhibitory Synapses',
    subtype='COLOR', default=nmv.enums.Color.INHIBITORY_SYNAPSES, min=0.0, max=1.0,
    description='The color of the inhibitory synapses')

# Afferent synapses color
bpy.types.Scene.NMV_AfferentSynapsesColor = bpy.props.FloatVectorProperty(
    name='Afferent Synapses',
    subtype='COLOR', default=nmv.enums.Color.AFFERENT_SYNAPSES, min=0.0, max=1.0,
    description='The color of the afferent synapses')

# Efferent synapses color
bpy.types.Scene.NMV_EfferentSynapsesColor = bpy.props.FloatVectorProperty(
    name='Efferent Synapses',
    subtype='COLOR', default=nmv.enums.Color.EFFERENT_SYNAPSES, min=0.0, max=1.0,
    description='The color of the efferent synapses')

# A single color that is used to color all the synapses
bpy.types.Scene.NMV_SynapsesColor = bpy.props.FloatVectorProperty(
    name='Synapses Color',
    subtype='COLOR', default=nmv.enums.Color.SYNAPSES, min=0.0, max=1.0,
    description='A unifying color used to color all the shown synapses')

# The percentage of the synapses loaded in the scene
bpy.types.Scene.NMV_SynapsesPercentage = bpy.props.FloatProperty(
    name='Percentage',
    default=100.0, min=0, max=100,
    description='The percentage of the synapses loaded in the scene. Applicable values [0-100%]')

# The unified radius of all the synapses
bpy.types.Scene.NMV_SynapseRadius = bpy.props.FloatProperty(
    name='Radius',
    description='The unified radius of all the synapses in μm. Applicable values [2-5]',
    default=2.0, min=0, max=5)

# Pre-synaptic neuron GID, for visualizing shared synapses
bpy.types.Scene.NMV_PreSynapticGID = bpy.props.StringProperty(
    name='Pre-Synaptic GID',
    description="The GID of a pre-synaptic cell that shares synapses with this cell.",
    default=nmv.consts.Strings.PRE_GID, maxlen=1024)

# Post-synaptic neuron GID, for visualizing shared synapses
bpy.types.Scene.NMV_PostSynapticGID = bpy.props.StringProperty(
    name='Post-Synaptic GID',
    description="The GID of a post-synaptic cell that shares synapses with this cell.",
    default=nmv.consts.Strings.POST_GID, maxlen=1024)

# Single neuron properties #########################################################################
# Display the dendrites
bpy.types.Scene.NMV_DisplayDendrites = bpy.props.BoolProperty(
    name='Dendrites',
    description='',
    default=True)

# Display the axons
bpy.types.Scene.NMV_DisplayAxons = bpy.props.BoolProperty(
    name='Axons',
    description='',
    default=True)

# Dendrites color
bpy.types.Scene.NMV_SynapticsDendritesColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description='')

# Axons color
bpy.types.Scene.NMV_SynapticsAxonsColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description='')

# Neuron pair properties ###########################################################################
bpy.types.Scene.NMV_DisplayPreSynapticDendrites = bpy.props.BoolProperty(
    name='Pre-Synaptic Dendrites',
    description='',
    default=True)

bpy.types.Scene.NMV_DisplayPreSynapticAxons = bpy.props.BoolProperty(
    name='Pre-Synaptic Axons',
    description='',
    default=True)

bpy.types.Scene.NMV_DisplayPostSynapticDendrites = bpy.props.BoolProperty(
    name='Post-Synaptic Dendrites',
    description='',
    default=True)

bpy.types.Scene.NMV_DisplayPostSynapticAxons = bpy.props.BoolProperty(
    name='Post-Synaptic Axons',
    description='',
    default=True)

bpy.types.Scene.NMV_PreSynapticDendritesColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description='')

bpy.types.Scene.NMV_PreSynapticAxonsColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description='')

bpy.types.Scene.NMV_PostSynapticDendritesColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description='')

bpy.types.Scene.NMV_PostSynapticAxonsColor = bpy.props.FloatVectorProperty(
    name='',
    subtype='COLOR', default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description='')

# Shared neuron parameters #########################################################################
bpy.types.Scene.NMV_SynapticsUnifyRadius = bpy.props.BoolProperty(
    name='Unify Branches Radii',
    description='',
    default=True)

# The unified radius of all the synapses
bpy.types.Scene.NMV_SynapticsUnifiedNeuronRadius = bpy.props.FloatProperty(
    name='Neuron Radius',
    description='The unified radius of all the branches of the neuron. Applicable values [0.1-5]',
    default=0.5, min=0.1, max=5)

# Number of synapses ###############################################################################
bpy.types.Scene.NMV_SynapticsNumberAfferentSynapses = bpy.props.IntProperty(
    name="Count",
    description="The number of afferent synapses found",
    default=0, min=0, max=1000000)

bpy.types.Scene.NMV_SynapticsNumberEfferentSynapses = bpy.props.IntProperty(
    name="Count",
    description="The number of efferent synapses found",
    default=0, min=0, max=1000000)

bpy.types.Scene.NMV_SynapticsNumberExcitatorySynapses = bpy.props.IntProperty(
    name="Count",
    description="The number of excitatory synapses found",
    default=0, min=0, max=1000000)

bpy.types.Scene.NMV_SynapticsNumberInhibitorySynapses = bpy.props.IntProperty(
    name="Count",
    description="The number of inhibitory synapses found",
    default=0, min=0, max=1000000)

bpy.types.Scene.NMV_SynapticsNumberSharedSynapses = bpy.props.IntProperty(
    name="Count",
    description="The number of shared synapses between the two neurons",
    default=0, min=0, max=1000000)

# Performance ######################################################################################
bpy.types.Scene.NMV_SynapticReconstructionTime = bpy.props.FloatProperty(
    name="Time (Sec)",
    description="The time it takes to reconstruct the synaptome",
    default=0, min=0, max=1000000)

# Rendering options ################################################################################
# Rendering resolution
bpy.types.Scene.NMV_SynapticsRenderingResolution = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.Resolution.FIXED,
            'Fixed',
            'Renders an image at a specific resolution'),
           (nmv.enums.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image at a multiple factor of the exact scale in (um)')],
    name='Type',
    default=nmv.enums.Rendering.Resolution.FIXED)

# Rendering view
bpy.types.Scene.NMV_SynapticsRenderingView = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.View.WIDE_SHOT,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Rendering.View.CLOSEUP,
            'Close Up',
            'Renders a close up image the focuses on the soma of the chosen neuron')],
    name='View', default=nmv.enums.Rendering.View.WIDE_SHOT)

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.NMV_SynapticsScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Render the scale bar on the resulting image',
    default=False)

# Image format
bpy.types.Scene.NMV_SynapticsImageFormat = bpy.props.EnumProperty(
    items=nmv.enums.Image.Extension.IMAGE_EXTENSION_ITEMS,
    name='',
    default=nmv.enums.Image.Extension.PNG)

# Image resolution
bpy.types.Scene.NMV_SynapticsFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=nmv.consts.Image.DEFAULT_RESOLUTION, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_SynapticsFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a mesh to scale")

# Rendering closeup size
bpy.types.Scene.NMV_SynapticsCloseUpSize = bpy.props.FloatProperty(
    name='Size',
    description='The size of the view that will be rendered in microns',
    default=20, min=5, max=100)

# Rendering time
bpy.types.Scene.NMV_SynapticsRenderingTime = bpy.props.FloatProperty(
    name='Rendering (Sec)',
    description='The time it takes to render the synaptics scene into an image',
    default=0, min=0, max=1000000)

# Synaptics json file
bpy.types.Scene.NMV_SynapticsJsonFile = bpy.props.StringProperty(
    name="Synaptics File",
    description="Select a specific synaptics json file that contains a color-coded list "
                "of synapses",
    default=nmv.consts.Strings.SELECT_FILE, maxlen=2048, subtype='FILE_PATH')

# Shader applied to the synaptics elements
bpy.types.Scene.NMV_SynapticsShader = bpy.props.EnumProperty(
    items=nmv.enums.Shader.MATERIAL_ITEMS,
    name='',
    default=nmv.enums.Shader.LAMBERT_WARD)

# Synaptics projection name
bpy.types.Scene.NMV_SynapticsProjectionName = bpy.props.StringProperty(
    name="Projection Name",
    description="Enter the name of the projection.",
    default='Enter Projection Name', maxlen=2048
)