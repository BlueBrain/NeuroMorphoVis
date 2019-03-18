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

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal modules
import nmv
import nmv.scene
import nmv.mesh


####################################################################################################
# @deselect_all_vertices
####################################################################################################
def deselect_all_vertices(mesh_object):
    """Deselect all the vertices of a given mesh object.

    :param mesh_object:
        A given mesh object.
    """

    # Deselect all the objects in the scene
    nmv.scene.ops.deselect_all()

    # Select only the object of interest and set it the only active object
    nmv.scene.ops.set_active_object(mesh_object)

    # Switch to edit mode to be able to select the vertices
    bpy.ops.object.mode_set(mode='EDIT')

    # Apply a vertex deselection action to the selected object
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')

    # Switch back to the object mode
    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @select_all_vertices
####################################################################################################
def select_all_vertices(mesh_object):
    """Select all the vertices on a given object.

    :param mesh_object:
        A given mesh object.
    """

    # Deselect all the vertices to avoid Blender crashes
    deselect_all_vertices(mesh_object)

    # Select the object and activate it
    nmv.scene.ops.set_active_object(mesh_object)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Select all vertices
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='SELECT')

    # Switch back to edit mode
    bpy.ops.object.editmode_toggle()


####################################################################################################
# @deselect_vertex
####################################################################################################
def deselect_vertex(mesh_object,
                    vertex_index):
    """Deselect a given vertex of a given mesh object relying on its index.

    :param mesh_object:
        A given mesh object.
    :param vertex_index:
        The index of a certain vertex to deselect.
    """

    # deselecting a vertex by setting its select flag to False !
    mesh_object.data.vertices[vertex_index].select = False


####################################################################################################
# @deselect_vertices
####################################################################################################
def deselect_vertices(mesh_object,
                      vertices_indices):
    """Deselect a group of vertices in a mesh object using a list containing their indices.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        A list of indices of the vertices to be deselected.
    """

    # Deselecting all the vertices by setting their select flags to False !
    for vertex_index in vertices_indices:
        mesh_object.data.vertices[vertex_index].select = False


####################################################################################################
# @select_vertex
####################################################################################################
def select_vertex(mesh_object,
                  vertex_index):
    """Select a vertex on a given mesh object specified by its index.

    :param mesh_object:
        A given mesh object.
    :param vertex_index:
        The index of a certain vertex to select.
    """

    # Deselect all the vertices to avoid crashes
    deselect_all_vertices(mesh_object)

    # Get the vertex by its index and select it
    mesh_object.data.vertices[vertex_index].select = True


####################################################################################################
# @select_vertices
####################################################################################################
def select_vertices(mesh_object,
                    vertices_indices):
    """Select a set of vertices on a given mesh object specified by their indices.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        A list of indices of the vertices to be selected.
    """

    # Deselect all the vertices to avoid crashes
    deselect_all_vertices(mesh_object)

    # Select all the vertices by setting their select flags to True !
    for vertex_index in vertices_indices:
        mesh_object.data.vertices[vertex_index].select = True


####################################################################################################
# @select_face_vertices
####################################################################################################
def select_face_vertices(mesh_object,
                         face_index):
    """Select the vertices of a face in a given object using its face index.

    :param mesh_object:
        A given mesh object.
    :param face_index:
        The index of the requested face to be selected.
    """

    # Deselect all the vertices to avoid crashes
    deselect_all_vertices(mesh_object)

    # Get the face and select its vertices one by one
    face = mesh_object.data.polygons[face_index]
    vertices_indices = []
    for vertex in face.vertices[:]:
        vertices_indices.append(vertex)

    # Select all the retrieved vertices
    for vertex_index in vertices_indices:
        mesh_object.data.vertices[vertex_index].select = True


####################################################################################################
# @get_faces_vertices_indices
####################################################################################################
def get_faces_vertices_indices(mesh_object,
                               face_index):
    """Return a list of vertices of a face in a given mesh object using the face index.

    :param mesh_object:
        A given mesh object.
    :param face_index:
        The index of the requested face to get its vertices.
    :return:
        The indices of the vertices composing the selected face.
    """

    # Get the face and select its vertices one by one
    face = mesh_object.data.polygons[face_index]

    # A list that will contain the indices of the selected vertices
    vertices_indices = list()

    # Iterate over all the vertices of the face object
    for vertex in face.vertices[:]:

        # Append
        vertices_indices.append(vertex)

    # Return a list of the indices of the selected vertices that correspond to the face
    return vertices_indices


