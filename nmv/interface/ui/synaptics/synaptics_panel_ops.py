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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.bbp
import nmv.scene


####################################################################################################
# @reconstruct_synaptics
####################################################################################################
def reconstruct_synaptics(operator, context, circuit, options):

    # Afferent synapses only (on dendrites)
    if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_afferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options, context=context)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        afferent_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberAfferentSynapses = afferent_synapses_count

    # Efferent synapses (on axon)
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_efferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options, context=context)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        efferent_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberEfferentSynapses = efferent_synapses_count

    # Afferent and efferent synapses
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_afferent_and_efferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options,
            visualize_afferent=True, visualize_efferent=True)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        afferent_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberAfferentSynapses = afferent_synapses_count
        efferent_synapses_count = len(synapse_groups[1].synapses_ids_list)
        context.scene.NMV_SynapticsNumberEfferentSynapses = efferent_synapses_count

    # Excitatory synapses only
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options,
            visualize_excitatory=True, visualize_inhibitory=False)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        excitatory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberExcitatorySynapses = excitatory_synapses_count

    # Inhibitory synapses only
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui.globals.options.morphology.gid,
            visualize_excitatory=False, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        inhibitory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberInhibitorySynapses = inhibitory_synapses_count

    # Excitatory and inhibitory synapses
    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui.globals.options.morphology.gid,
            visualize_excitatory=True, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        excitatory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberExcitatorySynapses = excitatory_synapses_count
        inhibitory_synapses_count = len(synapse_groups[1].synapses_ids_list)
        context.scene.NMV_SynapticsNumberInhibitorySynapses = inhibitory_synapses_count

    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:

        # Ensure that the given pre-synaptic GID is an integer
        try:
            int(options.synaptics.pre_synaptic_gid)
        except ValueError:
            operator.report({'ERROR'}, 'Please enter a valid GID as an integer')
            return {'FINISHED'}

        # Ensure that the pre-synaptic and post-synaptic GIDs are not the same
        if int(options.synaptics.pre_synaptic_gid) == int(options.morphology.gid):
            operator.report({'ERROR'}, 'Please enter a valid pre-synaptic GID, that is different '
                                       'from the post-synaptic one')
            return {'FINISHED'}

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.synaptics.pre_synaptic_gid,
            post_gid=options.morphology.gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            operator.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
                            % (str(options.synaptics.pre_synaptic_gid),
                               str(options.morphology.gid)))
            return {'FINISHED'}

        nmv.scene.clear_scene()

        # Create the post-synaptic neuron AT ORIGIN - THIS IS THE FOCUS
        post_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Create the pre-synaptic neuron AT ORIGIN
        pre_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.synaptics.pre_synaptic_gid, options=options)

        # Get the transformations of the pre- and post-synaptic neurons
        pre_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.synaptics.pre_synaptic_gid)
        post_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.morphology.gid)

        # Since the focus is given to the post-synaptic neuron; it is the originally loaded one,
        # transform the pre-synaptic neuron w.r.t to the post synaptic one
        pre_synaptic_neuron_mesh.matrix_world = pre_synaptic_transformation
        pre_synaptic_neuron_mesh.matrix_world = \
            post_synaptic_transformation.inverted() @ pre_synaptic_neuron_mesh.matrix_world

        # Transform the synapses to be loaded on the post-synaptic neuron
        nmv.bbp.visualize_shared_synapses_between_two_neurons(
            circuit=circuit,
            pre_gid=options.synaptics.pre_synaptic_gid,
            post_gid=options.morphology.gid,
            options=options,
            inverse_transformation=post_synaptic_transformation.inverted())

        # Synapses count
        context.scene.NMV_SynapticsNumberSharedSynapses = len(shared_synapses_ids)

    elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:

        # Ensure that the given post-synaptic GID is an integer
        try:
            int(options.synaptics.post_synaptic_gid)
        except ValueError:
            operator.report({'ERROR'}, 'Please enter a valid GID as an integer')
            return {'FINISHED'}

        # Ensure that the pre-synaptic and post-synaptic GIDs are not the same
        if int(options.synaptics.post_synaptic_gid) == int(options.morphology.gid):
            operator.report({'ERROR'}, 'Please enter a valid post-synaptic GID, that is different '
                                       'from the pre-synaptic one')
            return {'FINISHED'}

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            operator.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
                            % (str(options.morphology.gid),
                               str(options.synaptics.post_synaptic_gid)))
            return {'FINISHED'}

        nmv.scene.clear_scene()

        # Create the pre-synaptic neuron AT ORIGIN - THIS IS THE FOCUS
        pre_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Create the post-synaptic neuron AT ORIGIN
        post_synaptic_neuron_mesh = nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.synaptics.post_synaptic_gid, options=options)

        # Get the transformations of the pre- and post-synaptic neurons
        pre_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.morphology.gid)
        post_synaptic_transformation = circuit.get_neuron_transformation_matrix(
            gid=options.synaptics.post_synaptic_gid)

        # Since the focus is given to the pre-synaptic neuron; it is the originally loaded one,
        # transform the post-synaptic neuron w.r.t to the pre synaptic one
        post_synaptic_neuron_mesh.matrix_world = post_synaptic_transformation
        post_synaptic_neuron_mesh.matrix_world = \
            pre_synaptic_transformation.inverted() @ post_synaptic_neuron_mesh.matrix_world

        nmv.bbp.visualize_shared_synapses_between_two_neurons(
            circuit=circuit,
            pre_gid=nmv.interface.ui.globals.options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid,
            options=options,
            inverse_transformation=pre_synaptic_transformation.inverted())

        # Synapses count
        context.scene.NMV_SynapticsNumberSharedSynapses = len(shared_synapses_ids)

    # Done
    return {'FINISHED'}
