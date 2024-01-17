####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Blender modules
import bpy
import bmesh
import mathutils

# Internal imports
import nmv.scene


####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_bmesh_copy_from_mesh_object(mesh_object,
                                       transform=True,
                                       triangulate=False):
    """Creates a bmesh copy from an input mesh object.

    :param mesh_object:
        An input mesh object.
    :param transform:
        Transform to the actual coordinates.
    :param triangulate:
        Triangulate the resulting bmesh.
    :return:
        A bmesh object.
    """
    # If the given object is not mesh, assert
    assert mesh_object.type == 'MESH'

    # Get access to the mesh data
    mesh_data = mesh_object.data

    # If the mesh is in the edit mode
    if mesh_object.mode == 'EDIT':
        bm_orig = bmesh.from_edit_mesh(mesh_data)
        bmesh_object = bm_orig.copy()
    else:
        bmesh_object = bmesh.new()
        bmesh_object.from_mesh(mesh_data)

    # If we need to consider the transformation
    if transform:
        matrix = mesh_object.matrix_world.copy()
        if not matrix.is_identity:
            bmesh_object.transform(matrix)

            # Update normals if the matrix has no rotation.
            matrix.translation.zero()
            if not matrix.is_identity:
                bmesh_object.normal_update()

    # If we need to triangulate the bmesh
    if triangulate:
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_bmesh_copy_from_vertices_and_faces(vertex_data,
                                              face_data,
                                              triangulate=False):
    """Creates a bmesh object from list of vertices and faces.

    @param vertex_data:
        A list of numpy data of vertices.
    @param face_data:
        A list of numpy data of faces.
    @param triangulate:
        If this flag is set, the created bmesh will be triangulated.
    @return:
        A reference to the created bmesh object.
    """

    # Create a new bmesh object
    bmesh_object = bmesh.new()

    # Add the vertices and update the lookup table
    for vertex in vertex_data:
        bmesh_object.verts.new(vertex)
    bmesh_object.verts.ensure_lookup_table()

    # Add the faces and update the lookup table
    for face in face_data:
        v0 = bmesh_object.verts[face[0]]
        v1 = bmesh_object.verts[face[1]]
        v2 = bmesh_object.verts[face[2]]
        bmesh_object.faces.new((v0, v1, v2))
    bmesh_object.faces.ensure_lookup_table()

    # If we need to triangulate the bmesh
    if triangulate:
        bmesh.ops.triangulate(bmesh_object, faces=bmesh_object.faces)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @convert_to_mesh_object
####################################################################################################
def convert_to_mesh_object(bmesh_object,
                           name='mesh'):
    """Converts the bmesh to a new mesh object and rename it. This operation returns a reference to
    the created object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the mesh object.
    :return:
        Returns a reference to the converted object.
    """

    # Create a new mesh object and convert the bmesh object to it
    mesh_object = bpy.data.meshes.new(name)
    bmesh_object.to_mesh(mesh_object)

    # Return a reference to the mesh object
    return mesh_object


####################################################################################################
# @join_bmeshes_list
####################################################################################################
def join_bmeshes_list(bmeshes_list,
                      normal_update=False):
    """Takes as input a list of bm references and outputs a single merged bmesh.

    :param bmeshes_list:
        A list of bmeshes to be joint.
    :param normal_update:
        Force normal calculations
    :return:
        A single merged bmesh.
    """

    # Merged bmesh object
    merged_bmesh = bmesh.new()

    # Vertices list
    add_vert = merged_bmesh.verts.new

    # Faces list
    add_face = merged_bmesh.faces.new

    # Edges list
    add_edge = merged_bmesh.edges.new

    # For every bmesh entry in the list
    for i_bmesh in bmeshes_list:

        # Get the current offset of the vertices
        offset = len(merged_bmesh.verts)

        # Append the vertices
        for v in i_bmesh.verts:
            add_vert(v.co)

        # Update the lookup table
        merged_bmesh.verts.index_update()
        merged_bmesh.verts.ensure_lookup_table()

        # Append the vertices
        if i_bmesh.faces:
            for face in i_bmesh.faces:
                add_face(tuple(merged_bmesh.verts[i.index+offset] for i in face.verts))

            # Update the faces
            merged_bmesh.faces.index_update()

        # Append the edges
        if i_bmesh.edges:
            for edge in i_bmesh.edges:
                edge_seq = tuple(merged_bmesh.verts[i.index+offset] for i in edge.verts)
                try:
                    add_edge(edge_seq)
                except ValueError:
                    # Edge exists!, pass
                    pass

            # Update the edges
            merged_bmesh.edges.index_update()

    # Update the normal
    if normal_update:
        merged_bmesh.normal_update()

    # Return a reference to the merged bmesh
    return merged_bmesh


