####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal imports
from nmv.analysis.structs import AnalysisItem
from nmv.analysis.kernels.morphology import *


####################################################################################################
# A list of all the analysis items (kernels) that will applied on the morphology skeleton per arbor
####################################################################################################
ui_per_arbor_analysis_items = [

    ################################################################################################
    # Samples-related items
    ################################################################################################
    AnalysisItem(variable='TotalNumberSamples',
                 name='Total # Samples',
                 kernel=kernel_total_number_samples,
                 description='The total number of samples (or digitized points)',
                 data_format='INT'),

    AnalysisItem(variable='TotalNumberSections',
                 name='Total # Sections',
                 kernel=kernel_total_number_sections,
                 description='The total number of sections (or branches)',
                 data_format='INT'),

    AnalysisItem(variable='NumberTips',
                 name='Total # Tips',
                 kernel=kernel_total_number_terminal_tips,
                 description='The total number number of terminal tips',
                 data_format='INT'),

    AnalysisItem(variable='NumberTerminalSegments',
                 name='Total # Terminal Segments',
                 kernel=kernel_total_number_terminal_segments,
                 description='The total number number of terminal segments',
                 data_format='INT'),

    AnalysisItem(variable='MaximumBranchingOrder',
                 name='Max. Branching Order',
                 kernel=kernel_maximum_branching_order,
                 description='The maximum branching order',
                 data_format='INT'),

    AnalysisItem(variable='TotalNumberBifurcations',
                 name='Total # Bifurcations',
                 kernel=kernel_total_number_bifurcations,
                 description='The total number of bifurcations',
                 data_format='INT'),

    AnalysisItem(variable='TotalNumberTrifurcations',
                 name='Total # Trifurcations',
                 kernel=kernel_total_number_trifurcations,
                 description='The total number of trifurcations (or sections with three '
                             'children)',
                 data_format='INT'),

    AnalysisItem(variable='DistanceToOrigin',
                 name='Distance to Origin',
                 kernel=kernel_distance_from_initial_sample_to_origin,
                 description='The distance between the first sample on the initial segment of '
                             'the arbor to the origin. This value is important to see if the arbor '
                             'is disconnected from the soma in the reconstruction',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaximumPathDistance',
                 name='Max. Path Distance',
                 kernel=kernel_maximum_path_distance,
                 description='The maximum distance along an arbor from its root sample to its '
                             'most far leaf',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaximumEuclideanDistance',
                 name='Max. Euclidean Distance',
                 kernel=kernel_maximum_euclidean_distance,
                 description='The maximum Euclidean distance along an arbor from its root sample '
                             'to its most far leaf',
                 data_format='FLOAT'),

    AnalysisItem(variable='MinNumberSamplePerSection',
                 name='Min. # Samples / Section',
                 kernel=kernel_minimum_number_samples_per_section,
                 description='The lowest number of samples a section has',
                 data_format='INT'),

    AnalysisItem(variable='MaxNumberSamplePerSection',
                 name='Max. # Samples / Section',
                 kernel=kernel_maximum_number_samples_per_section,
                 description='The largest number of samples a section has',
                 data_format='INT'),

    AnalysisItem(variable='AvgNumberSamplePerSection',
                 name='Avg. # Samples / Section',
                 kernel=kernel_average_number_samples_per_section,
                 description='The average number of samples per section',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgNumberSamplePerMicron',
                 name='Avg. # Samples / Micron',
                 kernel=kernel_average_number_samples_per_micron_per_section,
                 description='The average number of samples per micron',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgSamplingDistance',
                 name='Avg. Sampling Distance',
                 kernel=kernel_average_sampling_distance_per_section,
                 description='The average sampling step (or distance)',
                 data_format='FLOAT'),

    AnalysisItem(variable='MinSampleRadius',
                 name='Min. Sample Radius',
                 kernel=kernel_minimum_sample_radius,
                 description='The radius of the smallest sample',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaxSampleRadius',
                 name='Max. Sample Radius',
                 kernel=kernel_maximum_sample_radius,
                 description='The radius of the largest sample',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgSampleRadius',
                 name='Avg. Sample Radius',
                 kernel=kernel_average_sample_radius,
                 description='The average sample radius',
                 data_format='FLOAT'),

    AnalysisItem(variable='ZeroRadiiSamples',
                 name='Zero-radius Samples',
                 kernel=kernel_number_zero_radius_samples,
                 description='The total number of zero-radii samples (epsilon value 1e-3 or 1 nm)',
                 data_format='INT'),

    AnalysisItem(variable='MinBurkeTaper',
                 name='Min. Burke Taper',
                 kernel=kernel_minimum_burke_taper,
                 description='The minimum Burke taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='MaxBurkeTaper',
                 name='Max. Burke Taper',
                 kernel=kernel_maximum_burke_taper,
                 description='The maximum Burke taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='AvgBurkeTaper',
                 name='Avg. Burke Taper',
                 kernel=kernel_average_burke_taper,
                 description='The average Burke taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='MinHillmanTaper',
                 name='Min. Hillman Taper',
                 kernel=kernel_minimum_hillman_taper,
                 description='The minimum Hillman taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='MaxHillmanTaper',
                 name='Max. Hillman Taper',
                 kernel=kernel_maximum_hillman_taper,
                 description='The maximum Hillman taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='AvgHillmanTaper',
                 name='Avg. Hillman Taper',
                 kernel=kernel_average_hillman_taper,
                 description='The average Hillman taper value',
                 data_format='NEGATIVE_FLOAT'),

    AnalysisItem(variable='MinContraction',
                 name='Min. Contraction',
                 kernel=kernel_minimum_contraction,
                 description='The minimum contraction ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaxContraction',
                 name='Max. Contraction',
                 kernel=kernel_maximum_contraction,
                 description='The maximum contraction ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgContraction',
                 name='Avg. Contraction',
                 kernel=kernel_average_contraction,
                 description='The average contraction ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='MinDaughterRatio',
                 name='Min. Daughter Ratio',
                 kernel=kernel_minimum_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The minimum daughter ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaxDaughterRatio',
                 name='Max. Daughter Ratio',
                 kernel=kernel_maximum_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The maximum daughter ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgDaughterRatio',
                 name='Avg. Daughter Ratio',
                 kernel=kernel_average_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The average daughter ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='MinParentDaughterRatio',
                 name='Min. Parent  Daughter Ratio',
                 kernel=kernel_minimum_parent_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The minimum parent daughter ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='MaxParentDaughterRatio',
                 name='Max. Parent  Daughter Ratio',
                 kernel=kernel_maximum_parent_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The maximum parent daughter ratio',
                 data_format='FLOAT'),

    AnalysisItem(variable='AvgParentDaughterRatio',
                 name='Avg. Parent Daughter Ratio',
                 kernel=kernel_average_parent_daughter_ratio,
                 description='NOTE: If this value is ZERO, this means that the arbor has no '
                             'branching. The average parent daughter ratio',
                 data_format='FLOAT'),

    ################################################################################################
    # Angle-related items
    ################################################################################################
    AnalysisItem(variable='MinimumLocalBifurcationAngle',
                 name='Min. Local Bifurcation Angle',
                 kernel=kernel_minimum_local_bifurcation_angle,
                 description='The minimum local bifurcation angle (computed from the first two '
                             'samples along the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    AnalysisItem(variable='MaximumLocalBifurcationAngle',
                 name='Max. Local Bifurcation Angle',
                 kernel=kernel_maximum_local_bifurcation_angle,
                 description='The minimum local bifurcation angle (computed from the first two '
                             'samples along the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    AnalysisItem(variable='AverageLocalBifurcationAngle',
                 name='Avg. Local Bifurcation Angle',
                 kernel=kernel_average_local_bifurcation_angle,
                 description='The average local bifurcation angle (computed from the first two '
                             'samples along the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    AnalysisItem(variable='MinimumGlobalBifurcationAngle',
                 name='Min. Global Bifurcation Angle',
                 kernel=kernel_minimum_global_bifurcation_angle,
                 description='The minimum global bifurcation angle (computed from the first and '
                             'last samples of the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    AnalysisItem(variable='MaximumGlobalBifurcationAngle',
                 name='Max. Global Bifurcation Angle',
                 kernel=kernel_maximum_global_bifurcation_angle,
                 description='The minimum global bifurcation angle (computed from the first and '
                             'last samples of the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    AnalysisItem(variable='AverageGlobalBifurcationAngle',
                 name='Avg. Global Bifurcation Angle',
                 kernel=kernel_average_global_bifurcation_angle,
                 description='The average global bifurcation angle (computed from the first and '
                             'last samples of the section)',
                 data_format='FLOAT',
                 unit='ROTATION'),

    ################################################################################################
    # Length-related items
    ################################################################################################
    AnalysisItem(variable='TotalLength',
                 name='Total Length',
                 kernel=kernel_total_length,
                 description='The total length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='MinSectionLength',
                 name='Min. Section Length',
                 kernel=kernel_minimum_section_length,
                 description='The maximum section length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='MaxSectionLength',
                 name='Max. Section Length',
                 kernel=kernel_maximum_section_length,
                 description='The minimum section length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='AvgSectionLength',
                 name='Avg. Section Length',
                 kernel=kernel_average_section_length,
                 description='Average section length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='ShortSections',
                 name='Short Sections',
                 kernel=kernel_short_sections,
                 description='The total number of short sections '
                             '(length is smaller than the sum of the radii of the terminal samples)',
                 data_format='INT'),

    AnalysisItem(variable='MinSegmentLength',
                 name='Min. Segment Length ',
                 kernel=kernel_minimum_segment_length,
                 description='The minimum segment length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='MaxSegmentLength',
                 name='Max. Segment Length ',
                 kernel=kernel_maximum_segment_length,

                 description='The maximum segment length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='AvgSegmentLength',
                 name='Avg. Segment Length ',
                 kernel=kernel_average_segment_length,
                 description='The average segment length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    AnalysisItem(variable='ZeroLengthSegments',
                 name='Zero-length Segments',
                 kernel=kernel_zero_length_segments,
                 description='The total number of zero-length segments (or duplicate samples)',
                 data_format='INT'),

    ################################################################################################
    # Area-related items
    ################################################################################################
    AnalysisItem(variable='TotalSurfaceArea',
                 name='Total Surface Area',
                 kernel=kernel_total_surface_area,
                 description='Total surface area',
                 data_format='FLOAT',
                 unit='AREA'),

    AnalysisItem(variable='MinSectionSurfaceArea',
                 name='Min. Section Surface Area',
                 kernel=kernel_minimum_section_surface_area,
                 description='The minimum section surface area',
                 data_format='FLOAT',
                 unit='AREA'),

    AnalysisItem(variable='MaxSectionSurfaceArea',
                 name='Max. Section Surface Area',
                 kernel=kernel_maximum_section_surface_area,
                 description='The maximum section surface area',
                 data_format='FLOAT',
                 unit='AREA'),

    AnalysisItem(variable='AvgSurfaceAreaPerSection',
                 name='Avg. Section Surface Area',
                 kernel=kernel_average_section_surface_area,
                 description='The average section surface area',
                 data_format='FLOAT',
                 unit='AREA'),

    ################################################################################################
    # Volume-related items
    ################################################################################################
    AnalysisItem(variable='TotalVolume',
                 name='Total Volume',
                 kernel=kernel_total_volume,
                 description='the total volume',
                 data_format='FLOAT',
                 unit='VOLUME'),

    AnalysisItem(variable='MinSectionVolume',
                 name='Min. Section Volume',
                 kernel=kernel_minimum_section_volume,
                 description='The minimum section volume',
                 data_format='FLOAT',
                 unit='VOLUME'),

    AnalysisItem(variable='MaxSectionVolume',
                 name='Max. Section Volume',
                 kernel=kernel_maximum_section_volume,
                 description='The maximum section volume',
                 data_format='FLOAT',
                 unit='VOLUME'),

    AnalysisItem(variable='AvgSectionVolume',
                 name='Avg. Section Volume',
                 kernel=kernel_average_section_volume,
                 description='The average section volume',
                 data_format='FLOAT',
                 unit='VOLUME'),
]

