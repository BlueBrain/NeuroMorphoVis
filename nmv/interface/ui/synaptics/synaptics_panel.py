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
import os
import subprocess

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

        # Define the use case
        use_case_row = layout.row()
        use_case_row.prop(context.scene, 'NMV_SynapticsUseCase')
        options.synaptics.use_case = context.scene.NMV_SynapticsUseCase

        # Display the options accordingly, based on the use case selection
        if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
            draw_afferent_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
            draw_efferent_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
            draw_afferent_and_efferent_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
            draw_excitatory_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
            draw_inhibitory_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
            draw_excitatory_and_inhibitory_options(layout, context.scene, options)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.SPECIFIC_COLOR_CODED_SET:
            draw_specific_color_coded_set_options(layout, context.scene, options)

        else:
            # No options to show
            pass

        percentage_row = layout.row()
        percentage_row.prop(context.scene, 'NMV_SynapsesPercentage')
        options.synaptics.percentage = context.scene.NMV_SynapsesPercentage

        synapse_radius_row = layout.row()
        synapse_radius_row.prop(context.scene, 'NMV_SynapseRadius')
        options.synaptics.synapses_radius = context.scene.NMV_SynapseRadius

        layout.row().separator()
        reconstruction_button_row = layout.row()
        reconstruction_button_row.operator('nmv.reconstruct_synaptics')


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
            afferent_scheme = options.synaptics.afferent_color_coding

            # Single color
            if afferent_scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
                nmv.bbp.visualize_afferent_and_efferent_synapses(
                    circuit=circuit, gid=options.morphology.gid,
                    visualize_afferent=True, visualize_efferent=False,
                    synapse_radius=options.synaptics.synapses_radius,
                    synapses_percentage=options.synaptics.percentage,
                    afferent_color=nmv.utilities.rgb_vector_to_hex(
                        options.synaptics.afferent_synapses_color),
                    efferent_color=nmv.utilities.rgb_vector_to_hex(
                        options.synaptics.efferent_synapses_color))

            # m-type colors
            elif afferent_scheme == nmv.enums.Synaptics.ColorCoding.MTYPE_COLOR_CODED:

                # Get the color-coding dictionary from the UI
                color_set = {}
                for i in range(len(nmv.consts.Circuit.MTYPES)):
                    color_set[nmv.consts.Circuit.MTYPES[i]] = options.shading.mtypes_colors[i]

                print(color_set)

                nmv.bbp.visualize_afferent_synapses_colored_by_pre_synaptic_mtypes(
                    circuit=circuit, gid=options.morphology.gid,
                    color_dict=color_set,
                    synapse_radius=options.synaptics.synapses_radius,
                    synapses_percentage=options.synaptics.percentage)






                pass

            # e-type colors
            elif afferent_scheme == nmv.enums.Synaptics.ColorCoding.ETYPE_COLOR_CODED:
                pass



        # Efferent synapses (on axon)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
            efferent_scheme = options.synaptics.efferent_color_coding

            # Single color
            if efferent_scheme == nmv.enums.Synaptics.ColorCoding.SINGLE_COLOR:
                nmv.bbp.visualize_afferent_and_efferent_synapses(
                    circuit=circuit, gid=options.morphology.gid,
                    visualize_afferent=False, visualize_efferent=True,
                    synapse_radius=options.synaptics.synapses_radius,
                    synapses_percentage=options.synaptics.percentage,
                    afferent_color=nmv.utilities.rgb_vector_to_hex(
                        options.synaptics.afferent_synapses_color),
                    efferent_color=nmv.utilities.rgb_vector_to_hex(
                        options.synaptics.efferent_synapses_color))

        # Afferent and efferent synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
            nmv.bbp.visualize_afferent_and_efferent_synapses(
                circuit=circuit, gid=options.morphology.gid,
                visualize_afferent=True, visualize_efferent=True,
                synapse_radius=options.synaptics.synapses_radius,
                synapses_percentage=options.synaptics.percentage,
                afferent_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.afferent_synapses_color),
                efferent_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.efferent_synapses_color))


        # Excitatory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=options.morphology.gid,
                visualize_excitatory=True, visualize_inhibitory=False,
                synapse_radius=options.synaptics.synapses_radius,
                synapses_percentage=options.synaptics.percentage,
                exc_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.excitatory_synapses_color),
                inh_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.inhibitory_synapses_color))

        # Inhibitory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
                visualize_excitatory=False, visualize_inhibitory=True,
                synapse_radius=options.synaptics.synapses_radius,
                synapses_percentage=options.synaptics.percentage,
                exc_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.excitatory_synapses_color),
                inh_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.inhibitory_synapses_color))

        # Excitatory and inhibitory synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
            nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
                circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
                visualize_excitatory=True, visualize_inhibitory=True,
                synapse_radius=options.synaptics.synapses_radius,
                synapses_percentage=options.synaptics.percentage,
                exc_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.excitatory_synapses_color),
                inh_color=nmv.utilities.rgb_vector_to_hex(
                    options.synaptics.inhibitory_synapses_color))


        return {'FINISHED'}




        import bluepy

        from bluepy import Circuit

        circuit_config = '/gpfs/bbp.cscs.ch/project/proj83/circuits/Bio_M/20200805/CircuitConfig_h5'

        gid = 961928
        gid = 3793945

        # Read the circuit
        nmv.logger.info('Loading circuit')
        circuit = Circuit(circuit_config)

        material_type = nmv.enums.Shader.LAMBERT_WARD

        # Create the neuron mesh
        nmv.logger.info('Creating the neuron mesh')
        neuron_color = nmv.consts.Color.RED # nmv.utilities.confirm_rgb_color_from_color_string(args.neuron_color)
        neuron_mesh = nmv.bbp.create_symbolic_neuron_mesh_in_circuit(
            circuit=circuit, gid=gid,
            unified_radius=False,
            branch_radius=1.0,
            soma_color=neuron_color,
            basal_dendrites_color=neuron_color,
            apical_dendrites_color=neuron_color,
            axons_color=neuron_color,
            material_type=material_type,
            axon_branching_order=1)

        synapse_groups = nmv.bbp.create_color_coded_synapse_groups_by_pre_mtype(
            circuit=circuit, post_gid=gid)

        # Create the synapses mesh
        nmv.logger.info('Creating the synapse mesh')
        transformation = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit,
                                                                  gid=gid)
        synapses_mesh = nmv.bbp.create_color_coded_synapses_particle_system(
            circuit=circuit, synapse_groups=synapse_groups,
            synapse_radius=2.0,
            synapses_percentage=100,
            inverted_transformation=transformation.inverted(),
            material_type=material_type)

        # Switch to the top view
        nmv.scene.view_axis()

        # View all the objects in the scene
        # if not nmv.interface.ui.Globals.nmv_initialized:
        nmv.scene.ops.view_all_scene()

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