####################################################################################################
# @convert_from_mesh_object
####################################################################################################
def convert_from_mesh_object(mesh_object):
    """Converts the mesh object to a bmesh object and returns a reference to it.

    :param mesh_object:
        An input mesh object.
    :return:
        A reference to the bmesh object.
    """

    # Return a reference to the bmesh created from the object.
    return bmesh.from_edit_mesh(mesh_object.data)

####################################################################################################
# @create_bmesh_copy_from_mesh_object
####################################################################################################
def create_mesh_copy_from_bmesh_object(bmesh_object,
                                       name):
    """Creates a mesh object from a given bmesh object.

    @param bmesh_object:
        A give bmesh object to create a mesh object from.
    @param name:
        The name of the created mesh object.
    @return:
        The reference of the created mesh object.
    """

    # Create a new mesh object and convert the bmesh object to it
    mesh = bpy.data.meshes.new(name)
    bmesh_object.to_mesh(mesh)

    # Create a blender object, link it to the scene
    mesh_object = bpy.data.objects.new(name, mesh)
    nmv.scene.link_object_to_scene(mesh_object)

    # Return a reference of the created mesh object.
    return mesh_object


####################################################################################################
# @convert_to_mesh_object
####################################################################################################
def link_to_new_object_in_scene(bmesh_object,
                                name='bmesh'):
    """Converts the bmesh to a new mesh object, renames it and links it to the scene as a blender
    object such that you can see it in the interface.
    This operation returns a reference to the created blender object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the object.
    :return:
        A reference to the linked object.
    """

    # Create a mesh object from the bmesh
    mesh_object = convert_to_mesh_object(bmesh_object, name)

    # Create a blender object, link it to the scene
    blender_object = bpy.data.objects.new(name, mesh_object)
    nmv.scene.link_object_to_scene(blender_object)

    # Return a reference to it
    return blender_object


####################################################################################################
# @link_to_existing_object_in_scene
####################################################################################################
def link_to_existing_object_in_scene(bmesh_object,
                                     scene_object):
    """Links the bmesh object to an existing object in the scene.

    :param bmesh_object:
        An input bmesh object.
    :param scene_object:
        An object existing in the scene where the bmesh object will be linked to.
    """

    # Link the bmesh to the given object, and update the mesh.
    bmesh_object.to_mesh(scene_object.data)
    bmesh.update_edit_mesh(scene_object.data, True)


####################################################################################################
# @convert_bmesh_to_mesh
####################################################################################################
def convert_bmesh_to_mesh(bmesh_object,
                          name='bmesh'):
    """Convert a bmesh object to a mesh object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the object.
    :return:
        A reference to the converted mesh.
    """

    return link_to_new_object_in_scene(bmesh_object=bmesh_object, name=name)


####################################################################################################
# @check_self_intersections_of_bmesh_object
####################################################################################################
def check_self_intersections_of_bmesh_object(bmesh_object):
    """Checks if the given bmesh object has self-intersecting faces.

    :param bmesh_object:
        A given bmesh object to delete.
    :return:
        A list of the self-intersecting faces.
    """
    # Construct the BVHTree from the bmesh object
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bmesh_object, epsilon=0.00001)

    # Check if any overlaps exist
    overlap = tree.overlap(tree)

    # Obtain a list of self-intersecting faces
    faces_error = {i for i_pair in overlap for i in i_pair}
    faces_error = list(faces_error)

    # Return a list of faces
    return faces_error


