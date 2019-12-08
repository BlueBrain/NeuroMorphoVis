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


####################################################################################################
# Global analysis items, only applied on a global level not per-arbor level
####################################################################################################
distributions = [
    AnalysisDistribution(
        name='Total Number of Samples per Arbor',
        description='The total number of sampler per arbor in the morphology',
        data_format='NUMBER_PER_ARBOR',
        figure_title='Number of Samples / Arbor',
        figure_name='number-of-samples-per-arbor',
        figure_xlabel='Number of Samples',
        compute_total_kernel=compute_number_of_samples_of_arbor,
        add_percentage=True),

]

'''
distributionss = [


    AnalysisDistribution(
        name='Number ot Tips',
        kernel=kernel_number_terminal_tips_distribution,
        description='The range of the segments volume',
        data_format='INT',
        figure_title='Number of Terminal Tips / Neurite',
        figure_axis_label='Number of Tips',
        figure_label='number-of-tips'),

    AnalysisDistribution(
        name='Number ot Tips',
        kernel=kernel_number_of_sections_distribution,
        description='The number of sections per arbor',
        data_format='INT',
        figure_title='Number of Sections / Neurite',
        figure_axis_label='Number of Sections',
        figure_label='number-of-sections'),

    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii_range_distribution,
        description='Radii range',
        data_format='FLOAT',
        figure_title='Samples Radii',
        figure_axis_label='Sample Radius (\u03BCm)',
        figure_label='samples-radii'),

    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii_range_distribution,
        description='Radii range',
        data_format='FLOAT',
        figure_title='Sample Radius (\u03BCm)',
        figure_axis_label='Samples Radii',
        figure_label='samples-radii'),

    AnalysisDistribution(
        name='Total Number of Samples per Neurite',
        kernel=kernel_total_number_of_samples_per_arbor_distribution,
        description='The total number of sampler per neurite (or arbor) in the morphology',
        data_format='INT',
        figure_title='Number of Samples / Neurite',
        figure_axis_label='Number of Samples',
        figure_label='number-of-samples-per-neurite'),

    AnalysisDistribution(
        name='Arbor Length',
        kernel=kernel_total_arbor_length_distribution,
        description='The total length of each arbor in the morphology',
        data_format='FLOAT',
        figure_title='Neurite Length',
        figure_axis_label='Length (\u03BCm)',
        figure_label='per-neurite-length'),

    AnalysisDistribution(
        name='Section Length',
        kernel=kernel_sections_length_range_distribution,
        description='The range of the sections length',
        data_format='FLOAT',
        figure_title='Sections Length Range',
        figure_axis_label='Length (\u03BCm)',
        figure_label='sections-length-range'),

    AnalysisDistribution(
        name='Segment Length',
        kernel=kernel_segment_length_range_distribution,
        description='The range of the segments length',
        data_format='FLOAT',
        figure_title='Segments Length Range',
        figure_axis_label='Length (\u03BCm)',
        figure_label='segment-length-range'),

    AnalysisDistribution(
        name='Section Surface Area',
        kernel=kernel_sections_surface_area_range_distribution,
        description='The range of the sections surface area',
        data_format='FLOAT',
        figure_title='Sections Surface Area Range',
        figure_axis_label='Area (\u03BCm\u00b2)',
        figure_label='sections-surface-area-range'),

    AnalysisDistribution(
        name='Segment Surface Area',
        kernel=kernel_segment_surface_area_range_distribution,
        description='The range of the segments surface area',
        data_format='FLOAT',
        figure_title='Segments Surface Area Range',
        figure_axis_label='Area (\u03BCm\u00b2)',
        figure_label='segments-surface-area-range'),

    AnalysisDistribution(
        name='Section Volume',
        kernel=kernel_section_volume_range_distribution,
        description='The range of the sections volume',
        data_format='FLOAT',
        figure_title='Sections Volume Range',
        figure_axis_label='Volume (\u03BCm\u00b3)',
        figure_label='sections-volume-range'),

    AnalysisDistribution(
        name='Segment Volume',
        kernel=kernel_segment_volume_range_distribution,
        description='The range of the segments volume',
        data_format='FLOAT',
        figure_title='Segments Volume Range',
        figure_axis_label='Volume (\u03BCm\u00b3)',
        figure_label='segments-volume-range'),

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

'''

    
        
    AnalysisDistribution(
        name='Samples Radii',
        kernel=kernel_samples_radii,
        description='The distribution of the radii of all the samples in the morphology',
        data_format='INT'),

    



    AnalysisDistribution(
        name='Total Number of Samples',
        kernel=kernel_total_number_of_sections_per_arbor_distribution,
        description='The distribution of the radii of all the samples in the morphology',
        data_format='INT'),

    AnalysisDistribution(
        name='Total Number of Samples',
        kernel=kernel_total_arbor_length_distribution,
        description='The distribution of the radii of all the samples in the morphology',
        data_format='INT'),

    AnalysisDistribution(
        name='Maximum Branching Order ',
        kernel=kernel_maximum_branching_order_distribution,
        description='The maximum branching order',
        data_format='INT'),
    '''

'''

AnalysisDistribution(
    name='Total Arbor Surface Area',
    kernel=kernel_total_arbor_surface_area_distribution,
    description='The distribution of the radii of all the samples in the morphology',
    data_format='INT',
    '(\u03BCm\u00b2)'),

AnalysisDistribution(
    name='Total Arbor Surface Area',
    kernel=kernel_total_arbor_volume_distribution,
    description='The distribution of the radii of all the samples in the morphology',
    data_format='INT'),
'''
