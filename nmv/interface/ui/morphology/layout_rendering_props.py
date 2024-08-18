####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# System imports
import time

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene

from .layout_buttons import draw_morphology_rendering_buttons
from .layout_buttons import draw_dendrogram_rendering_button
from .layout_buttons import draw_animated_morphology_rendering_buttons


####################################################################################################
# draw_still_frame_rendering_options
####################################################################################################
def draw_still_frame_rendering_options(panel, scene, options, show_stats=False):

    nmv.interface.ui.common.draw_rendering_header(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_morphology_rendering_view_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_resolution_basis_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_resolution_options(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_image_format_option(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_scale_bar_option(
        layout=panel.layout, scene=scene, options=options)

    draw_morphology_rendering_buttons(panel=panel, scene=scene)

    if show_stats:
        row = panel.layout.row()
        row.prop(scene, 'NMV_MorphologyRenderingTime')
        row.enabled = False


####################################################################################################
# draw_dendrogram_rendering_options
####################################################################################################
def draw_dendrogram_rendering_options(panel, scene, options, show_stats):

    nmv.interface.ui.common.draw_rendering_header(
        layout=panel.layout, scene=scene, options=options)

    nmv.interface.ui.common.draw_resolution_options(
        layout=panel.layout, scene=scene, options=options)

    draw_dendrogram_rendering_button(panel=panel, scene=scene)

    if show_stats:
        row = panel.layout.row()
        row.prop(scene, 'NMV_MorphologyRenderingTime')
        row.enabled = False


####################################################################################################
# draw_animated_sequences_rendering_options
####################################################################################################
def draw_animated_sequences_rendering_options(panel, scene, options):

    draw_animated_morphology_rendering_buttons(panel=panel, scene=scene)


####################################################################################################
# draw_rendering_options
####################################################################################################
def draw_rendering_options(panel, scene, options, show_stats=False):

    if options.morphology.reconstruction_method == nmv.enums.Skeleton.Method.DENDROGRAM:
        draw_dendrogram_rendering_options(
            panel=panel, scene=scene, options=options, show_stats=show_stats)
    else:
        draw_still_frame_rendering_options(
            panel=panel, scene=scene, options=options, show_stats=show_stats)
        draw_animated_sequences_rendering_options(
            panel=panel, scene=scene, options=options)
