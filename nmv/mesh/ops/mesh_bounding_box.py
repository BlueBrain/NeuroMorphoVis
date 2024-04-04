####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.mesh
import nmv.shading


####################################################################################################
# @draw_bounding_box_of_mesh
####################################################################################################
def draw_bounding_box_of_mesh(mesh_object,
                              edge_gap_percentage=0.0):
    """Draws a bounding box around a given mesh object. Note that the drawn bounding box will not
    be shown in any rendering. It is just created to highlight certain objects in the view port to
    debug and analyze a given mesh object.

    :param mesh_object:
        A given mesh object.
    :param edge_gap_percentage:
        A slight gap between the edges of the mesh and the drawn bounding box. By default, Zero.
        Note that this is calculated based on the dimensions of the bounding box.
    :return:
        A reference the created bounding box mesh.
    """

    # Ensure that it is a mesh
    if mesh_object.type == 'MESH':

        # Get object's bounding box dimensions
        bbox = [mesh_object.matrix_world @ Vector(corner) for corner in mesh_object.bound_box]
        min_x = min(bbox, key=lambda x: x[0])[0]
        max_x = max(bbox, key=lambda x: x[0])[0]
        dx = max_x - min_x
        min_y = min(bbox, key=lambda x: x[1])[1]
        max_y = max(bbox, key=lambda x: x[1])[1]
        dy = max_y - min_y
        min_z = min(bbox, key=lambda x: x[2])[2]
        max_z = max(bbox, key=lambda x: x[2])[2]
        dz = max_z - min_z

        # Update the edge gap
        min_x -= dx * edge_gap_percentage
        max_x += dx * edge_gap_percentage
        min_y -= dy * edge_gap_percentage
        max_y += dy * edge_gap_percentage
        min_z -= dz * edge_gap_percentage
        max_z += dz * edge_gap_percentage

        # Create bounding box vertices
        vertices = [(min_x, min_y, min_z), (max_x, min_y, min_z),
                    (max_x, max_y, min_z), (min_x, max_y, min_z),
                    (min_x, min_y, max_z), (max_x, min_y, max_z),
                    (max_x, max_y, max_z), (min_x, max_y, max_z)]

        # Define edges for the bounding box
        edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]

        # Create mesh and object for the bounding box
        bbox_mesh = bpy.data.meshes.new(name="Bounding Box [%s]" % mesh_object.name)
        bbox_mesh.from_pydata(vertices, edges, [])

        # Link the bounding box mesh to the scene
        bbox_mesh_object = bpy.data.objects.new("Bounding Box [%s]" % mesh_object.name, bbox_mesh)
        bpy.context.collection.objects.link(bbox_mesh_object)
        bpy.context.view_layer.objects.active = bbox_mesh_object
    else:
        print('The object [%s] is NOT a mesh object!' % mesh_object.name)


####################################################################################################
# @draw_bounding_box_of_mesh
####################################################################################################
def draw_solid_bounding_box_of_mesh(mesh_object,
                                    edge_gap_percentage=0.0,
                                    apply_solidification=True,
                                    thickness=0.05):

    # Get object's bounding box dimensions
    bbox = [mesh_object.matrix_world @ Vector(corner) for corner in mesh_object.bound_box]
    min_x = min(bbox, key=lambda x: x[0])[0]
    max_x = max(bbox, key=lambda x: x[0])[0]
    dx = max_x - min_x
    min_y = min(bbox, key=lambda x: x[1])[1]
    max_y = max(bbox, key=lambda x: x[1])[1]
    dy = max_y - min_y
    min_z = min(bbox, key=lambda x: x[2])[2]
    max_z = max(bbox, key=lambda x: x[2])[2]
    dz = max_z - min_z

    # Update the edge gap
    min_x -= dx * edge_gap_percentage
    max_x += dx * edge_gap_percentage
    min_y -= dy * edge_gap_percentage
    max_y += dy * edge_gap_percentage
    min_z -= dz * edge_gap_percentage
    max_z += dz * edge_gap_percentage

    # Create bounding box vertices
    vertices = [(min_x, min_y, min_z), (max_x, min_y, min_z),
                (max_x, max_y, min_z), (min_x, max_y, min_z),
                (min_x, min_y, max_z), (max_x, min_y, max_z),
                (max_x, max_y, max_z), (min_x, max_y, max_z)]

    # Define faces for the bounding box
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

    # Create mesh and object for the bounding box
    bbox_mesh = bpy.data.meshes.new(name="Bounding Box [%s]" % mesh_object.name)
    bbox_mesh.from_pydata(vertices, [], faces)

    # Link the bounding box mesh to the scene
    bbox_mesh_object = bpy.data.objects.new("Bounding Box [%s]" % mesh_object.name, bbox_mesh)
    bpy.context.collection.objects.link(bbox_mesh_object)
    bpy.context.view_layer.objects.active = bbox_mesh_object

    # Apply the "Solidify" modifier to give thickness to the bounding box
    if apply_solidification:
        wireframe_modifier = bbox_mesh_object.modifiers.new(name="Wireframe", type='WIREFRAME')
        wireframe_modifier.thickness = thickness
        bpy.ops.object.modifier_apply(modifier="Wireframe")

    # Return a reference to the created bounding box
    return bbox_mesh_object


####################################################################################################
# @draw_wireframe_bounding_boxes_from_solid_ones
####################################################################################################
def draw_wireframe_bounding_boxes_mesh_from_solid_ones(solid_bounding_boxes,
                                                       name='Bounding Boxes',
                                                       wireframe_thickness=0.1,
                                                       material=None):
    """Draws wireframe (with thickness) bounding boxes from solid ones to highlight the objects
    of interest. This applies a WIREFRAME modifier to the solid bounding boxes. Note that the
    resulting mesh is simply an aggregate of all the bounding boxes to facilitate using it in
    the scene.

    :param solid_bounding_boxes:
        A list of the solid bounding boxes.
    :param name:
        The name of the created bounding boxes mesh.
    :param wireframe_thickness:
        The thickness of the wireframe. By default, 0.1.
    :param material:
        A given material to color the bounding box. If this is None, the resulting bounding
        boxes mesh will be gray (the default material color in Blender).
    :return:
        A reference to the created bounding boxes mesh.
    """

    if len(solid_bounding_boxes) == 0:
        return None

    # Make a joint mesh
    joint_bounding_boxes_mesh = nmv.mesh.join_mesh_objects(mesh_list=solid_bounding_boxes,
                                                           name=name)

    # Apply the Wireframe modifier
    wireframe_modifier = joint_bounding_boxes_mesh.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe_modifier.thickness = wireframe_thickness
    bpy.ops.object.modifier_apply(modifier="Wireframe")

    # Apply the material
    if material is not None:
        nmv.shading.set_material_to_object(mesh_object=joint_bounding_boxes_mesh,
                                           material_reference=material)

    # Return a reference to the created bounding box
    return joint_bounding_boxes_mesh
