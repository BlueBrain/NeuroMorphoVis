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

# System imports
import os

# Blender imports
import bpy

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.enums
import neuromorphovis.scene


def create_lambert_ward_illumination(name):
    return

def create_super_electron_light_illumination(name):
    return

def create_super_electron_dark_illumination(name):
    return

def create_electron_light_illumination(name):
    return

def create_electron_dark_illumination(name):
    return

def create_shadow_illumination(name):
    return

def create_glossy_illumination(name):
    return

def create_glossy_bumpy_illumination(name):
    return

def create_flat_illumination(name):
    return






####################################################################################################
# @create_light
####################################################################################################
def create_illumination(name,
                        material_type):
    """Create a specific light that corresponds to a given material.

    :param name:
        Light source name.
    :param material_type:
        Material type.
    :return:
        A reference to the created light source.
    """

    # Lambert Ward
    if material_type == nmv.enums.Shading.LAMBERT_WARD:
        return create_lambert_ward_illumination(name='%s_light' % name)

    # Super electron light
    elif material_type == nmv.enums.Shading.SUPER_ELECTRON_LIGHT:
        return create_super_electron_light_illumination(name='%s_light' % name)

    # Super electron dark
    elif material_type == nmv.enums.Shading.SUPER_ELECTRON_DARK:
        return create_super_electron_dark_illumination(name='%s_light' % name)

    # Electron light
    elif material_type == nmv.enums.Shading.ELECTRON_LIGHT:
        return create_electron_light_illumination(name='%s_light' % name)

    # Electron dark
    elif material_type == nmv.enums.Shading.ELECTRON_DARK:
        return create_electron_dark_illumination(name='%s_light' % name)

    # Shadow
    elif material_type == nmv.enums.Shading.SHADOW:
        return create_shadow_illumination(name='%s_light' % name)

    # Glossy
    elif material_type == nmv.enums.Shading.GLOSSY:
        return create_glossy_illumination(name='%s_light' % name)

    # Glossy bumpy
    elif material_type == nmv.enums.Shading.GLOSSY_BUMPY:
        return create_glossy_bumpy_illumination(name='%s_light' % name)

    # Flat
    elif material_type == nmv.enums.Shading.FLAT:
        return create_flat_illumination(name='%s_light' % name)

    # Default
    else:
        return create_lambert_ward_illumination(name='%s_light' % name)