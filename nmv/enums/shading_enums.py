####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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
# @Shader
####################################################################################################
class Shader:
    """Shader enumerators
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

    # Transparent
    TRANSPARENT = 'TRANSPARENT_SHADER'

    # Glossy shader
    GLOSSY = 'GLOSSY_SHADER'

    # Wax shader
    WAX = 'WAX_SHADER'

    # Glossy bympy shader
    GLOSSY_BUMPY = 'GLOSSY_BUMPY_SHADER'

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

    # Plastic
    PLASTIC = 'PLASTIC_SHADER'

    # Wire frame
    WIRE_FRAME = 'WIREFRAME_SHADER'

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
            return Shader.FLAT
        elif shader_type == 'electron-light':
            return Shader.ELECTRON_LIGHT
        elif shader_type == 'electron-dark':
            return Shader.ELECTRON_DARK
        elif shader_type == 'super-electron-light':
            return Shader.SUPER_ELECTRON_LIGHT
        elif shader_type == 'super-electron-dark':
            return Shader.SUPER_ELECTRON_DARK
        elif shader_type == 'transparent':
            return Shader.TRANSPARENT
        elif shader_type == 'glossy':
            return Shader.GLOSSY
        elif shader_type == 'glossy-bumpy':
            return Shader.GLOSSY_BUMPY
        elif shader_type == 'lambert':
            return Shader.LAMBERT_WARD
        elif shader_type == 'toon':
            return Shader.LAMBERT_WARD
        elif shader_type == 'wireframe':
            return Shader.WIRE_FRAME
        else:
            return Shader.LAMBERT_WARD

    ################################################################################################
    # A list of all the available materials in NeuroMorphoVis
    ################################################################################################
    MATERIAL_ITEMS = [
        (LAMBERT_WARD,
         'Default',
         "Use the default Lambert Ward shader. This shader is used to create high resolution "
         "images in few seconds. The rendering quality of this shader is not the best"),

        (FLAT,
         'Flat',
         "Use Flat shader. This shader is used to create high resolution images in few seconds. "
         "The rendering quality of this shader is not the best"),

        (TOON,
         'Toon',
         "Use Toon shader. This shader is used to create high resolution images in few seconds. "
         "The rendering quality of this shader is not the best"),

        (TRANSPARENT,
         'Transparent',
         "Transparent shader to show the internals of the mesh"),

        (ELECTRON_LIGHT,
         'Electron Light',
         "Light electron microscopy shader"),

        (ELECTRON_DARK,
         'Electron Dark',
         "Dark electron microscopy shader"),

        (SUPER_ELECTRON_LIGHT,
         'Super Electron Light',
         "Highly detailed light electron shader"),

        (SUPER_ELECTRON_DARK,
         'Super Electron Dark',
         "Highly detailed dark electron shader"),

        (WAX,
         'Wax',
         "Creates high quality images. This shader might take up to few hours to create a single "
         "image depending on the complexity of the neuron"),

        (GLOSSY,
         'Plastic',
         "Creates high quality images. This shader might take up to few hours to create a single "
         "image depending on the complexity of the neuron"),

        (GLOSSY_BUMPY,
         'Glossy Bumpy',
         "Creates high quality images. This shader might take up to few hours to create a single "
         "image depending on the complexity of the neuron"),

        (WIRE_FRAME,
         'Wire-frame',
         "Wire-frame shader to show the polygons of the mesh")
    ]