####################################################################################################
# @convert_bmesh_to_mesh
####################################################################################################
def delete_bmesh(bmesh_object):
    """Deletes a bmesh object.

    :param bmesh_object:
        A given bmesh object to delete.
    """
    bmesh.ops.delete(bmesh_object, geom=bmesh_object.faces)


####################################################################################################
# @delete_bmesh_list
####################################################################################################
def delete_bmesh_list(bmesh_list):
    """Delete a list of bmesh objects.

    :param bmesh_list:
        A list of bmesh objects to be deleted.
    """

    for bmesh_object in bmesh_list:
        delete_bmesh(bmesh_object)


####################################################################################################
# @get_partitions_of_bmesh_object
####################################################################################################
def get_partitions_of_bmesh_object(bmesh_object):
    """Detects the number of partitions (or islands) in the given bmesh object.

    :param bmesh_object:
        A given bmesh object to process.
    """

    # Get the paths along the edges of the mesh
    paths = {v.index: set() for v in bmesh_object.verts}
    for e in bmesh_object.edges:
        paths[e.verts[0].index].add(e.verts[1].index)
        paths[e.verts[1].index].add(e.verts[0].index)

    # A list that will contain the different partitions in the mesh. Each partition will be
    # represented by a list of indices of the vertices of that partition.
    partitions_vertices_indices = list()

    # Search
    while True:

        # Get the next path
        try:
            iterator = next(iter(paths.keys()))
        except StopIteration:
            break
        partition = {iterator}
        current = {iterator}
        while True:
            eligible = {sc for sc in current if sc in paths}
            if not eligible:
                break
            current = {ve for sc in eligible for ve in paths[sc]}
            partition.update(current)
            for key in eligible:
                paths.pop(key)

        # Add
        partitions_vertices_indices.append(partition)

    # Convert the set to a list
    return list(partitions_vertices_indices)


####################################################################################################
# @remove_small_partitions_of_bmesh_object
####################################################################################################
def remove_small_partitions_of_bmesh_object(bmesh_object):
    """Removes any small partitions of a given bmesh object to yield a single partition.

    @param bmesh_object:
        A given bmesh object.
    """

    # Get the partitions of the mesh object
    partitions = get_partitions_of_bmesh_object(bmesh_object)

    # There is only a single partition in th e mesh
    if len(partitions) == 1:
        return

    # Remove the small floating partitions
    largest_partition = 0
    largest_partition_number_vertices = len(partitions[0])

    for i in range(1, len(partitions)):
        num_vertices = len(partitions[i])
        if num_vertices > largest_partition_number_vertices:
            largest_partition_number_vertices = num_vertices
            largest_partition = i

    removed_vertices_indices = list()
    for i in range(0, len(partitions)):
        if i == largest_partition: continue
        removed_vertices_indices.extend(partitions[i])
    removed_vertices_indices = list(set(removed_vertices_indices))

    # Remove all the vertices of the small partitions from the mesh object
    nmv.bmeshi.remove_vertices(bmesh_object=bmesh_object, vertices_indices=removed_vertices_indices)

####################################################################################################
# @remove_non_manifold_vertices_of_bmesh_object
####################################################################################################
def remove_non_manifold_vertices_of_bmesh_object(bmesh_object):
    """Removes non-manifold vertices of a given bmesh object

    @param bmesh_object:
        A given bmesh object.
    """

    # Create a list of the non-manifold vertices in the mesh
    vertices_non_manifold = [ele.index for i, ele in enumerate(bmesh_object.verts) if
                             not ele.is_manifold]

    # Remove all the non-manifold vertices
    nmv.bmeshi.remove_vertices(bmesh_object=bmesh_object, vertices_indices=vertices_non_manifold)


