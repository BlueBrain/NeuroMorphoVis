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

# Internal imports
from .structs import *
from .kernels import *
import nmv.enums
import nmv.consts


####################################################################################################
# Analysis distributions
####################################################################################################
distributions = [

    AnalysisDistribution(
        name='Total Number of Samples per Arbor',
        description='The total number of sampler per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Samples / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_SAMPLE_PER_ARBOR,
        figure_xlabel='Number of Samples',
        compute_total_kernel=compute_number_of_samples_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Total Number of Terminal Tips per Arbor',
        description='The total number of terminal tips per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Terminal Tips / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_TERMINAL_TIPS_PER_ARBOR,
        figure_xlabel='Number of Tips',
        compute_total_kernel=compute_total_number_of_terminal_tips_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Number of Terminal Segments per Arbor',
        description='The total number of terminal segments per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Terminal Segments / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_TERMINAL_SEGMENTS_PER_ARBOR,
        figure_xlabel='Number of Segments',
        compute_total_kernel=compute_total_number_of_terminal_segments_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Number of Bifurcations per Arbor',
        description='The total number of bifurcations per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Bifurcations / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_BIFURCATIONS_PER_ARBOR,
        figure_xlabel='Number of Bifurcations',
        compute_total_kernel=compute_total_number_of_bifurcations_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Maximum Branching Order per Arbor',
        description='The maximum branching order per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Branching Order / Arbor',
        figure_name=nmv.consts.Analysis.MAXIMUM_BRANCHING_ORDER_PER_ARBOR,
        figure_xlabel='Branching Order',
        compute_total_kernel=compute_maximum_branching_order_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Arbor Length',
        description='The total length of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Length',
        figure_name=nmv.consts.Analysis.ARBOR_LENGTH ,
        figure_xlabel='Length (\u03BCm)',
        compute_total_kernel=compute_total_length_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Total Number of Section per Arbor',
        description='The total number of sections per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Sections / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_SECTIONS_PER_ARBOR,
        figure_xlabel='Number of Sections',
        compute_total_kernel=compute_total_number_of_sections_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Total Number of Short Section per Arbor',
        description='The total number of short sections (where the length of the section is '
                    'less than the sum of the diameters of the first and last samples) per arbor '
                    'in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Short Sections / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_SHORT_SECTIONS_PER_ARBOR,
        figure_xlabel='Number of Short Sections',
        compute_total_kernel=compute_number_of_short_sections_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Maximum Path Distance per Arbor',
        description='The maximum distance from the soma to the terminal tip per arbor in the '
                    'morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Path Distance / Arbor',
        figure_name=nmv.consts.Analysis.MAXIMUM_PATH_DISTANCE_PER_ARBOR,
        figure_xlabel='Path Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_maximum_path_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Maximum Euclidean Distance per Arbor',
        description='The maximum radial distance from the soma to the terminal tip per arbor in '
                    'the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Maximum Euclidean Distance / Arbor',
        figure_name=nmv.consts.Analysis.MAXIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR,
        figure_xlabel='Radial Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_maximum_euclidean_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Minimum Euclidean Distance per Arbor',
        description='The minimum radial distance from the soma to the first sample along every '
                    'arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Minimum Euclidean Distance / Arbor',
        figure_name=nmv.consts.Analysis.MINIMUM_EUCLIDEAN_DISTANCE_PER_ARBOR,
        figure_xlabel='Radial Distance from Soma (\u03BCm)',
        compute_total_kernel=compute_minimum_euclidean_distance_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Arbor Surface Area',
        description='The surface area of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Surface Area',
        figure_name=nmv.consts.Analysis.ARBOR_SURFACE_AREA,
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_total_kernel=compute_arbor_total_surface_area,
        add_percentage=True),

    AnalysisDistribution(
        name='Arbor Volume',
        description='The volume of each arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Arbor Volume',
        figure_name=nmv.consts.Analysis.ARBOR_VOLUME,
        figure_xlabel='Volume (\u03BCm\u00b3)',
        compute_total_kernel=compute_arbor_total_volume,
        add_percentage=True),

    AnalysisDistribution(
        name='Sections Length Range per Arbor',
        description='The range of sections length per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Length Range / Arbor',
        figure_name=nmv.consts.Analysis.SECTIONS_LENGTH_RANGE_PER_ARBOR,
        figure_xlabel='Length (\u03BCm)',
        compute_min_kernel=compute_minimum_section_length_of_arbor,
        compute_avg_kernel=compute_average_section_length_of_arbor,
        compute_max_kernel=compute_maximum_section_length_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Length Range per Arbor',
        description='The range of segments length per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Length Range / Arbor',
        figure_name=nmv.consts.Analysis.SEGMENTS_LENGTH_RANGE_PER_ARBOR,
        figure_xlabel='Length (\u03BCm)',
        compute_min_kernel=compute_minimum_segment_length_of_arbor,
        compute_avg_kernel=compute_average_segment_length_of_arbor,
        compute_max_kernel=compute_maximum_segment_length_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Sections Surface Area Range per Arbor',
        description='The range of sections surface area per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Surface Area Range / Arbor',
        figure_name=nmv.consts.Analysis.SECTIONS_SURFACE_RANGE_PER_ARBOR,
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_min_kernel=compute_minimum_section_surface_area,
        compute_avg_kernel=compute_average_section_surface_area,
        compute_max_kernel=compute_maximum_section_surface_area,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Surface Area Range per Arbor',
        description='The range of segments surface area per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Surface Area Range / Arbor',
        figure_name=nmv.consts.Analysis.SEGMENTS_SURFACE_RANGE_PER_ARBOR,
        figure_xlabel='Area (\u03BCm\u00b2)',
        compute_min_kernel=compute_minimum_segment_surface_area,
        compute_avg_kernel=compute_average_segment_surface_area,
        compute_max_kernel=compute_maximum_segment_surface_area,
        add_percentage=False),

    AnalysisDistribution(
        name='Sections Volume Range per Arbor',
        description='The range of sections volume per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Sections Volume Range / Arbor',
        figure_name=nmv.consts.Analysis.SECTIONS_VOLUME_RANGE_PER_ARBOR,
        figure_xlabel='Volume (\u03BCm\u00b3)',
        compute_min_kernel=compute_minimum_section_volume,
        compute_avg_kernel=compute_average_section_volume,
        compute_max_kernel=compute_maximum_section_volume,
        add_percentage=False),

    AnalysisDistribution(
        name='Segments Volume Range per Arbor',
        description='The range of segments volume per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Segments Volume Range / Arbor',
        figure_name=nmv.consts.Analysis.SEGMENTS_VOLUME_RANGE_PER_ARBOR,
        figure_xlabel='Volume (\u03BCm\u00b3)',
        compute_min_kernel=compute_minimum_segment_volume,
        compute_avg_kernel=compute_average_segment_volume,
        compute_max_kernel=compute_maximum_segment_volume,
        add_percentage=False),

    AnalysisDistribution(
        name='Contraction Range per Arbor',
        description='The range of contraction per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Contraction / Arbor',
        figure_name=nmv.consts.Analysis.CONTRACTION_PER_ARBOR,
        figure_xlabel='',
        compute_min_kernel=compute_minimum_section_contraction_of_arbor,
        compute_avg_kernel=compute_average_section_contraction_of_arbor,
        compute_max_kernel=compute_maximum_section_contraction_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Samples Radii Range per Arbor',
        description='The range of samples radii per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Samples Radii Range / Arbor',
        figure_name=nmv.consts.Analysis.SAMPLES_RADII_PER_ARBOR,
        figure_xlabel='Sample Radius (\u03BCm)',
        compute_min_kernel=compute_minimum_sample_radius_of_arbor,
        compute_avg_kernel=compute_average_sample_radius_of_arbor,
        compute_max_kernel=compute_maximum_sample_radius_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Burke Taper Range per Arbor',
        description='The range of Burke taper per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Burke Taper Range / Arbor',
        figure_name=nmv.consts.Analysis.TAPER_1_RANGE_PER_ARBOR,
        figure_xlabel='Burke Taper',
        compute_min_kernel=compute_minimum_burke_taper_of_arbor,
        compute_avg_kernel=compute_average_burke_taper_of_arbor,
        compute_max_kernel=compute_maximum_burke_taper_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Hillman Taper Range per Arbor',
        description='The range of Hillman taper per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Hillman Taper Range / Arbor',
        figure_name=nmv.consts.Analysis.TAPER_2_RANGE_PER_ARBOR,
        figure_xlabel='Hillman Taper',
        compute_min_kernel=compute_minimum_hillman_taper_of_arbor,
        compute_avg_kernel=compute_average_hillman_taper_of_arbor,
        compute_max_kernel=compute_maximum_hillman_taper_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Daughter Ratio Range per Arbor',
        description='The range of the daughter ration per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Daughter Ratio Range / Arbor',
        figure_name=nmv.consts.Analysis.DAUGHTER_RATIO_RANGE_PER_ARBOR,
        figure_xlabel='Daughter Ratio',
        compute_min_kernel=compute_minimum_daughter_ratio_of_arbor,
        compute_avg_kernel=compute_average_daughter_ratio_of_arbor,
        compute_max_kernel=compute_maximum_daughter_ratio_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Parent Daughter Ratio Range per Arbor',
        description='The range of the parent daughter ration per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Parent Daughter Ratio Range / Arbor',
        figure_name=nmv.consts.Analysis.PARENT_DAUGHTER_RATIO_RANGE_PER_ARBOR,
        figure_xlabel='Parent Daughter Ratio',
        compute_min_kernel=compute_minimum_parent_daughter_ratio_of_arbor,
        compute_avg_kernel=compute_average_parent_daughter_ratio_of_arbor,
        compute_max_kernel=compute_maximum_parent_daughter_ratio_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Total Number of Zero-radii Samples per Arbor',
        description='The total number of zero-radii sampler per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR,
        figure_title='Number of Zero-radii Samples / Arbor',
        figure_name=nmv.consts.Analysis.NUMBER_ZERO_RADII_SAMPLES_PER_ARBOR,
        figure_xlabel='Number of Samples',
        compute_total_kernel=compute_number_of_zero_radius_samples_per_section_of_arbor,
        add_percentage=True),

    AnalysisDistribution(
        name='Local Bifurcation Angle Range per Arbor',
        description='The range of the local bifurcation angles per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Local Bifurcation Angle Range / Arbor',
        figure_name=nmv.consts.Analysis.LOCAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR,
        figure_xlabel='Angle (Degrees \u00B0)',
        compute_min_kernel=compute_minimum_local_bifurcation_angle_of_arbor,
        compute_avg_kernel=compute_average_local_bifurcation_angle_of_arbor,
        compute_max_kernel=compute_maximum_local_bifurcation_angle_of_arbor,
        add_percentage=False),

    AnalysisDistribution(
        name='Global Bifurcation Angle Range per Arbor',
        description='The range of the global bifurcation angles per arbor in the morphology',
        data_format=nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR,
        figure_title='Global Bifurcation Angle Range / Arbor',
        figure_name=nmv.consts.Analysis.GLOBAL_BIFURCATION_ANGLE_RANGE_PER_ARBOR,
        figure_xlabel='Angle (Degrees \u00B0)',
        compute_min_kernel=compute_minimum_global_bifurcation_angle_of_arbor,
        compute_avg_kernel=compute_average_global_bifurcation_angle_of_arbor,
        compute_max_kernel=compute_maximum_global_bifurcation_angle_of_arbor,
        add_percentage=False),
]

####################################################################################################
# Global analysis items, only applied on a global level not per-arbor level
####################################################################################################
distributionss = [














]

'''
distributionss = [

    
    

    


    

    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii,
        description='Radii range',
        data_format='FLOAT',
        figure_title='Samples Radii',
        figure_axis_label='Sample Radius (\u03BCm)',
        figure_label='samples-radii'),

]
'''
