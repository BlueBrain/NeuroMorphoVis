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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.utilities


# Reconstruction method
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

           (nmv.enums.Synaptics.UseCase.NOT_SELECTED,
            'Please select a Use Case',
            'Select a specific use case or configuration to visualize a specific set of synapse'),
           ],
    name='Use Case',
    default=nmv.enums.Synaptics.UseCase.NOT_SELECTED)


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

    name='Coloring Scheme',
    default=nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR)

bpy.types.Scene.NMV_EfferentColorCoding = bpy.props.EnumProperty(
    items=[(nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR,
            'Unified Color',
            'Color all the synapses with a single color'),

           (nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED,
            'Post-synaptic Morphological Type',
            'Color code the synapses based on the morphological type (or m-type) of the connecting'
            'post-synaptic cell.'),

           (nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED,
            'Pre-synaptic Electrical Type',
            'Color code the synapses based on the electrical type (or e-type) of the connecting'
            'post-synaptic cell.')],

    name='Coloring Scheme',
    default=nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR)


# Excitatory synapses color
bpy.types.Scene.NMV_ExcitatorySynapsesColor = bpy.props.FloatVectorProperty(
    name='Excitatory Synapses Color',
    subtype='COLOR', default=nmv.enums.Color.EXCITATORY_SYNAPSES, min=0.0, max=1.0,
    description='The color of the excitatory synapses')

# Inhibitory synapses color
bpy.types.Scene.NMV_InhibitorySynapsesColor = bpy.props.FloatVectorProperty(
    name='Inhibitory Synapses Color',
    subtype='COLOR', default=nmv.enums.Color.INHIBITORY_SYNAPSES, min=0.0, max=1.0,
    description='The color of the inhibitory synapses')

# Afferent synapses color
bpy.types.Scene.NMV_AfferentSynapsesColor = bpy.props.FloatVectorProperty(
    name='Afferent Synapses Color',
    subtype='COLOR', default=nmv.enums.Color.AFFERENT_SYNAPSES, min=0.0, max=1.0,
    description='The color of the afferent synapses')

# Efferent synapses color
bpy.types.Scene.NMV_EfferentSynapsesColor = bpy.props.FloatVectorProperty(
    name='Efferent Synapses Color',
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
    default=100, min=0, max=100,
    description='The percentage of the synapses loaded in the scene')

# The unified radius of all the synapses
bpy.types.Scene.NMV_SynapseRadius = bpy.props.FloatProperty(
    name='Synapse Radius',
    description='The unified radius of all the synapses',
    default=0, min=0, max=1000000)



