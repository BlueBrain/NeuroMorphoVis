####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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
import nmv.enums
import nmv.consts


####################################################################################################
# @get_morphology_image_suffixes_from_view
####################################################################################################
def get_morphology_image_suffixes_from_view(camera_view):
    """Gets the suffix that will be appended to the morphology image from the camera view.
    The result will be in a list to allow rendering multiple views at the same moment even if it
    contains a single element.

    :param camera_view:
        The camera view.
    :return
        Image suffix list.
    """

    # Front
    if camera_view == nmv.enums.Camera.View.FRONT:
        return [nmv.consts.Suffix.MORPHOLOGY_FRONT]

    # Side
    elif camera_view == nmv.enums.Camera.View.SIDE:
        return [nmv.consts.Suffix.MORPHOLOGY_SIDE]

    # Top
    elif camera_view == nmv.enums.Camera.View.TOP:
        return [nmv.consts.Suffix.MORPHOLOGY_TOP]

    # All views
    elif camera_view == nmv.enums.Camera.View.ALL_VIEWS:
        return [nmv.consts.Suffix.MORPHOLOGY_FRONT,
                nmv.consts.Suffix.MORPHOLOGY_SIDE,
                nmv.consts.Suffix.MORPHOLOGY_TOP]

    # By default, render the front view
    else:
        return [nmv.consts.Suffix.MORPHOLOGY_FRONT]


####################################################################################################
# @get_mesh_image_suffixes_from_view
####################################################################################################
def get_mesh_image_suffixes_from_view(camera_view):
    """Gets the suffix that will be appended to the mesh image from the camera view.
    The result will be in a list to allow rendering multiple views at the same moment even if it
    contains a single element.

    :param camera_view:
        The camera view.
    :return
        Image suffix list.
    """

    # Front
    if camera_view == nmv.enums.Camera.View.FRONT:
        return [nmv.consts.Suffix.MESH_FRONT]

    # Side
    elif camera_view == nmv.enums.Camera.View.SIDE:
        return [nmv.consts.Suffix.MESH_SIDE]

    # Top
    elif camera_view == nmv.enums.Camera.View.TOP:
        return [nmv.consts.Suffix.MESH_TOP]

    # All views
    elif camera_view == nmv.enums.Camera.View.ALL_VIEWS:
        return [nmv.consts.Suffix.MESH_FRONT,
                nmv.consts.Suffix.MESH_SIDE,
                nmv.consts.Suffix.MESH_TOP]

    # By default, render the front view
    else:
        return [nmv.consts.Suffix.MESH_FRONT]


####################################################################################################
# @get_soma_image_suffixes_from_view
####################################################################################################
def get_soma_image_suffixes_from_view(camera_view):
    """Gets the suffix that will be appended to the soma image from the camera view.
    The result will be in a list to allow rendering multiple views at the same moment even if it
    contains a single element.

    :param camera_view:
        The camera view.
    :return
        Image suffix list.
    """

    # Front
    if camera_view == nmv.enums.Camera.View.FRONT:
        return [nmv.consts.Suffix.SOMA_FRONT]

    # Side
    elif camera_view == nmv.enums.Camera.View.SIDE:
        return [nmv.consts.Suffix.SOMA_SIDE]

    # Top
    elif camera_view == nmv.enums.Camera.View.TOP:
        return [nmv.consts.Suffix.SOMA_TOP]

    # All views
    elif camera_view == nmv.enums.Camera.View.ALL_VIEWS:
        return [nmv.consts.Suffix.SOMA_FRONT,
                nmv.consts.Suffix.SOMA_SIDE,
                nmv.consts.Suffix.SOMA_TOP]

    # By default, render the front view
    else:
        return [nmv.consts.Suffix.SOMA_FRONT]
