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

# Blender imports
import bpy

import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.analysis
import neuromorphovis.enums
import neuromorphovis.file
import neuromorphovis.interface
import neuromorphovis.skeleton


def add_analysis_group_to_panel(arbor_prefix, layout, context):

    # Create a column outline in the panel
    outline = layout.column()

    # Add a label that identifies the arbor
    outline.label(text='%s:' % arbor_prefix)

    # Create a sub-column that aligns the analysis data from the original outline
    analysis_area = outline.column(align=True)

    # Update the analysis area with all the filters
    for item in nmv.analysis.sample_per_neurite:

        # Update the UI entry s
        item.update_ui_entry(arbor_prefix, analysis_area, context)

    # Disable editing the analysis area
    analysis_area.enabled = False