####################################################################################################
# Soma analysis items
####################################################################################################
ui_soma_analysis_items = [

    AnalysisItem(variable='SomaReportedRadius',
                 name='Soma Reported Radius',
                 kernel=kernel_soma_get_reported_mean_radius,
                 description='The radius of the soma as reported in the morphology file',
                 data_format='FLOAT'),

    AnalysisItem(variable='SomaMinimumRadius',
                 name='Soma Min. Radius',
                 kernel=kernel_soma_get_minimum_radius,
                 description='The minimum radius of the soma as based on the reported profile '
                             'points and the root samples of all the connected arbors (or stems)',
                 data_format='FLOAT'),

    AnalysisItem(variable='SomaMaximumRadius',
                 name='Soma Max. Radius',
                 kernel=kernel_soma_get_maximum_radius,
                 description='The maximum radius of the soma as based on the reported profile '
                             'points and the root samples of all the connected arbors (or stems)',
                 data_format='FLOAT'),

    AnalysisItem(variable='ReportedSomaSurfaceArea',
                 name='Soma Surface Area',
                 kernel=kernel_soma_get_average_surface_area,
                 description='The surface area of the soma as reported in the morphology file '
                             'in \u03BCm\u00b2',
                 data_format='FLOAT'),

    AnalysisItem(variable='ReportedSomaVolume',
                 name='Soma Volume',
                 kernel=kernel_soma_get_average_volume,
                 description='The volume of the soma as reported in the morphology file in '
                             '\u03BCm\u00b3',
                 data_format='FLOAT'),

    AnalysisItem(variable='NumberProfilePoints',
                 name='# Profile Points',
                 kernel=kernel_soma_count_profile_points,
                 description='The number of profile points of the soma',
                 data_format='INT'),
]

