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

# Blender imports
import bpy

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.scene


####################################################################################################
# @apply_soft_body_to_object
####################################################################################################
def apply_soft_body_to_object(soft_body_object,
                              vertex_group,
                              soft_body_options):
    """Apply soft-body physics to a given mesh object.

    NOTE: This operator is mainly used for reconstructing a realistic shapes for the somata.

    :param soft_body_object:
        A given soft body mesh object.
    :param vertex_group:
        A set of vertices in the selected mesh that will get deformed.
    :param soft_body_options:
        Soft body options tuned by the user.
    """

    # Deselect all the objects in the scene to avoid any issues
    nmv.scene.ops.deselect_all()

    # Activate the selected object
    nmv.scene.ops.set_active_object(soft_body_object)

    # Create a soft body modifier
    bpy.ops.object.modifier_add(type='SOFT_BODY')
    
    # Adjust the settings of the soft body
    soft_body_settings = bpy.context.object.modifiers["Softbody"].settings

    # Adjust the Soft body settings
    soft_body_settings.effector_weights.gravity = nmv.consts.SoftBody.GRAVITY
    soft_body_settings.goal_spring = soft_body_options.stiffness
    soft_body_settings.goal_max = nmv.consts.SoftBody.GOAL_MAX
    soft_body_settings.goal_min = nmv.consts.SoftBody.GOAL_MIN
    soft_body_settings.goal_default = nmv.consts.SoftBody.GOAL_DEFAULT
    soft_body_settings.vertex_group_goal = vertex_group.name
