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
# @ColorMaps
####################################################################################################
class ColorMaps:
    """ColorMaps enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Default RGB color-map
    RGB = 'RGB_COLOR_MAP'

    # HSV color-map
    HSV = 'HSV_COLOR_MAP'

    # Viridis
    VIRIDIS = 'VIRIDIS_COLOR_MAP'

    # Plasma
    PLASMA = 'PLASMA_COLOR_MAP'

    # Gray-scale
    GRAY_SCALE = 'GRAY_SCALE_COLOR_MAP'

    ################################################################################################
    # get_enum
    ################################################################################################
    @staticmethod
    def get_enum(color_map_name):
        """Return the color-map enumerator from the name

        :param color_map_name:
            The name of the color map.
        :return:
            The color-map enumerator.
        """
        if color_map_name == 'rgb':
            return ColorMaps.RGB
        elif color_map_name == 'hsv':
            return ColorMaps.HSV
        else:
            return ColorMaps.RGB

    ################################################################################################
    # get_hex_color_list
    ################################################################################################
    @staticmethod
    def get_hex_color_list(color_map_enum):

        if color_map_enum == ColorMaps.HSV:
            return ['F92024', '42FDF9', 'FA7380'] 
        elif color_map_enum == ColorMaps.VIRIDIS:
            return ['430652', '308C8B', 'F7E545']
        elif color_map_enum == ColorMaps.PLASMA:
            return ['1B0D85', 'CA4F75', 'EEF447']
        elif color_map_enum == ColorMaps.GRAY_SCALE:
            return ['000000', 'FFFFFF']
        else:
            return ['1B0D85', 'CA4F75', 'EEF447']

    ################################################################################################
    # A list of all the available color-maps in NeuroMorphoVis
    ################################################################################################
    COLOR_MAPS = [

        # HSV
        (HSV, 'HSV', 'HSV color map'),
        
        # Viridis
        (VIRIDIS, 'Viridis', 'Viridis color map'),

        # Plasma
        (PLASMA, 'Plasma', 'Plasma color map'),

        # Gray Scale
        (GRAY_SCALE, 'Gray Scale', 'Gray-scale color map'),        
    ]
