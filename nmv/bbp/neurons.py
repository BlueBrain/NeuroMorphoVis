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

# Internal import
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.options
import nmv.mesh
import nmv.shading


####################################################################################################
# @create_neuron_mesh_in_circuit
####################################################################################################
def create_neuron_mesh_in_circuit(
        circuit, gid,
        unified_radius=True, branch_radius=1.0,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        material_type=nmv.enums.Shader.LAMBERT_WARD):

    # Get the path of the morphology from the circuit
    morphology_path = circuit.get_neuron_morphology_path(gid=int(gid))

    # Read the morphology and get its NMV object, and ensure that it is centered at the origin
    morphology = nmv.file.read_morphology_with_morphio(
        morphology_file_path=morphology_path,
        morphology_format=nmv.file.get_morphology_file_format(morphology_file_path=morphology_path),
        center_at_origin=True)

    # Adjust the label to be set according to the GID not the morphology label
    morphology.label = str(gid)

    # Create default NMV options with fixed radius value for the visualization
    nmv_options = nmv.options.NeuroMorphoVisOptions()

    # Radii
    if unified_radius:
        nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
        nmv_options.morphology.samples_unified_radii_value = branch_radius

    # Branching orders
    nmv_options.morphology.basal_dendrites_branch_order = basal_branching_order
    nmv_options.morphology.apical_dendrite_branch_order = apical_branching_order
    nmv_options.morphology.axon_branch_order = axon_branching_order

    # Morphology colors and materials
    nmv_options.shading.morphology_soma_color = soma_color
    nmv_options.shading.morphology_basal_dendrites_color = basal_dendrites_color
    nmv_options.shading.morphology_apical_dendrites_color = apical_dendrites_color
    nmv_options.shading.morphology_axons_color = axons_color
    nmv_options.shading.morphology_material = material_type

    # Mesh colors and materials
    nmv_options.shading.mesh_soma_color = soma_color
    nmv_options.shading.mesh_basal_dendrites_color = basal_dendrites_color
    nmv_options.shading.mesh_apical_dendrites_color = apical_dendrites_color
    nmv_options.shading.mesh_axons_color = axons_color
    nmv_options.shading.mesh_material = material_type

    # Soma
    nmv_options.mesh.soma_type = nmv.enums.Soma.Representation.META_BALLS

    mesh_builder = nmv.builders.PiecewiseBuilder(morphology=morphology,
                                                 options=nmv_options)
    neuron_meshes = mesh_builder.reconstruct_mesh()

    # Join all the mesh objects into a single mesh object to represent the neuron
    neuron_mesh = nmv.mesh.join_mesh_objects(mesh_list=neuron_meshes, name='Neuron')

    # Return a reference to the neuron mesh
    return neuron_mesh


####################################################################################################
# @visualize_circuit_neuron_for_synaptics
####################################################################################################
def visualize_circuit_neuron_for_synaptics(circuit,
                                           gid,
                                           options,
                                           which_neuron=nmv.enums.Synaptics.WhichNeuron.INDIVIDUAL):

    # Adjust the branching order of the dendrites and axons
    dendrites_branching_order = 0
    axons_branching_order = 0

    # Adjust the coloring parameters based on the neuron order (pre- or post-synaptic neuron)
    if which_neuron == nmv.enums.Synaptics.WhichNeuron.PRE_SYNAPTIC:
        soma_color = options.synaptics.pre_synaptic_dendrites_color
        dendrites_color = options.synaptics.pre_synaptic_dendrites_color
        axons_color = options.synaptics.pre_synaptic_axons_color

        if options.synaptics.display_pre_synaptic_dendrites:
            dendrites_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
        if options.synaptics.display_pre_synaptic_axons:
            axons_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

    elif which_neuron == nmv.enums.Synaptics.WhichNeuron.POST_SYNAPTIC:
        soma_color = options.synaptics.post_synaptic_dendrites_color
        dendrites_color = options.synaptics.post_synaptic_dendrites_color
        axons_color = options.synaptics.post_synaptic_axons_color

        if options.synaptics.display_post_synaptic_dendrites:
            dendrites_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
        if options.synaptics.display_post_synaptic_axons:
            axons_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
    else:
        soma_color = options.synaptics.dendrites_color
        dendrites_color = options.synaptics.dendrites_color
        axons_color = options.synaptics.axons_color

        if options.synaptics.display_dendrites:
            dendrites_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER
        if options.synaptics.display_axons:
            axons_branching_order = nmv.consts.Skeleton.MAX_BRANCHING_ORDER

    # If we ignore both, then return None
    if dendrites_branching_order == 0 and axons_branching_order == 0:
        return None

    # Create the mesh and return a reference to it
    return create_neuron_mesh_in_circuit(circuit=circuit, gid=gid,
                                         unified_radius=options.synaptics.unify_branch_radii,
                                         branch_radius=options.synaptics.unified_radius,
                                         basal_branching_order=dendrites_branching_order,
                                         apical_branching_order=dendrites_branching_order,
                                         axon_branching_order=axons_branching_order,
                                         soma_color=soma_color,
                                         basal_dendrites_color=dendrites_color,
                                         apical_dendrites_color=dendrites_color,
                                         axons_color=axons_color,
                                         material_type=options.synaptics.shader)


