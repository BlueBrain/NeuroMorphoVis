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
        color, material_type=nmv.enums.Shader.LAMBERT_WARD,
        unified_radius=True, branch_radius=1.0,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER):
    """Creates a neuron mesh, specified by a GID in a given circuit.
    NOTE: The soma is located at the origin.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param color:
        Neuron RGB color in a Vector.
    :param material_type:
        The type of the material to be applied to the mesh.
    :param unified_radius:
        If this flag is set to true, the neuron will have unified radius across it all branches.
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

    # Get the path of the morphology from the circuit
    morphology_path = circuit.morph.get_filepath(int(gid))

    # Read the morphology and get its NMV object, and ensure that it is centered at the origin
    morphology = nmv.file.read_morphology_with_morphio(
        morphology_file_path=morphology_path, center_at_origin=True)

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

    # Materials
    nmv_options.shading.mesh_material = material_type

    # Soma
    nmv_options.mesh.soma_type = nmv.enums.Soma.Representation.META_BALLS

    # Create a meta balls meshing builder
    mesh_builder = nmv.builders.PiecewiseBuilder(morphology=morphology, options=nmv_options)

    # Create the neuron mesh
    neuron_mesh = mesh_builder.reconstruct_mesh_in_single_object()

    # Add the material top the reconstructed mesh
    neuron_material = nmv.shading.create_material(
        name='neuron_%s' % morphology.label, color=color, material_type=material_type)
    nmv.shading.set_material_to_object(mesh_object=neuron_mesh, material_reference=neuron_material)

    # Return a reference to the neuron mesh
    return neuron_mesh


####################################################################################################
# @create_symbolic_neuron_mesh_in_circuit
####################################################################################################
def create_symbolic_neuron_mesh_in_circuit(
        circuit, gid,
        color, material_type=nmv.enums.Shader.LAMBERT_WARD,
        branch_radius=1.0,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER):
    """Creates a symbolic mesh of a neuron, specified by a GID in a given circuit.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param color:
        Neuron RGB color in a Vector.
    :param material_type:
        The type of the material to be applied to the mesh.
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
        circuit=circuit, gid=gid, color=color, material_type=material_type,
        unified_radius=True, branch_radius=branch_radius,
        basal_branching_order=basal_branching_order,
        apical_branching_order=apical_branching_order,
        axon_branching_order=axon_branching_order)


####################################################################################################
# @create_to_scale_neuron_mesh_in_circuit
####################################################################################################
def create_to_scale_neuron_mesh_in_circuit(
        circuit, gid,
        color, material_type=nmv.enums.Shader.LAMBERT_WARD,
        basal_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        apical_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER,
        axon_branching_order=nmv.consts.Skeleton.MAX_BRANCHING_ORDER):
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
        circuit=circuit, gid=gid, color=color, material_type=material_type, unified_radius=False,
        basal_branching_order=basal_branching_order,
        apical_branching_order=apical_branching_order,
        axon_branching_order=axon_branching_order)
