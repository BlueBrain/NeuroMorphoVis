####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


####################################################################################################
# @Shading
####################################################################################################
class Shading:
    """Shading enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Flat or 'shade-less' shader
    FLAT = 'FLAT_SHADER'

    # Blender default lambert shader
    LAMBERT_WARD = 'LAMBERT_WARD_SHADER'

    # Toon shader
    TOON = 'TOON_SHADER'

    # Glossy shader
    GLOSSY = 'GLOSSY_SHADER'

    # Glossy bympy shader
    GLOSSY_BUMPY = 'GLOSSY_SHADER'

    # Electron (light) shader
    ELECTRON_LIGHT = 'ELECTRON_LIGHT_SHADER'

    # Electron (dark) shader
    ELECTRON_DARK = 'ELECTRON_DARK_SHADER'

    # Super resolution electron (light) shader
    SUPER_ELECTRON_LIGHT = 'SUPER_ELECTRON_LIGHT_SHADER'

    # Super resolution electron (dark) shader
    SUPER_ELECTRON_DARK = 'SUPER_ELECTRON_DARK_SHADER'

    # Sub-surface scattering shader
    SUB_SURFACE_SCATTERING = 'SUB_SURFACE_SCATTERING_SHADER'

    # Shadow
    SHADOW = 'SHADOW_SHADER'

    # Plastic
    PLASTIC = 'PLASTIC_SHADER'

    # Cracks
    CRACKS = 'CRACKS_SHADER'

    # Grid
    GRID = 'GRID_SHADER'

    # Granular
    GRANULAR = 'GRANULAR_SHADER'

    # Wave
    WAVE = 'WAVE_SHADER'

    ################################################################################################
    # get_enum
    ################################################################################################
    @staticmethod
    def get_enum(shader_type):
        """Return the shader enumerator from the type

        :param shader_type:
            The type of the shader.
        :return:
            The shader enumerator.
        """
        if shader_type == 'flat':
            return Shading.FLAT
        elif shader_type == 'electron-light':
            return Shading.ELECTRON_LIGHT
        elif shader_type == 'electron-dark':
            return Shading.ELECTRON_DARK
        elif shader_type == 'super-electron-light':
            return Shading.SUPER_ELECTRON_LIGHT
        elif shader_type == 'super-electron-dark':
            return Shading.SUPER_ELECTRON_DARK
        elif shader_type == 'shadow':
            return Shading.SHADOW
        elif shader_type == 'glossy':
            return Shading.GLOSSY
        elif shader_type == 'glossy-bumpy':
            return Shading.GLOSSY_BUMPY
        elif shader_type == 'lambert':
            return Shading.LAMBERT_WARD
        elif shader_type == 'plastic':
            return Shading.PLASTIC
        elif shader_type == 'cracks':
            return Shading.CRACKS
        elif shader_type == 'grid':
            return Shading.GRID
        elif shader_type == 'granular':
            return Shading.GRANULAR
        elif shader_type == 'wave':
            return Shading.WAVE

        else :
            return Shading.LAMBERT_WARD

    ################################################################################################
    # A list of all the available materials in NeuroMorphoVis
    ################################################################################################
    MATERIAL_ITEMS = [
        (LAMBERT_WARD,
         'Lambert Ward',
         "Lambert Ward Shader"),

        (SUPER_ELECTRON_LIGHT,
         'Super Electron Light',
         "Highly Detailed Light Electron Shader"),

        (SUPER_ELECTRON_DARK,
         'Super Electron Dark',
         "Highly Detailed Dark Electron Shader"),

        (ELECTRON_LIGHT,
         'Electron Light',
         "Light Electron Shader"),

        (ELECTRON_DARK,
         'Electron Dark',
         "Use Dark Electron Shader"),

        (GLOSSY,
         'Glossy',
         "Glossy Bumpy Shader"),

        (GLOSSY_BUMPY,
         'Glossy Bumpy',
         "Glossy Bumpy Shader"),

        (SHADOW,
         'Shadow',
         "Use Shadows Shader"),

        (FLAT,
         'Flat',
         "Use Flat Shader")
    ]
