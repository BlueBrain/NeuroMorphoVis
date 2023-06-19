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


####################################################################################################
# @ColorMaps
####################################################################################################
class ColorMaps:
    """ColorMaps enumerators"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Tab 10
    TAB_10 = 'TAB_10_COLOR_MAP'

    # Dark 2
    DARK_2 = 'DARK_2_COLOR_MAP'

    # Magma
    MAGMA = 'MAGMA_COLOR_MAP'

    # Terrain
    TERRAIN = 'TERRAIN_COLOR_MAP'

    # GNU Plot
    GNU_PLOT = 'GNU_PLOT_COLOR_MAP'

    # GNU Plot 2
    GNU_PLOT_2 = 'GNU_PLOT_2_COLOR_MAP'

    # Rainbow
    RAINBOW = 'RAINBOW_COLOR_MAP'

    # Jet
    JET = 'JET_COLOR_MAP'

    # Turbo
    TURBO = 'TURBO_COLOR_MAP'

    # Blues
    BLUES = 'BLUES_COLOR_MAP'

    # Greens
    GREENS = 'GREENS_COLOR_MAP'

    # Reds
    REDS = 'REDS_COLOR_MAP'

    # Spectral
    SPECTRAL = 'SPECTRAL_COLOR_MAP'

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
        if color_map_name == 'gnuplot':
            return ColorMaps.GNU_PLOT

        elif color_map_name == 'gnuplot2':
            return ColorMaps.GNU_PLOT_2

        elif color_map_name == 'rainbow':
            return ColorMaps.RAINBOW

        elif color_map_name == 'jet':
            return ColorMaps.JET

        elif color_map_name == 'turbo':
            return ColorMaps.TURBO

        elif color_map_name == 'rainbow':
            return ColorMaps.RAINBOW

        elif color_map_name == 'reds':
            return ColorMaps.REDS

        elif color_map_name == 'blues':
            return ColorMaps.BLUES

        elif color_map_name == 'greens':
            return ColorMaps.GREENS

        elif color_map_name == 'spectral':
            return ColorMaps.SPECTRAL

        elif color_map_name == 'magma':
            return ColorMaps.MAGMA

        elif color_map_name == 'viridis':
            return ColorMaps.VIRIDIS

        elif color_map_name == 'plasma':
            return ColorMaps.PLASMA

        elif color_map_name == 'terrain':
            return ColorMaps.TERRAIN

        elif color_map_name == 'dark2':
            return ColorMaps.DARK_2

        elif color_map_name == 'tab10':
            return ColorMaps.TAB_10

        elif color_map_name == 'gray':
            return ColorMaps.GRAY_SCALE

        else:
            return ColorMaps.GNU_PLOT

    ################################################################################################
    # get_hex_color_list
    ################################################################################################
    @staticmethod
    def get_hex_color_list(color_map_enum):

        if color_map_enum == ColorMaps.GNU_PLOT:
            return ['000000', '5f00c5', '8805f8', 'a61370', 'c02f00', 'd75c00', 'eca100', 'ffff00']

        elif color_map_enum == ColorMaps.GNU_PLOT_2:
            return ['000000', '000090', '1c00ff', '8d03fb', 'ff4db1', 'ff9569', 'ffdf1f', 'ffffff']

        elif color_map_enum == ColorMaps.TAB_10:
            return ['1f77b4', 'ff7f0e', '2ca02c', '9467bd', '8c564b', '7f7f7f', 'bcbd22', '17becf']

        elif color_map_enum == ColorMaps.DARK_2:
            return ['1b9e77', 'd95f02', '7570b3', 'e7298a', '66a61e', 'e6ab02', 'a6761d', '666666']

        elif color_map_enum == ColorMaps.MAGMA:
            return ['000003', '221150', '5e177f', '972c7f', 'd3426d', 'f8755c', 'febb80', 'fbfcbf']

        elif color_map_enum == ColorMaps.TERRAIN:
            return ['333399', '0393f9', '25d36d', 'b5f08a', 'dacf85', '92735e', 'b7a29e', 'ffffff']

        elif color_map_enum == ColorMaps.RAINBOW:
            return ['7f00ff', '376df8', '12c7e5', '5af8c7', 'a4f89e', 'ecc76e', 'ff6d38', 'ff0000']

        elif color_map_enum == ColorMaps.JET:
            return ['00007f', '0010ff', '00a4ff', '3fffb7', 'b7ff3f', 'ffb900', 'ff3000', '7f0000']

        elif color_map_enum == ColorMaps.TURBO:
            return ['30123b', '4675ed', '1bcfd4', '61fc6c', 'd1e834', 'fe9b2d', 'd93806', '7a0402']

        elif color_map_enum == ColorMaps.VIRIDIS:
            return ['440154', '46317e', '365b8c', '277e8e', '1fa187', '49c16d', '9fd938', 'fde724']

        elif color_map_enum == ColorMaps.PLASMA:
            return ['0c0786', '5201a3', '8b09a4', 'b83289', 'db5b67', 'f38748', 'fdbc2a', 'eff821']

        elif color_map_enum == ColorMaps.BLUES:
            return ['f7fbff', 'dae8f5', 'bad6ea', '88bedc', '539dcc', '2a7ab9', '0b559f', '08306b']

        elif color_map_enum == ColorMaps.GREENS:
            return ['f7fcf5', 'e1f3db', 'bbe4b5', '8ed08b', '56b567', '2b944b', '04702f', '00441b']

        elif color_map_enum == ColorMaps.REDS:
            return ['fff5f0', 'fddbcb', 'fcaf93', 'fb8161', 'f44e38', 'd52221', 'a91016', '67000d']

        elif color_map_enum == ColorMaps.SPECTRAL:
            return ['9e0142', 'e1514a', 'fba55c', 'fee899', 'ecf7a2', 'a1d9a4', '479fb3', '5e4fa2']

        elif color_map_enum == ColorMaps.GRAY_SCALE:
            return ['000000', 'ffffff']

        else:
            return ['000000', '5f00c5', '8805f8', 'a61370', 'c02f00', 'd75c00', 'eca100', 'ffff00']

    ################################################################################################
    # A list of all the available color-maps in NeuroMorphoVis
    ################################################################################################
    COLOR_MAPS = [

        (GNU_PLOT, 'GNU Plot', 'GNU Plot (gnuplot) color map'),

        (GNU_PLOT_2, 'GNU Plot 2', 'GNU Plot 2 (gnuplot2) color map'),

        (RAINBOW, 'Rainbow', 'Rainbow (rainbow) color map'),

        (JET, 'Jet', 'Jet (jet) color map'),

        (TURBO, 'Turbo', 'Turbo (turbo) color map'),

        (MAGMA, 'Magma', 'Magma (magma) color map'),

        (VIRIDIS, 'Viridis', 'Viridis color map'),

        (PLASMA, 'Plasma', 'Plasma color map'),

        (BLUES, 'Blues', 'Blues color map'),

        (REDS, 'Reds', 'Reds color map'),

        (GREENS, 'Greens', 'Greens color map'),

        (SPECTRAL, 'Spectral', 'Spectral color map'),

        (TERRAIN, 'Terrain', 'Terrain (terrain) color map'),

        (TAB_10, 'Tab 10', 'Tab 10 (tab10) color map'),

        (DARK_2, 'Dark 2', 'Dark 2 (Dark2) color map'),

        (GRAY_SCALE, 'Gray Scale', 'Gray-scale color map'),
    ]
