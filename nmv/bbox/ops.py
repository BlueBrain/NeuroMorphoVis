####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import math

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv
import nmv.bbox
import nmv.consts
import nmv.geometry
import nmv.mesh
import nmv.scene


####################################################################################################
# @extend_bounding_boxes
####################################################################################################
def extend_bounding_boxes(bounding_boxes_list):
    """Return the largest bounding box that is composed of smaller ones.

    :param bounding_boxes_list:
        A list of bounding boxes given to get the union of them.
    :return:
        The union bounding box of all the given bounding boxes.
    """

    # Initialize the min and max points
    p_min = Vector((nmv.consts.Math.INFINITY,
                    nmv.consts.Math.INFINITY,
                    nmv.consts.Math.INFINITY))
    p_max = Vector((-1 * nmv.consts.Math.INFINITY,
                    -1 * nmv.consts.Math.INFINITY,
                    -1 * nmv.consts.Math.INFINITY))

    for bounding_box in bounding_boxes_list:
        if bounding_box.p_min[0] < p_min[0]:
            p_min[0] = bounding_box.p_min[0]
        if bounding_box.p_min[1] < p_min[1]:
            p_min[1] = bounding_box.p_min[1]
        if bounding_box.p_min[2] < p_min[2]:
            p_min[2] = bounding_box.p_min[2]

        if bounding_box.p_max[0] > p_max[0]:
            p_max[0] = bounding_box.p_max[0]
        if bounding_box.p_max[1] > p_max[1]:
            p_max[1] = bounding_box.p_max[1]
        if bounding_box.p_max[2] > p_max[2]:
            p_max[2] = bounding_box.p_max[2]

    # Build bounding box object
    bounding_box = nmv.bbox.BoundingBox(p_min, p_max)

    # Return a reference to it
    return bounding_box


####################################################################################################
# @get_object_bounding_box
####################################################################################################
def get_object_bounding_box(scene_object):
    """Return the bounding box of a given object in the scene.

    :param scene_object:
        An object existing in the scene.
    :return:
        The bounding box of the given object.
    """

    # Get the center and the bounds of the given object from blender
    center = scene_object.location
    bounds = scene_object.dimensions

    # Build bounding box object
    bounding_box = nmv.bbox.BoundingBox(center=center, bounds=bounds)

    # Return a reference to it
    return bounding_box


####################################################################################################
# @confirm_object_bounding_box
####################################################################################################
def confirm_object_bounding_box(scene_object):
    """Return the bounding box of the given object that is already existing in the scene.

    :param scene_object:
        An object existing in the scene.
    :return:
        The bounding box of the given object.
    """

    # Compute the bounding box of the object from the vertices
    box = scene_object.bound_box

    # Compute the bounding box from the vertices of the object
    verts = list()
    verts.append((box[0][0], box[0][1], box[0][2]))
    verts.append((box[1][0], box[1][1], box[1][2]))
    verts.append((box[2][0], box[2][1], box[2][2]))
    verts.append((box[3][0], box[3][1], box[3][2]))
    verts.append((box[4][0], box[4][1], box[4][2]))
    verts.append((box[5][0], box[5][1], box[5][2]))
    verts.append((box[6][0], box[6][1], box[6][2]))
    verts.append((box[7][0], box[7][1], box[7][2]))

    # Initialize the min and max points
    p_min = Vector((10000000, 10000000, 10000000))
    p_max = Vector((-10000000, -10000000, -10000000))

    for point in range(0, len(verts)):
        if verts[point][0] < p_min[0]:
            p_min[0] = verts[point][0]
        if verts[point][1] < p_min[1]:
            p_min[1] = verts[point][1]
        if verts[point][2] < p_min[2]:
            p_min[2] = verts[point][2]
        if verts[point][0] > p_max[0]:
            p_max[0] = verts[point][0]
        if verts[point][1] > p_max[1]:
            p_max[1] = verts[point][1]
        if verts[point][2] > p_max[2]:
            p_max[2] = verts[point][2]

    # Get object location
    location = scene_object.location

    # Adjust the bounding box transform
    p_min += location
    p_max += location

    # Build bounding box object
    bounding_box = nmv.bbox.BoundingBox(p_min=p_min, p_max=p_max)

    # Return a reference to it
    return bounding_box


####################################################################################################
# @get_objects_bounding_box
####################################################################################################
def get_objects_bounding_box(objects):
    """Return the bounding box of a group of objects.

    :param objects:
        A list of objects existing in the scene.
    :return:
        The bounding box of a group of objects.
    """

    # Get a list of all the bounding boxes of the given objects in the scene
    objects_bboxes_list = list()

    for scene_object in objects:
        bbox = confirm_object_bounding_box(scene_object)
        objects_bboxes_list.append(bbox)

    # Compute the largest bounding box of all the given ones
    objects_bounding_box = extend_bounding_boxes(objects_bboxes_list)

    # Return a reference to the union bounding box
    return objects_bounding_box


