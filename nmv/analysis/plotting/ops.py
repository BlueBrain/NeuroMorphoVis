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

# System imports
import copy

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.rendering
import nmv.utilities


####################################################################################################
# @plot_analysis_results
####################################################################################################
def plot_analysis_results(morphology,
                          options):
    """Plots the analysis results of the morphology.

    :param morphology:
        The morphology skeleton.
    :param options:
        System options.
    """

    # Create the color palette
    nmv.interface.ui_morphology.create_morphology_color_palette()

    # Ensure to set the branching order to maximum to draw the entire skeleton and dendrogram
    options_clone = copy.deepcopy(options)
    options_clone.morphology.adjust_to_analysis_mode()

    # Render a simplified dendrogram
    builder = nmv.builders.DendrogramBuilder(morphology=morphology, options=options_clone)
    nmv.scene.clear_scene()
    builder.render_highlighted_arbors(dendrogram_type=nmv.enums.Dendrogram.Type.SIMPLIFIED,
                                      resolution=3000)

    # Render a detailed dendrogram
    nmv.scene.clear_scene()
    builder = nmv.builders.DendrogramBuilder(morphology=morphology, options=options_clone)
    builder.render_highlighted_arbors(dendrogram_type=nmv.enums.Dendrogram.Type.DETAILED,
                                      resolution=5000)

    # Render the arbors
    nmv.scene.clear_scene()
    builder = nmv.builders.DisconnectedSectionsBuilder(morphology=morphology,
                                                       options=options_clone)
    builder.render_highlighted_arbors()

    # TODO:
    # Apply the analysis kernels and compile the analysis distributions
    for distribution in nmv.analysis.distributions:
        distribution.apply_kernel(morphology=morphology, options=options)
