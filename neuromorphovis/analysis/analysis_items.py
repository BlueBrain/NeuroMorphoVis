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


from neuromorphovis.analysis import AnalysisItem

####################################################################################################
# Analysis items per neurite
####################################################################################################
per_neurite = [

    # Neurite total length
    AnalysisItem(variable='Length',
                 name='Length',
                 format='FLOAT',
                 unit='LENGTH'),

    # Average section length
    AnalysisItem(variable='AvgSectionLength',
                 name='Section Length (Avg.)',
                 format='FLOAT',
                 unit='LENGTH'),

    # Average segment length
    AnalysisItem(variable='AvgSegmentLength',
                 name='Segment Length (Avg.)',
                 format='FLOAT',
                 unit='LENGTH'),

    # Neurite total surface area
    AnalysisItem(variable='SurfaceArea',
                 name='Surface Area',
                 format='FLOAT',
                 unit='AREA'),

    # Average section surface area
    AnalysisItem(variable='AvgSectionSurfaceArea',
                 name='Section Surface Area (Avg.)',
                 format='FLOAT',
                 unit='AREA'),

    # Average segment surface area
    AnalysisItem(variable='AvgSegmentSurfaceArea',
                 name='Segment Surface Area (Avg.)',
                 format='FLOAT',
                 unit='AREA'),

    # Neurite total volume
    AnalysisItem(variable='Volume',
                 name='Volume',
                 format='FLOAT',
                 unit='VOLUME'),

    # Average section volume
    AnalysisItem(variable='AvgSectionVolume',
                 name='Section Volume (Avg.)',
                 format='FLOAT',
                 unit='VOLUME'),

    # Average segment volume
    AnalysisItem(variable='AvgSegmentVolume',
                 name='Segment Volume (Avg.)',
                 format='FLOAT',
                 unit='VOLUME'),

    # Number of bifurcations along the neurite
    AnalysisItem(variable='NumberBifurcations',
                 name='# Bifurcations',
                 description='Number of bifurcations along the neurite',
                 format='INT'),

    # Number of trifurcations along the neurite
    AnalysisItem(variable='NumberTrifurcations',
                 name='# Trifurcations',
                 description='Number of trifurcations along the neurite',
                 format='INT'),

    # Number of orphan sections
    AnalysisItem(variable='NumberOrphanSections',
                 name='# Orphan Sections',
                 description='Number of sections with a single child only at the branching points',
                 format='INT'),

    # Number of sections along the neurite
    AnalysisItem(variable='NumberSections',
                 description='Number of sections along the neurite',
                 name='# Sections',
                 format='INT'),

    # Number of short sections along the neurite
    AnalysisItem(variable='NumberShortSections',
                 name='# Short Sections',
                 description='Sections with large radii compared to their length',
                 format='INT'),

    # Number of samples along the neurite
    AnalysisItem(variable='NumberSamples',
                 name='# Samples',
                 description='Number of samples along the neurite',
                 format='INT'),

    # Average number of samples per section
    AnalysisItem(variable='AvgNumberSamplesPerSection',
                 name='# Samples / Section (Avg.)',
                 description='Average number of samples per section',
                 format='INT'),

]


####################################################################################################
# Analysis items per neurite
####################################################################################################
per_soma = [

    # Soma surface area
    AnalysisItem(variable='SurfaceArea',
                 name='Surface Area',
                 format='FLOAT',
                 unit='AREA'),

    # Soma volume
    AnalysisItem(variable='Volume',
                 name='Volume',
                 format='FLOAT',
                 unit='Volume'),

    # Number of profile samples
    AnalysisItem(variable='NumberProfileSamples',
                 name='# Profile Samples',
                 format='INT'),


]



sample_per_neurite = [

    AnalysisItem(variable='NumberSamples',
                 name='# Samples',
                 description='Number of samples along the neurite',
                 format='INT'),
]
