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

import neuromorphovis as nmv
import neuromorphovis.analysis
from neuromorphovis.analysis import AnalysisItem


####################################################################################################
# Analysis items per neurite
####################################################################################################
per_neurite = [

    # Neurite total length
    AnalysisItem(variable='Length',
                 name='Length',
                 description='Total length of the neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Average section length
    AnalysisItem(variable='AvgSectionLength',
                 name='Section Length (Avg.)',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Average segment length
    AnalysisItem(variable='AvgSegmentLength',
                 name='Segment Length (Avg.)',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Neurite total surface area
    AnalysisItem(variable='SurfaceArea',
                 name='Surface Area',
                 data_format='FLOAT',
                 unit='AREA'),

    # Average section surface area
    AnalysisItem(variable='AvgSectionSurfaceArea',
                 name='Section Surface Area (Avg.)',
                 data_format='FLOAT',
                 unit='AREA'),

    # Average segment surface area
    AnalysisItem(variable='AvgSegmentSurfaceArea',
                 name='Segment Surface Area (Avg.)',
                 data_format='FLOAT',
                 unit='AREA'),

    # Neurite total volume
    AnalysisItem(variable='Volume',
                 name='Volume',
                 data_format='FLOAT',
                 unit='VOLUME'),

    # Average section volume
    AnalysisItem(variable='AvgSectionVolume',
                 name='Section Volume (Avg.)',
                 data_format='FLOAT',
                 unit='VOLUME'),

    # Average segment volume
    AnalysisItem(variable='AvgSegmentVolume',
                 name='Segment Volume (Avg.)',
                 data_format='FLOAT',
                 unit='VOLUME'),

    # Number of bifurcations along the neurite
    AnalysisItem(variable='NumberBifurcations',
                 name='# Bifurcations',
                 description='Number of bifurcations along the neurite',
                 data_format='INT'),

    # Number of trifurcations along the neurite
    AnalysisItem(variable='NumberTrifurcations',
                 name='# Trifurcations',
                 description='Number of trifurcations along the neurite',
                 data_format='INT'),

    # Number of orphan sections
    AnalysisItem(variable='NumberOrphanSections',
                 name='# Orphan Sections',
                 description='Number of sections with a single child only at the branching points',
                 data_format='INT'),

    # Number of sections along the neurite
    AnalysisItem(variable='NumberSections',
                 description='Number of sections along the neurite',
                 name='# Sections',
                 data_format='INT'),

    # Number of short sections along the neurite
    AnalysisItem(variable='NumberShortSections',
                 name='# Short Sections',
                 description='Sections with large radii compared to their length',
                 data_format='INT'),

    # Number of samples along the neurite
    AnalysisItem(variable='NumberSamples',
                 name='# Samples',
                 description='Number of samples along the neurite',
                 data_format='INT'),

    # Average number of samples per section
    AnalysisItem(variable='AvgNumberSamplesPerSection',
                 name='# Samples / Section (Avg.)',
                 description='Average number of samples per section',
                 data_format='INT'),

]


####################################################################################################
# Analysis items per neurite
####################################################################################################
per_soma = [

    # Soma surface area
    AnalysisItem(variable='SurfaceArea',
                 name='Surface Area',
                 data_format='FLOAT',
                 unit='AREA'),

    # Soma volume
    AnalysisItem(variable='Volume',
                 name='Volume',
                 data_format='FLOAT',
                 unit='Volume'),

    # Number of profile samples
    AnalysisItem(variable='NumberProfileSamples',
                 name='# Profile Samples',
                 data_format='INT'),


]


filters = [

    # number samples on arbor

    # min number of samples per section
    # avg number of samples per section
    # max number of samples per section

]

import neuromorphovis.consts
import neuromorphovis.analysis



x = [
    # Minimum section length
    AnalysisItem(variable='MinSectionLength',
                 name='Min. Section Length ',
                 description='The length of the shortest section along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Maximum section length
    AnalysisItem(variable='MaxSectionLength',
                 name='Max. Section Length ',
                 description='The length of the longest section along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Average section length
    AnalysisItem(variable='AvgSectionLength',
                 name='Avg. Section Length ',
                 description='Average length of the sections along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Minimum segment length
    AnalysisItem(variable='MinSegmentLength',
                 name='Min. Segment Length ',
                 description='The length of the shortest segment along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Maximum segment length
    AnalysisItem(variable='MaxSegmentLength',
                 name='Max. Segment Length ',
                 description='The length of the longest segment along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Average segment length
    AnalysisItem(variable='AvgSegmentLength',
                 name='Avg. Segment Length ',
                 description='Average length of the segment along this neurite',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Zero-length segments
    AnalysisItem(variable='ZeroLengthSegments',
                 name='0-length Segments',
                 description='The total number of zero-length segments along this neurite',
                 data_format='INT'),

    ################################################################################################
    # Surface Area
    ################################################################################################


    AnalysisItem(variable='NumberSamples',
                 name='# Samples',
                 description='Total number of samples along this neurite',
                 data_format='INT'),
    AnalysisItem(variable='MinSamplesPerSection',
                 name='Min. # Samples / Section',
                 description='The minimum number of samples along a section of this neurite',
                 data_format='INT'),
    AnalysisItem(variable='MaxSamplesPerSection',
                 name='Max. # Samples / Section',
                 description='The maximum number of samples along a section of this neurite',
                 data_format='INT'),
    AnalysisItem(variable='AvgSamplesPerSection',
                 name='Avg. # Samples / Section',
                 description='The average number of samples along a section of this neurite',
                 data_format='INT'),
]