####################################################################################################
# @compute_scene_bounding_box_for_curves
####################################################################################################
def compute_scene_bounding_box_for_curves():
    """Compute the bounding box of all the 'curves' in the scene.

    NOTE: This function considers only 'CURVE' type and ignores the cameras for example.

    :return:
        A reference to the bounding box of the scene.
    """

    # Select all the objects that are meshes or curves
    objects = []
    for scene_object in bpy.data.objects:
        if scene_object.type in ['CURVE']:
            objects.append(scene_object)

    # Returns the bounding box of a group of objects
    bounding_box = get_objects_bounding_box(objects)

    # Return a reference to the bounding box of the scene
    return bounding_box


####################################################################################################
# @compute_scene_bounding_box_for_meshes
####################################################################################################
def compute_scene_bounding_box_for_meshes():
    """Compute the bounding box of all the meshes in the scene.

    NOTE: This function considers only 'MESH' type and ignores the cameras for example.

    :return:
        A reference to the bounding box of the scene.
    """

    # Select all the objects that are meshes or curves
    objects = []
    for scene_object in bpy.data.objects:
        if scene_object.type in ['MESH']:
            if 'spine' in scene_object.name: continue
            objects.append(scene_object)

    # Returns the bounding box of a group of objects
    bounding_box = get_objects_bounding_box(objects)

    # Return a reference to the bounding box of the scene
    return bounding_box


####################################################################################################
# @get_scene_bounding_box
####################################################################################################
def compute_scene_bounding_box():
    """Get the bounding box of all the objects in the scene.

    NOTE: This function considers only 'MESH','CURVE' types and ignores the cameras for example.

    :return:
        A reference to the bounding box of the scene.
    """

    # Select all the objects that are meshes or curves
    objects = []
    for scene_object in bpy.data.objects:
        if scene_object.type in ['MESH', 'CURVE']:
            objects.append(scene_object)

    # Returns the bounding box of a group of objects
    bounding_box = get_objects_bounding_box(objects)

    # Return a reference to the bounding box of the scene
    return bounding_box


