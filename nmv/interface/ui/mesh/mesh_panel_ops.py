####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

# Internal imports
import nmv
import nmv.bbox
import nmv.consts
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.skeleton
import nmv.utilities


####################################################################################################
# @draw_spines_options
####################################################################################################
def draw_spines_options(layout,
                        scene):
    """Draw the spines options to the layout of the meshing panel.

    :param layout:
        Meshing panel layout.
    :param scene:
        A reference to the Blender scene.
    """

    # Just keep a reference to the meshing options for convenience
    meshing_options = nmv.interface.ui_options.mesh

    # Spines options
    spine_options_row = layout.row()
    spine_options_row.label(text='Spine Options:', icon='MOD_WAVE')

    # Spines source
    spines_row = layout.row()
    spines_row.label(text='Source:')

    # If you are reading from a BBP circuit, use the locations reported in the circuit, otherwise
    # use random spines
    if scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:
        spines_row.prop(scene, 'NMV_SpinesSourceCircuit', expand=True)
        meshing_options.spines = scene.NMV_SpinesSourceCircuit
    else:
        spines_row.prop(scene, 'NMV_SpinesSourceRandom', expand=True)
        meshing_options.spines = scene.NMV_SpinesSourceRandom

    # If the spines are not ignored
    if not meshing_options.spines == nmv.enums.Meshing.Spines.Source.IGNORE:

        # Spines quality
        spines_quality_row = layout.row()
        spines_quality_row.label(text='Quality:')
        spines_quality_row.prop(scene, 'NMV_SpineMeshQuality', expand=True)
        meshing_options.spines_mesh_quality = scene.NMV_SpineMeshQuality

        # In case of random spines, identify the percentage of randomness
        if meshing_options.spines == nmv.enums.Meshing.Spines.Source.RANDOM:

            # Randomness percentage
            spines_percentage_row = layout.row()
            spines_percentage_row.label(text='Percentage:')
            spines_percentage_row.prop(scene, 'NMV_RandomSpinesPercentage')
            meshing_options.random_spines_percentage = scene.NMV_RandomSpinesPercentage
