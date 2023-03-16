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

# Blender imports
import bpy


####################################################################################################
# @create_new_collection
####################################################################################################
def create_new_collection(name='Collection'):
    """Creates a new collection in the scene to group the objects into it.

    :param name:
        Collection name.
    :return:
        A reference to the created collection
    """

    # Create the collection
    collection = bpy.data.collections.new(name=name)

    # Link it to the scene to appear in the UI
    bpy.context.scene.collection.children.link(collection)

    # Return a reference to it
    return collection


####################################################################################################
# @delete_collection
####################################################################################################
def delete_collection(collection,
                      remove_contents=True):
    """Deletes a given collection and deletes its contents.

    :param collection:
        A reference to the collection that needs to be deleted.
    :param remove_contents:
        If this flag is set, all the content of the collection will be removed.
    """

    # Remove the contents
    if remove_contents:
        for i_object in collection.objects:
            bpy.data.objects.remove(i_object, do_unlink=True)

    # Delete the collection
    bpy.data.collections.remove(collection)


####################################################################################################
# @delete_collection_by_name
####################################################################################################
def delete_collection_by_name(name):
    """Deletes a collection identified by its name.

    :param name:
        Collection name.
    """

    # Get the collection
    try:
        collection = bpy.data.collections.get(name)
    except IndexError:
        return

    # Delete the collection
    delete_collection(collection)


####################################################################################################
# @move_objects_to_collection
####################################################################################################
def move_objects_to_collection(collection,
                               objects_list):
    """Moves a given list of objects into a given collection.

    :param collection:
        A reference to the collection.
    :param objects_list:
        A list of objects to be moved to the given collection.
    """

    for i_object in objects_list:

        # Unlink from the collections
        for i_collection in i_object.users_collection:
            i_collection.objects.unlink(i_object)

        # Link to the current collection
        if i_object.name not in collection.objects:
            collection.objects.link(i_object)


####################################################################################################
# @create_collection_with_objects
####################################################################################################
def create_collection_with_objects(name,
                                   objects_list):
    """Creates a new collection and moves a list of objects into it.

    :param name:
        Collection name.
    :param objects_list:
        A list of objects to be moved to the collection after its creation.
    :return:
        A reference to the created collection
    """

    # Create the collection
    collection = create_new_collection(name=name)

    # Move the objects into this collection
    move_objects_to_collection(collection=collection, objects_list=objects_list)

    # Return a reference to this collection
    return collection