####################################################################################################
# @get_vertices_in_object
####################################################################################################
def get_vertices_in_object(mesh_object):
    """Return a list of all the vertices in an object.

    :param mesh_object:
        A given mesh object.
    :return:
        A list of all the vertices composing the mesh object.
    """

    # Deselect all the vertices to avoid crashes
    deselect_all_vertices(mesh_object)

    # A list of all the vertices in the object
    vertices_list = list()

    # Iterate over all the vertices of the mesh object
    for vertex in mesh_object.data.vertices[:]:

        # Append
        vertices_list.append(vertex.co)

    # Return a list of the vertices that correspond to the entire object
    return vertices_list


####################################################################################################
# @get_vertices_indices_in_object
####################################################################################################
def get_vertices_indices_in_object(mesh_object):
    """Return a list of the indices of all the vertices in a given mesh object.

    :param mesh_object:
        A given mesh object.
    :return:
        A list of all the indices of the vertices composing the mesh object.
    """

    # Deselect all the vertices to avoid craches
    deselect_all_vertices(mesh_object)

    # Get a list of all the indices of the vertices in the object
    vertices_indices_list = []

    # Iterate over all the vertices of the mesh object
    for vertex in mesh_object.data.vertices[:]:

        # Append
        vertices_indices_list.append(vertex.index)

    # Return a list of the indices of the vertices that correspond to the entire object
    return vertices_indices_list


####################################################################################################
# @compute_centroid
####################################################################################################
def compute_centroid(mesh_object):
    """Compute the centroid of an object.

    :param mesh_object:
        A given mesh object.
    :return:
        The centroid of the mesh object.
    """

    # Compute the centroid from all the vertices of the mesh object
    centroid = Vector((0, 0, 0))

    # Compute the weights
    for vertex in mesh_object.data.vertices[:]:
        centroid = centroid + vertex.co

    # Normalize
    centroid = centroid / len(mesh_object.data.vertices)

    # Return the centroid
    return centroid


####################################################################################################
# @compute_centroid_of_vertices
####################################################################################################
def compute_centroid_of_vertices(mesh_object,
                                 vertices_indices):
    """Compute the centroid of the certain vertices in the mesh.

    NOTE: This method is quite useful in the bridging operations, since we need to compute the
    nearest point to the centroid of the first face in a mesh, but only using vertex data not face
    index.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        A list of indices of the vertices that will contribute to the centroid calculation.
    :return:
        The computed centroid.
    """

    # Compute the centroid
    centroid = Vector((0.0, 0.0, 0.0))

    # Compute the weights
    for vertex_index in vertices_indices:

        # Add the vertex value
        centroid += mesh_object.data.vertices[vertex_index].co

    # Normalize
    centroid = centroid / len(vertices_indices)

    # Return the centroid
    return centroid


####################################################################################################
# @create_vertex_group
####################################################################################################
def create_vertex_group(mesh_object,
                        name='vertex_group'):
    """Create a new vertex group.

    :param mesh_object:
        A given mesh object.
    :param name:
        The name of the vertex group.
    :return:
        A reference to the created vertex group.
    """

    # Create the vertex group
    vertex_group = mesh_object.vertex_groups.new(name)

    # Return a reference to the vertex group
    return vertex_group


####################################################################################################
# @add_vertex_to_vertex_group
####################################################################################################
def add_vertex_to_vertex_group(mesh_object,
                               vertex_index,
                               name='vertex_group'):
    """Add a vertex specified by its index to a vertex group for a given object.

    NOTE: The vertex group will be created here, but it can be used to append other vertices to
    it later.

    :param mesh_object:
        A given mesh object.
    :param vertex_index:
        The index of the vertex that will be added to the vertex group.
    :param name:
        The name of the vertex group.
    :return:
        A reference to the vertex group, for double checking.
    """

    # Add the vertex to this specific vertex group.
    vertex_group = mesh_object.vertex_groups.new(name)
    vertex_group.add([vertex_index], 1.0, "ADD")

    # Return a reference to the vertex group
    return vertex_group


