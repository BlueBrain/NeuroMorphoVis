####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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


####################################################################################################
# @ColorCoding
####################################################################################################
class ColorCoding:
    """ColorCoding enumerators
    """

    # Color the morphology by components
    DEFAULT_SCHEME = 'DEFAULT_SCHEME'

    # Use a homogeneous color for all the components in the morphology including soma
    HOMOGENEOUS_COLOR = 'HOMOGENEOUS_COLOR'

    # Use alternating colors for the different components in the morphology
    ALTERNATING_COLORS = 'ALTERNATING_COLORS'

    # Color code the components according to their average radius
    BY_RADIUS = 'COLOR_CODING_BY_RADIUS'

    # Color code the components according to their length
    BY_LENGTH = 'COLOR_CODING_BY_LENGTH'

    # Color code the components according to their area
    BY_SURFACE_AREA = 'COLOR_CODING_BY_AREA'

    # Color code the components according to their volume
    BY_VOLUME = 'COLOR_CODING_BY_VOLUME'

    # Color code the section according to the number of samples it contain
    BY_NUMBER_SAMPLES = 'COLOR_CODING_BY_NUMBER_SAMPLES'

    # Color code a segment based on its path distance from soma
    DISTANCE_FROM_SOMA = 'DISTANCE_FROM_SOMA'

    # Color code the segments based on their Euclidean distance from the origin
    EUCLIDEAN_DISTANCE = 'EUCLIDEAN_DISTANCE'

    # Short Sections
    SHORT_SECTIONS = 'SHORT_SECTION_COLOR_CODING'

    # Color code the different arbors in the morphology by type
    ARBORS_BY_TYPE = 'ARBORS_BY_TYPE'

    ################################################################################################
    # Segments color-coding items to be added to the interface list
    ################################################################################################
    SEGMENTS_COLOR_CODING_ITEMS = [

        # Default coloring scheme
        (DEFAULT_SCHEME,
         'Default Colors',
         'Use a single color for all the segments in the entire morphology, and assign a different '
         'color to the soma or the articulations at the branching points'),

        # Single color for all the components in the morphology including the soma
        (HOMOGENEOUS_COLOR,
         'Homogeneous Color',
         'Use a homogeneous color for all the components in the morphology including the soma'),

        # Alternating colors for every two segments in the morphology
        (ALTERNATING_COLORS,
         'Alternating Colors',
         'Use alternating segments colors to visualize certain patterns in the morphology'),

        # Radius
        (BY_RADIUS,
         'Segment Radius',
         'Color-code the morphology based on the radius of the segment with respect to '
         'the radii distribution along the entire morphology'),

        # Length
        (BY_LENGTH,
         'Segment Length',
         'Color-code the morphology based on the length of the segment with respect to '
         'the segments length distribution along the entire morphology'),

        # Area
        (BY_SURFACE_AREA,
         'Segment Area',
         'Color-code the morphology based on the area of the segment with respect to '
         'the distribution of the segments areas along the entire morphology'),

        # Volume
        (BY_VOLUME,
         'Segment Volume',
         'Color-code the morphology based on the volume of the segment with respect to '
         'the distribution of the segments volumes along the entire morphology'),

        # Path distance
        (DISTANCE_FROM_SOMA,
         'Path Distance from Soma',
         'Color-code the morphology based on the path distance of the segment from the soma'),

        # Euclidean distance
        (EUCLIDEAN_DISTANCE,
         'Euclidean Distance from Soma',
         'Color-code the morphology based on the Euclidean distance of the segment from the soma')
    ]

    ################################################################################################
    # Color coding options per section
    ################################################################################################
    SECTIONS_COLOR_CODING_ITEMS = [

        # Default coloring scheme
        (DEFAULT_SCHEME,
         'Default Colors',
         'Use a single color for all the sections of the same type in the entire morphology and '
         'assign a different color to the soma or the articulations at the branching points'),

        # Single color for all the components in the morphology including the soma
        (HOMOGENEOUS_COLOR,
         'Homogeneous Color',
         'Use a homogeneous color for all the components in the morphology including the soma'),

        # Alternating colors for every two sections in the morphology
        (ALTERNATING_COLORS,
         'Alternating Colors',
         'Use alternating sections colors to visualize certain patterns in the morphology'),

        # Length
        (BY_LENGTH,
         'Section Length',
         'Color-code the morphology based on the length of the section with respect to '
         'the sections length distribution along the entire morphology'),

        # Area
        (BY_SURFACE_AREA,
         'Section Surface Area',
         'Color-code the morphology based on the area of the section with respect to '
         'the distribution of the sections surface areas along the entire morphology'),

        # Volume
        (BY_VOLUME,
         'Section Volume',
         'Color-code the morphology based on the volume of the section with respect to '
         'the distribution of the sections volumes along the entire morphology'),

        # Number of samples
        (BY_NUMBER_SAMPLES,
         'Number of Samples',
         'Color-code the morphology based on the number of samples along the section')
    ]

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ############################################################################################
    # @get_enum
    ############################################################################################
    @staticmethod
    def get_enum(argument):

        # Default scheme
        if argument == 'default':
            return ColorCoding.DEFAULT_SCHEME

        # Homogeneous
        elif argument == 'homogeneous':
            return ColorCoding.HOMOGENEOUS_COLOR

        # Alternating colors
        if argument == 'alternating':
            return ColorCoding.ALTERNATING_COLORS

        # By radius
        elif argument == 'radius':
            return ColorCoding.BY_RADIUS

        # By length
        elif argument == 'length':
            return ColorCoding.BY_LENGTH

        # By area
        elif argument == 'area':
            return ColorCoding.BY_SURFACE_AREA

        # By volume
        elif argument == 'volume':
            return ColorCoding.BY_VOLUME

        # By number of samples along the section
        elif argument == 'number-samples':
            return ColorCoding.BY_NUMBER_SAMPLES

        # By default use the default scheme
        else:
            return ColorCoding.DEFAULT_SCHEME