####################################################################################################
# @compute_unified_extent_bounding_box
####################################################################################################
def compute_unified_extent_bounding_box(extent):
    """Compute the bounding box for a given extent in microns.

    :param extent:
        The bounding box extent.
    :return:
        The bounding box.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-extent, -extent, -extent))
    p_max = Vector((extent, extent, extent))

    # Compute a symmetric bounding box that fits the given extent
    unified_bounding_box = nmv.bbox.BoundingBox(p_min=p_min, p_max=p_max)

    # Return a reference to the bounding box
    return unified_bounding_box


####################################################################################################
# @compute_unified_bounding_box
####################################################################################################
def compute_unified_bounding_box(non_unified_bounding_box):
    """Compute a unified bounding box from a non unified one, where all the dimensions are set to

    the largest dimension of the non-unified one. This bounding box will be used for rendering.

    :param non_unified_bounding_box:
        Input non-unified bounding box.
    :return:
        Unified bounding box.
    """

    # Get the largest dimension of the non-unified bounding box
    x = non_unified_bounding_box.bounds[0]
    y = non_unified_bounding_box.bounds[1]
    z = non_unified_bounding_box.bounds[2]

    largest_dimension = x
    if y > largest_dimension:
        largest_dimension = y
    if z > largest_dimension:
        largest_dimension = z

    largest_bounds = Vector((largest_dimension, largest_dimension, largest_dimension))
    unified_bounding_box = nmv.bbox.BoundingBox(center=non_unified_bounding_box.center,
                                       bounds=largest_bounds)

    return unified_bounding_box


####################################################################################################
# @compute_360_bounding_box
####################################################################################################
def compute_360_bounding_box(non_unified_bounding_box,
                             soma_center=Vector((0.0, 0.0, 0.0))):
    """Compute a specific bounding box from a non unified one, where all the XZ dimensions are set
    to the largest dimension of the two to render 360 sequences.

    NOTE: This bounding box will be used for rendering movies.

    :param non_unified_bounding_box:
        Input non-unified bounding box.
    :param soma_center:
        The center of the soma.
    :return:
        XZ origin-centred bounding box with the same Y bounds.
    """

    # Get the largest dimension of the non-unified bounding box along X and Z
    x_min_distance = soma_center[0] - non_unified_bounding_box.p_min[0]
    x_max_distance = non_unified_bounding_box.p_max[0] - soma_center[0]
    x_bounds = x_min_distance
    if x_bounds < x_max_distance:
        x_bounds = x_max_distance

    z_min_distance = soma_center[2] - non_unified_bounding_box.p_min[2]
    z_max_distance = non_unified_bounding_box.p_max[2] - soma_center[2]
    z_bounds = z_min_distance
    if z_bounds < z_max_distance:
        z_bounds = z_max_distance

    # Compute the diagonal
    diagonal = math.sqrt((x_bounds * x_bounds) + (z_bounds * z_bounds))

    # Compute p_min and p_max
    x_max = soma_center[0] + diagonal
    y_max = non_unified_bounding_box.p_max[1]
    z_max = soma_center[2] + diagonal
    x_min = soma_center[0] - diagonal
    y_min = non_unified_bounding_box.p_min[1]
    z_min = soma_center[2] - diagonal

    p_min = Vector((x_min, y_min, z_min))
    p_max = Vector((x_max, y_max, z_max))

    # Compute new the bounding box
    bounding_box = nmv.bbox.BoundingBox(p_min=p_min, p_max=p_max)

    # Return a reference to the bounding box
    return bounding_box


####################################################################################################
# @draw_scene_bounding_box
####################################################################################################
def draw_scene_bounding_box():
    """Compute the scene bounding box and draws it.

    :return:
        A reference to the bounding box of the scene.
    """

    # Compute scene bounding box
    scene_bounding_box = compute_scene_bounding_box()

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Draw a cube, rename it and then scale it to fit the bounding box
    bpy.ops.mesh.primitive_cube_add(radius=0.5, location=scene_bounding_box.center)
    bpy.context.object.scale = scene_bounding_box.bounds
    bounding_box = bpy.context.scene.objects.active
    bounding_box.name = 'scene_bounding_box'

    # Return a reference to the bounding box
    return bounding_box


####################################################################################################
# @draw_bounding_box
####################################################################################################
def draw_bounding_box(bbox,
                      name='bbox'):
    """
    Draws a given bounding box.

    :param bbox: Input bounding box.
    :param name: Bounding box name.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    p_0 = Vector((bbox.p_min[0], bbox.p_min[1], bbox.p_min[2]))
    p_1 = Vector((bbox.p_max[0], bbox.p_min[1], bbox.p_min[2]))
    p_2 = Vector((bbox.p_max[0], bbox.p_min[1], bbox.p_max[2]))
    p_3 = Vector((bbox.p_min[0], bbox.p_min[1], bbox.p_max[2]))

    p_4 = Vector((bbox.p_min[0], bbox.p_max[1], bbox.p_min[2]))
    p_5 = Vector((bbox.p_max[0], bbox.p_max[1], bbox.p_min[2]))
    p_6 = Vector((bbox.p_max[0], bbox.p_max[1], bbox.p_max[2]))
    p_7 = Vector((bbox.p_min[0], bbox.p_max[1], bbox.p_max[2]))

    point_list = []
    point_list.append([p_0, p_1])
    point_list.append([p_1, p_2])
    point_list.append([p_2, p_3])
    point_list.append([p_3, p_0])

    point_list.append([p_4, p_5])
    point_list.append([p_5, p_6])
    point_list.append([p_6, p_7])
    point_list.append([p_7, p_4])

    point_list.append([p_0, p_1])
    point_list.append([p_1, p_5])
    point_list.append([p_5, p_4])
    point_list.append([p_4, p_0])

    point_list.append([p_0, p_4])
    point_list.append([p_4, p_7])
    point_list.append([p_7, p_3])
    point_list.append([p_3, p_0])

    point_list.append([p_2, p_6])
    point_list.append([p_6, p_5])
    point_list.append([p_5, p_1])
    point_list.append([p_1, p_2])

    line_list = []
    for i, line_coordinates in enumerate(point_list):
        line_name = '%s_%d' % (name, i)
        line = nmv.geometry.ops.draw_line(
            point1=line_coordinates[0], point2=line_coordinates[1], format='SIMPLE', thickness=0.5,
            color=(1, 0, 0), name=line_name)
        line_list.append(line)

    # Convert the lines to meshes
    for i in range(len(line_list)):
        line_list[i] = nmv.scene.ops.convert_object_to_mesh(line_list[i])

    # Union them into a single mesh object
    bbox_mesh = nmv.mesh.ops.join_mesh_objects(line_list, name=name)

    # Return a reference to the drawn bounding box
    return bbox_mesh