####################################################################################################
# @add_vertex_to_existing_vertex_group
####################################################################################################
def add_vertex_to_existing_vertex_group(vertex_index,
                                        vertex_group):
    """Add a single vertex in a list to the vertex group.

    :param vertex_index:
        A list having only one vertex to be added to the vertex group.
    :param vertex_group:
        The vertex group.
    """

    # Add the vertex to an existing vertex group
    vertex_group.add([vertex_index], 1.0, "ADD")


####################################################################################################
# @add_vertices_to_vertex_group
####################################################################################################
def add_vertices_to_vertex_group(mesh_object,
                                 vertices_indices,
                                 name='vertex_group'):
    """Add a vertex specified by its index to a vertex group for a given object.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        A list of the indices of all the vertices to be added to the group.
    :param name:
        The name of the vertex group.
    :return:
        A reference to the vertex group.
    """

    # Create a vertex group
    vertex_group = mesh_object.vertex_groups.new(name)

    # Add all the vertices defined by their indices to the vertex group
    for vertex_index in vertices_indices:

        # Add the vertex index to the vertex group
        vertex_group.add([vertex_index], 1.0, "ADD")

    # Return a reference to the created vertex group
    return vertex_group


####################################################################################################
# @add_vertices_to_existing_vertex_group
####################################################################################################
def add_vertices_to_existing_vertex_group(vertices_indices,
                                          vertex_group):
    """Add new vertices to the vertex group.

    :param vertices_indices:
        A list of the indices of all the vertices to be added to the group.
    :param vertex_group:
        Existing vertex group.
    """

    # Add the vertices by their index to an existing vertex group
    for vertex_index in vertices_indices:

        # Add the vertex index to the vertex group
        vertex_group.add([vertex_index], 1.0, "ADD")


####################################################################################################
# @create_face_from_selected_vertices
####################################################################################################
def create_face_from_selected_vertices(mesh_object,
                                       vertices_indices):
    """Create a single face from the selected vertices.

    :param mesh_object:
        A given mesh object.
    :param vertices_indices:
        A list of indices of the vertices to create the face from.
    :return:
        The index of the created face.
    """

    # Activate the mesh object
    nmv.scene.ops.set_active_object(mesh_object)

    # Deselect all the vertices
    deselect_all_vertices(mesh_object)

    # Select the vertices based on their indices
    select_vertices(mesh_object, vertices_indices)

    # Switch to edit mode
    bpy.ops.object.editmode_toggle()

    # Merge the faces into a single face, F-key in interface
    bpy.ops.mesh.edge_face_add()

    #  Switch back to object mode
    bpy.ops.object.editmode_toggle()

    # Note: Since we don't know the face count after the merge operation, we will just use this
    # trick in this case, but later, we can account for +5 and search amongst them only
    face_index = -1

    # Iterate over all the faces in the polygon
    for face in mesh_object.data.polygons[:]:

        # If the face is selected
        if face.select:

            # Get its index
            face_index = face.index

            # Break, we are done
            break

    # Return the face index
    return face_index


####################################################################################################
# @get_index_of_nearest_vertex_to_point
####################################################################################################
def get_index_of_nearest_vertex_to_point(mesh_object,
                                         point):
    """Get the index of the nearest vertex of an object to a given point in the space.

    :param mesh_object:
        A given mesh object.
    :param point:
        A given point in the three-dimensional space.
    :return:
        The index of the nearest vertex in the mesh to the given point.
    """

    # Initialize the nearest face index to -1
    nearest_vertex_index = -1

    # Initialize the shortest distance to infinity
    shortest_distance = 10000000000

    # Iterate over all the vertices in the mesh
    for vertex in mesh_object.data.vertices:

        # Compute the distance between the point and the vertex
        distance = (vertex.co - point).length

        # Check the distance
        if distance < shortest_distance:

            # Update
            shortest_distance = distance
            nearest_vertex_index = vertex.index

    # Return the nearest vertex index
    return nearest_vertex_index


####################################################################################################
# @get_vertex_position
####################################################################################################
def get_vertex_position(mesh_object,
                        vertex_index):
    """Gets the position of a vertex in a given mesh specified by its index.

    :param mesh_object:
        A mesh object that contains the vertex.
    :param vertex_index:
        The index of the vertex.
    :return:
        The position of the vertex.
    """

    return mesh_object.data.vertices[vertex_index].co