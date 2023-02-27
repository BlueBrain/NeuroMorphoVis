####################################################################################################
# Copyright (c) 2020 - 2023, EPFL / Blue Brain Project
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
import random
import os
import sys

# Internal imports
import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), import_path)))

import circuit_data

# BBP imports
import bluepy
from bluepy import Circuit

# Blender
from mathutils import Vector, Matrix

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.geometry
import nmv.options
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.shading
import nmv.utilities


####################################################################################################
# @create_neuron_mesh
####################################################################################################
def create_neuron_mesh(circuit,
                       gid,
                       color,
                       material_type=nmv.enums.Shader.LAMBERT_WARD):
    """Creates the mesh of the neuron.

    :param circuit:
        BBP circuit.
    :param gid:
        Neuron GID.
    :param neuron_material:
        The color of the neuron in a RGB Vector((R, G, B)) format
    :return:
        A reference to the created neuron mesh.
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
    nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
    nmv_options.morphology.samples_unified_radii_value = 1.0
    nmv_options.morphology.axon_branch_order = 1e5
    nmv_options.shading.mesh_material = material_type
    nmv_options.mesh.soma_type = nmv.enums.Soma.Representation.META_BALLS

    # Create a meta balls meshing builder
    mesh_builder = nmv.builders.PiecewiseBuilder(morphology=morphology, options=nmv_options)

    # Create the neuron mesh
    neuron_mesh = mesh_builder.reconstruct_mesh_in_single_object()

    # Smooth the mesh to make it look nice
    # nmv.mesh.smooth_object(mesh_object=neuron_mesh, level=1)

    # Add the material top the reconstructed mesh
    neuron_material = nmv.shading.create_material(
        name='neuron_%s' % str(gid), color=color, material_type=material_type)
    nmv.shading.set_material_to_object(mesh_object=neuron_mesh, material_reference=neuron_material)

    # Return a reference to the neuron mesh
    return neuron_mesh