####################################################################################################
# @remove_self_intersecting_faces_of_bmesh_object
####################################################################################################
def remove_self_intersecting_faces_of_bmesh_object(bmesh_object,
                                                   self_intersecting_faces):
    """Removes self-intersecting faces of a bmesh object.

    @param bmesh_object:
        A given bmesh object.
    @param self_intersecting_faces:
        A list of all self-intersecting faces in the given bmesh object.
    """

    # Get the vertices of the faces selected and remove the duplicates
    vertices_of_self_intersecting_faces = nmv.bmeshi.get_vertices_indices_from_faces_indices(
        bmesh_object, self_intersecting_faces)

    # Remove the duplicate vertices by making a set and then a list again
    vertices_of_self_intersecting_faces = list(set(vertices_of_self_intersecting_faces))

    # Remove the vertices
    nmv.bmeshi.remove_vertices(bmesh_object, vertices_of_self_intersecting_faces)


####################################################################################################
# @repair_non_manifold_edges_of_bmesh_object
####################################################################################################
def repair_non_manifold_edges_of_bmesh_object(bmesh_object):
    """Repairs the non-manifold edges of a given bmesh object to yield a watertight mesh.

    @param bmesh_object:
        A given bmesh object.
    """

    # Get the non-manifold edges
    edges_non_manifold = [ele for i, ele in enumerate(bmesh_object.edges) if not ele.is_manifold]

    # Fill the given non-manifold edges using the triangle_fill function
    bmesh.ops.triangle_fill(bmesh_object,
                            use_beauty=True,
                            use_dissolve=False,
                            edges=edges_non_manifold)


####################################################################################################
# @is_bmesh_object_watertight
####################################################################################################
def is_bmesh_object_watertight(bmesh_object):

    # Create a list of the non-manifold vertices in the mesh
    non_manifold_vertices_list = [ele.index for i, ele in enumerate(bmesh_object.verts) if
                             not ele.is_manifold]

    # Get the non-manifold edges
    non_manifold_edges_list = [ele for i, ele in enumerate(bmesh_object.edges) if not ele.is_manifold]

    # Self intersections
    self_intersecting_faces_list = check_self_intersections_of_bmesh_object(bmesh_object)

    number_non_manifold_vertices = len(non_manifold_vertices_list)
    number_non_manifold_edges = len(non_manifold_edges_list)
    number_self_intersecting_faces = len(self_intersecting_faces_list)

    if number_non_manifold_vertices > 0 or \
       number_non_manifold_edges > 0 or \
       number_self_intersecting_faces > 0:
        return False, non_manifold_vertices_list, non_manifold_edges_list, self_intersecting_faces_list
    else:
        return True, non_manifold_vertices_list, non_manifold_edges_list, self_intersecting_faces_list

####################################################################################################
# @is_bmesh_object_watertight
####################################################################################################
def try_to_make_bmesh_object_watertight(bmesh_object):
    """Tries to make the given bmesh object watertight.

    @param bmesh_object:
        A given bmesh object.
    """

    # Verify if the mesh is watertight or not
    is_watertight, non_manifold_vertices, non_manifold_edges, self_intersecting_faces = \
        is_bmesh_object_watertight(bmesh_object)

    # If the input mesh is already watertight, then proceed
    if is_watertight:
        return

    iteration = 1
    while True:
        print('WATERTIGHTNESS\t\t Iteration %d' % iteration)

        # Remove the self-intersecting faces from the mesh object
        nmv.bmeshi.remove_self_intersecting_faces_of_bmesh_object(bmesh_object, self_intersecting_faces)

        # Remove the small partitions of the mesh object
        nmv.bmeshi.remove_small_partitions_of_bmesh_object(bmesh_object)

        # Remove the non-manifold vertices
        nmv.bmeshi.remove_non_manifold_vertices_of_bmesh_object(bmesh_object)

        # Repair the non-manifold edges
        nmv.bmeshi.repair_non_manifold_edges_of_bmesh_object(bmesh_object)

        is_watertight, non_manifold_vertices, non_manifold_edges, self_intersecting_faces = \
            is_bmesh_object_watertight(bmesh_object)

        # If the mesh is watertight, the return
        if is_watertight:
            print('WATERTIGHTNESS\t\t OK!')
            return

        # Otherwise, make another iteration
        else:
            iteration += 1

