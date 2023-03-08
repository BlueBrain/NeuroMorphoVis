####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import sys

# Blender imports
import bpy

# Internal imports
import nmv.bbp
import nmv.enums
import nmv.interface
import nmv.utilities
import nmv.scene
from .synaptics_panel_ops import *
from .synaptics_panel_options import *


####################################################################################################
# @IOPanel
####################################################################################################
class NMV_SyynapticsPanel(bpy.types.Panel):
    """NMV Synaptics panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = "OBJECT_PT_NMV_Synaptics"
    bl_label = 'Synaptics Toolbox'
    bl_category = 'NeuroMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}



    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Blender context.
        """

        # Get a reference to the panel layout
        layout = self.layout
        options = nmv.interface.ui_options

        # Select the use case
        use_case_row = layout.row()
        use_case_row.prop(context.scene, 'NMV_SynapticsUseCase')
        options.synaptics.use_case = context.scene.NMV_SynapticsUseCase

        # Display the options accordingly, based on the use case selection
        if context.scene.NMV_SynapticsUseCase != nmv.enums.Synaptics.UseCase.NOT_SELECTED:

            # Reconstruction options
            synapses_options_row = layout.row()
            synapses_options_row.label(text='Synapses Options:', icon='OUTLINER_OB_EMPTY')

            if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
                draw_afferent_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
                draw_efferent_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
                draw_afferent_and_efferent_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
                draw_excitatory_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
                draw_inhibitory_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
                draw_excitatory_and_inhibitory_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)

                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.SPECIFIC_COLOR_CODED_SET:
                draw_specific_color_coded_set_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                draw_single_neuron_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:
                draw_pre_synaptic_pathway_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                # draw_neuron_pair_options(layout=layout, scene=context.scene, options=options)

            elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:
                draw_post_synaptic_pathway_options(layout, context.scene, options)
                draw_common_options_for_all_use_cases(layout, context.scene, options)
                # draw_neuron_pair_options(layout=layout, scene=context.scene, options=options)

            else:
                pass

            layout.row().separator()
            reconstruction_button_row = layout.row()
            reconstruction_button_row.operator('nmv.reconstruct_synaptics')

            layout.row().separator()
            stats_row = self.layout.row()
            stats_row.label(text='Stats:', icon='RECOVER_LAST')
            time_row = self.layout.row()
            time_row.prop(context.scene, 'NMV_SynapticReconstructionTime')
            time_row.enabled = False



####################################################################################################
# @InputOutputDocumentation
####################################################################################################
class NMV_ReconstructSynaptics(bpy.types.Operator):
    """Reconstruct the scene"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_synaptics"
    bl_label = "Reconstruct Synaptics"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import nmv.interface
        import nmv.consts

        # Clear the scene
        nmv.scene.clear_scene()

        # References
        circuit = nmv.interface.ui_circuit
        options = nmv.interface.ui_options

        # Afferent synapses only (on dendrites)
        if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
            nmv.bbp.visualize_afferent_synapses(
                circuit=circuit, gid=options.morphology.gid, options=options)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # Efferent synapses (on axon)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
            nmv.bbp.visualize_efferent_synapses(
                circuit=circuit, gid=options.morphology.gid, options=options)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # Afferent and efferent synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
            nmv.bbp.visualize_afferent_and_efferent_synapses(
                circuit=circuit, gid=options.morphology.gid, options=options,
                visualize_afferent=True, visualize_efferent=True)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # Excitatory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=options.morphology.gid, options=options,
                visualize_excitatory=True, visualize_inhibitory=False)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # Inhibitory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
                visualize_excitatory=False, visualize_inhibitory=True, options=options)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # Excitatory and inhibitory synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
                visualize_excitatory=True, visualize_inhibitory=True, options=options)
            nmv.bbp.visualize_circuit_neuron_for_synaptics(
                circuit=circuit, gid=options.morphology.gid, options=options)

        # TODO: handle errors if no pre-synaptic or post-synaptic cells exist
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:
            nmv.bbp.visualize_shared_synapses_between_two_neurons(
                circuit=circuit,
                pre_gid=options.synaptics.pre_synaptic_gid,
                post_gid=nmv.interface.ui_options.morphology.gid,
                options=options)

        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:
            nmv.bbp.visualize_shared_synapses_between_two_neurons(
                circuit=circuit,
                pre_gid=nmv.interface.ui_options.morphology.gid,
                post_gid=options.synaptics.post_synaptic_gid,
                options=options)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(NMV_SyynapticsPanel)

    # Button(s)
    bpy.utils.register_class(NMV_ReconstructSynaptics)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(NMV_SyynapticsPanel)

    # Button(s)
    bpy.utils.unregister_class(NMV_ReconstructSynaptics)
