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

# Blender imports
import bpy

# Internal imports
import nmv.bbp
import nmv.enums
import nmv.interface
import nmv.utilities
import nmv.scene


####################################################################################################
# @NMV_ReconstructSynaptics
####################################################################################################
class NMV_ReconstructSynaptics(bpy.types.Operator):
    """Reconstruct the synaptics scene"""

    # Operator parameters
    bl_idname = "nmv.reconstruct_synaptics"
    bl_label = "Reconstruct Synaptics"

    ################################################################################################
    # @reconstruct_afferent
    ################################################################################################
    def reconstruct_afferent(self, context, circuit, options):

        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_afferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options, context=context)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        afferent_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberAfferentSynapses = afferent_synapses_count

    ################################################################################################
    # @reconstruct_efferent
    ################################################################################################
    def reconstruct_efferent(self, context, circuit, options):

        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_efferent_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options, context=context)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        efferent_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberEfferentSynapses = efferent_synapses_count

    ################################################################################################
    # @reconstruct_afferent_and_afferent
    ################################################################################################
    def reconstruct_afferent_and_afferent(self, context, circuit, options):

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

    ################################################################################################
    # @reconstruct_excitatory
    ################################################################################################
    def reconstruct_excitatory(self, context, circuit, options):

        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=options.morphology.gid, options=options,
            visualize_excitatory=True, visualize_inhibitory=False)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        excitatory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberExcitatorySynapses = excitatory_synapses_count

    ################################################################################################
    # @reconstruct_inhibitory
    ################################################################################################
    def reconstruct_inhibitory(self, context, circuit, options):

        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
            visualize_excitatory=False, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        inhibitory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberInhibitorySynapses = inhibitory_synapses_count

    ################################################################################################
    # @reconstruct_excitatory_and_inhibitory
    ################################################################################################
    def reconstruct_excitatory_and_inhibitory(self, context, circuit, options):

        nmv.scene.clear_scene()
        synapse_groups = nmv.bbp.visualize_excitatory_and_inhibitory_synapses(
            circuit=circuit, gid=nmv.interface.ui_options.morphology.gid,
            visualize_excitatory=True, visualize_inhibitory=True, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

        # Synapses count
        excitatory_synapses_count = len(synapse_groups[0].synapses_ids_list)
        context.scene.NMV_SynapticsNumberExcitatorySynapses = excitatory_synapses_count
        inhibitory_synapses_count = len(synapse_groups[1].synapses_ids_list)
        context.scene.NMV_SynapticsNumberInhibitorySynapses = inhibitory_synapses_count

    ################################################################################################
    # @reconstruct_pathway_pre_synaptic
    ################################################################################################
    def reconstruct_pathway_pre_synaptic(self, context, circuit, options):

        # Ensure that the given pre-synaptic GID is an integer
        try:
            int(options.synaptics.pre_synaptic_gid)
        except ValueError:
            self.report({'ERROR'}, 'Please enter a valid GID as an integer')
            return {'FINISHED'}

        # Ensure that the pre-synaptic and post-synaptic GIDs are not the same
        if int(options.synaptics.pre_synaptic_gid) == int(options.morphology.gid):
            self.report({'ERROR'}, 'Please enter a valid pre-synaptic GID, that is different '
                                       'from the post-synaptic one')
            return {'FINISHED'}

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.synaptics.pre_synaptic_gid,
            post_gid=options.morphology.gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            self.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
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

    ################################################################################################
    # @reconstruct_pathway_post_synaptic
    ################################################################################################
    def reconstruct_pathway_post_synaptic(self, context, circuit, options):

        # Ensure that the given post-synaptic GID is an integer
        try:
            int(options.synaptics.post_synaptic_gid)
        except ValueError:
            self.report({'ERROR'}, 'Please enter a valid GID as an integer')
            return {'FINISHED'}

        # Ensure that the pre-synaptic and post-synaptic GIDs are not the same
        if int(options.synaptics.post_synaptic_gid) == int(options.morphology.gid):
            self.report({'ERROR'}, 'Please enter a valid post-synaptic GID, that is different '
                                       'from the pre-synaptic one')
            return {'FINISHED'}

        # Initially, try to get a list of synapses shared between the two cells
        shared_synapses_ids = circuit.get_shared_synapses_ids_between_two_neurons(
            pre_gid=options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid)

        # If that list is Zero, then report the error and exit
        if len(shared_synapses_ids) == 0:
            self.report({'ERROR'}, 'No shared synapses between the given neurons [%s - %s]'
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
            pre_gid=nmv.interface.ui_options.morphology.gid,
            post_gid=options.synaptics.post_synaptic_gid,
            options=options,
            inverse_transformation=pre_synaptic_transformation.inverted())

        # Synapses count
        context.scene.NMV_SynapticsNumberSharedSynapses = len(shared_synapses_ids)

    ################################################################################################
    # @reconstruct_projection
    ################################################################################################
    def reconstruct_projection(self, context, circuit, options):

        pass

    ################################################################################################
    # @reconstruct_projection
    ################################################################################################
    def reconstruct_targets(self, context, circuit, options):

        # If the given synaptics file is not valid, handle the error
        if not os.path.isfile(options.synaptics.synaptics_json_file):
            self.report({'ERROR'}, 'The given synaptics file does not exist.')
            return {'FINISHED'}

        # Try to load the synaptics file
        try:
            options.synaptics.customized_synaptics_group = \
                nmv.bbp.get_synapse_groups_from_color_coded_json_file(
                    synapse_json_file=options.synaptics.synaptics_json_file)
        except IOError:
            self.report({'ERROR'}, 'Cannot load the given synaptics file. FORMAT ERROR!')
            return {'FINISHED'}

        # If the number of synapse groups is less than 1 report the issue
        if len(options.synaptics.customized_synaptics_group) < 1:
            self.report({'ERROR'}, 'The file has no groups')
            return {'FINISHED'}

        # If we reach that point, the file has been successfully loaded
        nmv.interface.ui_synaptics_file_loaded = True

        # Create the info (colors and stats.) of the drawn synapses
        for i, group in enumerate(options.synaptics.customized_synaptics_group):
            setattr(bpy.types.Scene, 'NMV_CustomizedColor%d' % i,
                    bpy.props.FloatVectorProperty(
                        name=group.name, subtype='COLOR', default=group.color, min=0.0, max=1.0,
                        description='The color of the synapses of the %s group' % group.name))

            synapse_count = len(group.synapses_ids_list)
            setattr(bpy.types.Scene, 'NMV_CustomizedCount%d' % i,
                    bpy.props.IntProperty(
                        name="Count", default=synapse_count, min=synapse_count, max=synapse_count,
                        description="The number of the synapses of the %s group" % group.name,))

        # Visualize the synapses and the neuron
        nmv.scene.clear_scene()
        nmv.bbp.visualize_synapse_groups(
            circuit=circuit, synapse_groups=options.synaptics.customized_synaptics_group,
            gid=options.morphology.gid, options=options)
        nmv.bbp.visualize_circuit_neuron_for_synaptics(
            circuit=circuit, gid=options.morphology.gid, options=options)

    ################################################################################################
    # @reconstruct_synaptics
    ################################################################################################
    def reconstruct_synaptics(self, context, circuit, options):

        # Afferent synapses only (on dendrites)
        if options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT:
            self.reconstruct_afferent(context=context, circuit=circuit, options=options)

        # Efferent synapses (on axon)
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EFFERENT:
            self.reconstruct_efferent(context=context, circuit=circuit, options=options)

        # Afferent and efferent synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.AFFERENT_AND_EFFERENT:
            self.reconstruct_afferent_and_efferent(
                context=context, circuit=circuit, options=options)

        # Excitatory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY:
            self.reconstruct_excitatory(context=context, circuit=circuit, options=options)

        # Inhibitory synapses only
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.INHIBITORY:
            self.reconstruct_inhibitory(context=context, circuit=circuit, options=options)

        # Excitatory and inhibitory synapses
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.EXCITATORY_AND_INHIBITORY:
            self.reconstruct_excitatory_and_inhibitory(
                context=context, circuit=circuit, options=options)

        # Pre-synaptic pathways
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_PRE_SYNAPTIC:
            self.reconstruct_pathway_pre_synaptic(
                context=context, circuit=circuit, options=options)

        # Post-synaptic pathways
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PATHWAY_POST_SYNAPTIC:
            self.reconstruct_pathway_post_synaptic(
                context=context, circuit=circuit, options=options)

        # Projection
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.PROJECTION:
            self.reconstruct_projection(
                context=context, circuit=circuit, options=options)

        # Targets
        elif options.synaptics.use_case == nmv.enums.Synaptics.UseCase.TARGETS:
            self.reconstruct_targets(
                context=context, circuit=circuit, options=options)

        else:
            self.report({'ERROR'}, 'Please select a valid option')
            nmv.logger.log('UI_ERROR: NMV_ReconstructSynaptics::reconstruct_synaptics')

        return {'FINISHED'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        return self.reconstruct_synaptics(
            context=context, circuit=nmv.interface.ui_circuit, options=nmv.interface.ui_options)
