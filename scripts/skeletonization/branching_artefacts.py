####################################################################################################
# Copyright (c) 2020 - 2024, EPFL / Blue Brain Project
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
import copy

import nmv.mesh
import nmv.consts
import nmv.shading
import nmv.scene
import nmv.geometry
from mathutils import Vector


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def import_center_lines_and_draw(file_path,
                                 radius=0.1,
                                 color=nmv.consts.Color.BLACK):

    # Create a list of center-lines
    edges = list()
    polylines_data = list()

    f = open(file_path, 'r')
    branch_index = 0
    for i, line in enumerate(f):
        if 'start' in line:
            edges.clear()
            line = line.strip('\n')
            line = line.split(' ')
            branch_index = int(line[1])
            continue
        elif 'end' in line:
            polylines_data.append(copy.deepcopy(edges))
            continue
        else:
            line = line.strip('\n')
            line = line.split(' ')
            p = Vector((float(line[0]), float(line[1]), float(line[2]), 1))
            edges.append([p, radius])
    f.close()

    # Draw the polylines of the center-line edges
    bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, resolution=1, name='Bevel')
    polylines = nmv.geometry.draw_poly_lines_as_single_object(
        polylines_data, bevel_object=bevel_object)

    # Create the center-lines edges mesh
    center_lines_mesh = nmv.scene.convert_object_to_mesh(scene_object=polylines)
    center_lines_mesh.name = 'Center-lines'

    # Assign the material
    material = nmv.shading.create_flat_material(name='Center-lines Material', color=color)
    nmv.shading.set_material_to_object(center_lines_mesh, material)

    # Return the resul
    return center_lines_mesh


