####################################################################################################
# Copyright (c) 2024, EPFL / Blue Brain Project
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

# Internal imports
import nmv.mesh
import nmv.consts
import nmv.shading


####################################################################################################
# @draw_wireframe_meshes_bounding_boxes
####################################################################################################
def draw_wireframe_meshes_bounding_boxes(meshes_list,
                                         wireframe_thickness=0.1,
                                         color=nmv.consts.Color.RED):

    # Create a list of solid bounding boxes
    bounding_boxes = list()
    for i, mesh_object in enumerate(meshes_list):
        bounding_box = nmv.mesh.draw_solid_bounding_box_of_mesh(
            mesh_object=mesh_object, edge_gap_percentage=0.0, apply_solidification=False)
        bounding_boxes.append(bounding_box)

    # Create and assign the material to the bounding boxes mesh
    material = nmv.shading.create_flat_material(name='Partitions BB Material', color=color)

    # Create a wireframe bounding box mesh and assign the color to it
    mesh_bounding_box = nmv.mesh.draw_wireframe_bounding_boxes_mesh_from_solid_ones(
        solid_bounding_boxes=bounding_boxes, name='Bounding Boxes',
        wireframe_thickness=wireframe_thickness, material=material)

    # Return a reference to the mesh bounding box
    return mesh_bounding_box