####################################################################################################
# Global analysis items, only applied on a global level not per-arbor level
####################################################################################################
ui_global_analysis_items = [

    ################################################################################################
    # Arborization items
    ################################################################################################
    AnalysisItem(variable='NumberApicalDendritesLoaded',
                 name='Apical Dendrites',
                 kernel=kernel_global_number_apical_dendrites,
                 description='The total number of apical dendrites of the morphology',
                 data_format='INT'),

    AnalysisItem(variable='NumberBasalDendritesLoaded',
                 name='Basal Dendrites',
                 kernel=kernel_global_number_basal_dendrites,
                 description='The total number of basal dendrites of the morphology',
                 data_format='INT'),

    AnalysisItem(variable='NumberAxonsLoaded',
                 name='Axons',
                 kernel=kernel_global_number_axons,
                 description='The total number of axons of the morphology',
                 data_format='INT'),

    AnalysisItem(variable='NumberNeurites',
                 name='Total # Neurites',
                 kernel=kernel_global_total_number_neurites,
                 description='The total number of the arbors in the morphology '
                             'whether connected to the soma or not',
                 data_format='INT'),

    AnalysisItem(variable='NumberStems',
                 name='Total # Stems',
                 kernel=kernel_global_total_number_stems,
                 description='The total number of stems or the arbors that emanate from the '
                             'soma in the morphology',
                 data_format='INT'),
]
