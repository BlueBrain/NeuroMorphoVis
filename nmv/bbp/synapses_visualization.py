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
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.utilities


####################################################################################################
# @visualize_synapses_on_neuron
####################################################################################################
def visualize_synapses_on_neuron(circuit_config,
                                 gid,
                                 color_coded_synapses_dict,
                                 synapse_radius,
                                 soma_color=nmv.enums.Color.SOMA,
                                 basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
                                 apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
                                 axons_color=nmv.enums.Color.AXONS,
                                 material_type=nmv.enums.Shader.LAMBERT_WARD,
                                 unify_branch_radii=False,
                                 unified_branch_radius=1.0,
                                 basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
                                 apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
                                 axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER):

    # BBP imports
    from bluepy import Circuit

    # Read the circuit
    circuit = Circuit(circuit_config)

    # Create the neuron mesh
    if unify_branch_radii:
        neuron_mesh = nmv.bbp.create_symbolic_neuron_mesh_in_circuit(
            circuit=circuit, gid=gid,
            branch_radius=unified_branch_radius,
            basal_branching_order=basal_branching_order,
            apical_branching_order=apical_branching_order,
            axon_branching_order=axon_branching_order,
            soma_color=soma_color,
            basal_dendrites_color=basal_dendrites_color,
            apical_dendrites_color=apical_dendrites_color,
            axons_color=axons_color,
            material_type=material_type)
    else:
        neuron_mesh = nmv.bbp.create_to_scale_neuron_mesh_in_circuit(
            circuit=circuit, gid=gid,
            basal_branching_order=basal_branching_order,
            apical_branching_order=apical_branching_order,
            axon_branching_order=axon_branching_order,
            soma_color=soma_color,
            basal_dendrites_color=basal_dendrites_color,
            apical_dendrites_color=apical_dendrites_color,
            axons_color=axons_color,
            material_type=material_type)
    neuron_mesh.name = 'Neuron %s' % str(gid)

    # Create the synapses mesh
    transformation = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit, gid=int(gid))
    synapses_mesh = nmv.bbp.create_color_coded_synapses_mesh(
        circuit=circuit, color_coded_synapses_dict=color_coded_synapses_dict,
        synapse_radius=synapse_radius,
        inverted_transformation=transformation.inverted(),
        material_type=material_type)
    synapses_mesh.name = 'Neuron %s Synapses' % str(gid)

    # Return a list of meshes that has references to the meshes of the neuron and the synapses
    return [neuron_mesh, synapses_mesh]


####################################################################################################
# @visualize_efferent_synapses_on_pre_synaptic_neuron
####################################################################################################
def visualize_efferent_synapses_on_pre_synaptic_neuron(
        circuit_config,
        gid,
        color_coded_synapses_dict,
        synapse_radius,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        material_type=nmv.enums.Shader.LAMBERT_WARD,
        unify_branch_radii=False,
        unified_branch_radius=1.0,
        dendrites_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER):

    return visualize_synapses_on_neuron(
        circuit_config=circuit_config, gid=gid,
        color_coded_synapses_dict=color_coded_synapses_dict, synapse_radius=synapse_radius,
        unify_branch_radii=unify_branch_radii, unified_branch_radius=unified_branch_radius,
        basal_branching_order=dendrites_branching_order,
        apical_branching_order=dendrites_branching_order,
        soma_color=soma_color,
        basal_dendrites_color=basal_dendrites_color,
        apical_dendrites_color=apical_dendrites_color,
        axons_color=axons_color,
        material_type=material_type
    )


####################################################################################################
# @visualize_afferent_synapses_on_post_synaptic_neuron
####################################################################################################
def visualize_afferent_synapses_on_post_synaptic_neuron(
        circuit_config,
        gid,
        color_coded_synapses_dict,
        synapse_radius,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        material_type=nmv.enums.Shader.LAMBERT_WARD,
        unify_branch_radii=False,
        unified_branch_radius=1.0,
        axon_branching_order=1):

    return visualize_synapses_on_neuron(
        circuit_config=circuit_config, gid=gid,
        color_coded_synapses_dict=color_coded_synapses_dict, synapse_radius=synapse_radius,
        unify_branch_radii=unify_branch_radii, unified_branch_radius=unified_branch_radius,
        axon_branching_order=axon_branching_order,
        soma_color=soma_color,
        basal_dendrites_color=basal_dendrites_color,
        apical_dendrites_color=apical_dendrites_color,
        axons_color=axons_color,
        material_type=material_type)


####################################################################################################
# @visualize_excitatory_inhibitory_synapses_on_neuron
####################################################################################################
def visualize_excitatory_inhibitory_synapses_on_neuron(
        circuit_config,
        gid,
        synapse_radius,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        excitatory_synapses_color=nmv.consts.Color.RED,
        inhibitory_synapses_color=nmv.consts.Color.BLUE,
        material_type=nmv.enums.Shader.LAMBERT_WARD,
        unify_branch_radii=False,
        unified_branch_radius=1.0):

    # BBP imports
    from bluepy import Circuit

    # Read the circuit and get a color-coded dictionary of the excitatory and inhibitory synapses
    circuit = Circuit(circuit_config)
    color_coded_synapses_dict = nmv.bbp.get_excitatory_and_inhibitory_synapses_color_coded_dict(
        circuit=circuit, gid=int(gid),
        exc_color=excitatory_synapses_color, inh_color=inhibitory_synapses_color)

    return visualize_synapses_on_neuron(
        circuit_config=circuit_config, gid=gid,
        color_coded_synapses_dict=color_coded_synapses_dict, synapse_radius=synapse_radius,
        unify_branch_radii=unify_branch_radii, unified_branch_radius=unified_branch_radius,
        soma_color=soma_color,
        basal_dendrites_color=basal_dendrites_color,
        apical_dendrites_color=apical_dendrites_color,
        axons_color=axons_color,
        material_type=material_type
    )



def visualize_synapses_on_post_synaptic_neuron_based_on_pre_mtypes():
    pass


def visualize_synapses_on_pre_synaptic_neuron_based_on_post_mtypes():
    pass


def visualize_synapses_on_post_synaptic_neuron_based_on_pre_etypes():
    pass


def visualize_synapses_on_pre_synaptic_neuron_based_on_post_etypes():
    pass