####################################################################################################
# @create_symbolic_neuron_mesh_in_circuit
####################################################################################################
def create_symbolic_neuron_mesh_in_circuit(
        circuit, gid,
        unified_radius=True,
        branch_radius=1.0,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        material_type=nmv.enums.Shader.LAMBERT_WARD):
    """Creates a symbolic mesh of a neuron, specified by a GID in a given circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param color:
        Neuron RGB color in a Vector.
    :param material_type:
        The type of the material to be applied to the mesh.
    :param unified_radius:
        A flag to indicate if we will set the radii of all the branches in the neuron or not.
    :param branch_radius:
        The unified radius of all the branches in the neuron.
    :param basal_branching_order:
        The maximum branching order of the basal dendrites.
    :param apical_branching_order:
        The maximum branching order of the apical dendrites.
    :param axon_branching_order:
        The maximum branching order of the axons.
    :return:
        A reference to the created mesh object.
    """

    return create_neuron_mesh_in_circuit(
        circuit=circuit, gid=gid,
        unified_radius=unified_radius, branch_radius=branch_radius,
        basal_branching_order=basal_branching_order,
        apical_branching_order=apical_branching_order,
        axon_branching_order=axon_branching_order,
        soma_color=soma_color,
        basal_dendrites_color=basal_dendrites_color,
        apical_dendrites_color=apical_dendrites_color,
        axons_color=axons_color,
        material_type=material_type)


####################################################################################################
# @create_to_scale_neuron_mesh_in_circuit
####################################################################################################
def create_to_scale_neuron_mesh_in_circuit(
        circuit, gid,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        soma_color=nmv.enums.Color.SOMA,
        basal_dendrites_color=nmv.enums.Color.BASAL_DENDRITES,
        apical_dendrites_color=nmv.enums.Color.APICAL_DENDRITES,
        axons_color=nmv.enums.Color.AXONS,
        material_type=nmv.enums.Shader.LAMBERT_WARD,):
    """Creates a to-scale mesh of a neuron, specified by a GID in a given circuit.
    The branches preserve the actual diameters as specified in the morphology.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param color:
        Neuron RGB color in a Vector.
    :param material_type:
        The type of the material to be applied to the mesh.
    :param basal_branching_order:
        The maximum branching order of the basal dendrites.
    :param apical_branching_order:
        The maximum branching order of the apical dendrites.
    :param axon_branching_order:
        The maximum branching order of the axons.
    :return:
        A reference to the created mesh object.
    """

    return create_neuron_mesh_in_circuit(
        circuit=circuit, gid=gid, unified_radius=False,
        basal_branching_order=basal_branching_order,
        apical_branching_order=apical_branching_order,
        axon_branching_order=axon_branching_order,
        soma_color=soma_color,
        basal_dendrites_color=basal_dendrites_color,
        apical_dendrites_color=apical_dendrites_color,
        axons_color=axons_color,
        material_type=material_type)


####################################################################################################
# @transform_neuron_mesh_to_global_coordinates
####################################################################################################
def transform_neuron_mesh_to_global_coordinates(circuit,
                                                gid,
                                                neuron_mesh):
    """Transforms the mesh of a specific neuron to its global coordinates in the circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID in the circuit.
    :param neuron_mesh:
        A reference to the neuron mesh.
    """

    # Get the neuron transformation matrix and update that of the mesh accordingly
    neuron_mesh.matrix_world = nmv.bbp.get_neuron_transformation_matrix(circuit=circuit, gid=gid)
