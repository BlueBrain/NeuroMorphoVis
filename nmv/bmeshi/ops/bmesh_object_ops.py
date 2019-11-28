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

# Blender modules
import bpy
import bmesh

import nmv
import nmv.scene


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