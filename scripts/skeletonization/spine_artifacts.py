####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Blender improts
from mathutils import Vector

# Internal imports
import nmv.bmeshi
import nmv.consts
import nmv.shading


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def import_spines_terminals(file_path):

    spines_terminals = list()
    f = open(file_path, 'r')
    for line in f:
        data = line.strip('\n').split(' ')
        spines_terminals.append(Vector((float(data[0]), float(data[1]), float(data[2]))))
    f.close()
    return spines_terminals


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def draw_spines_terminals(spines_terminals,
                          radius=0.1):

    # Construct terminal spheres
    terminals_spheres = list()
    for spines_terminal in spines_terminals:
        terminal_sphere = nmv.bmeshi.create_ico_sphere(
            radius=radius, location=spines_terminal, subdivisions=2)
        terminals_spheres.append(terminal_sphere)

    # Join into a single bmesh
    terminals_bmesh = nmv.bmeshi.join_bmeshes_list(terminals_spheres)

    # Convert it to a mesh and return it
    return nmv.bmeshi.convert_bmesh_to_mesh(terminals_bmesh, name='Spine Terminals')


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def import_and_draw_spines_terminals(file_path,
                                     radius=0.1,
                                     color=nmv.consts.Color.BLACK):

    # Import
    spines_terminals = import_spines_terminals(file_path=file_path)

    # Draw
    terminals_mesh_object = draw_spines_terminals(spines_terminals=spines_terminals, radius=radius)

    # Create the material and assign it
    material = nmv.shading.create_flat_material(name='Spines Material', color=color)
    nmv.shading.set_material_to_object(
        mesh_object=terminals_mesh_object, material_reference=material)

    # Return the resulting mesh object
    return terminals_mesh_object