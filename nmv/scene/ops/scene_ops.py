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
import os, sys, bpy

# Blender imports
from mathutils import Vector

# Internal impots
import nmv
import nmv.bbox
import nmv.mesh


####################################################################################################
# @clear_default_scene
####################################################################################################
def clear_default_scene():
    """Clear the default scene loaded in Blender: the ['Cube', 'Lamp' and 'Camera'].
    """

    # Iterate over all the objects in the scene, and remove the 'Cube', 'Lamp' and 'Camera' if exist
    for scene_object in bpy.context.scene.objects:

        # Object selection
        if scene_object.name == 'Cube' or \
           scene_object.name == 'Lamp' or \
           scene_object.name == 'Camera':
            scene_object.select = True

            # Delete the object
            bpy.ops.object.delete()


####################################################################################################
# @clear_scene
####################################################################################################
def clear_scene():
    """Clear a scene and remove all the existing objects in it and unlink their references.

    NOTE: This function targets clearing meshes, curve, objects and materials.
    """

    # Adjust the clipping planes in case of perspective projection
    # bpy.context.space_data.clip_start = 0.01
    # bpy.context.space_data.clip_end = 10000

    # Select each object in the scene
    for scene_object in bpy.context.scene.objects:
        scene_object.select = True

    # Delete all the objects
    bpy.ops.object.delete()

    # Unlink all the objects in all the layers
    for scene in bpy.data.scenes:
        for scene_object in scene.objects:
            scene.objects.unlink(scene_object)

    # Select all the meshes, unlink them and clear their data
    for scene_mesh in bpy.data.meshes:
        scene_mesh.user_clear()
        bpy.data.meshes.remove(scene_mesh)

    # Select all the curves, unlink them and clear their data
    for scene_curve in bpy.data.curves:
        scene_curve.user_clear()
        bpy.data.curves.remove(scene_curve)

    # Select all the scene objects, unlink them and clear their data
    for scene_object in bpy.data.objects:
        scene_object.user_clear()
        bpy.data.objects.remove(scene_object)

    # Select all the scene materials, unlink them and clear their data
    for scene_material in bpy.data.materials:
        scene_material.user_clear()
        bpy.data.materials.remove(scene_material)


####################################################################################################
# @clear_lights
####################################################################################################
def clear_lights():
    """Clear the lights.
    """

    # Iterate over all the objects in the scene, and remove the 'Cube', 'Lamp' and 'Camera' if exist
    for scene_object in bpy.context.scene.objects:

        # Object selection
        if 'Lamp' in scene_object.name:
            scene_object.select = True

            # Delete the object
            bpy.ops.object.delete()

    # Select all the light, unlink them and clear their data
    for scene_lamp in bpy.data.lamps:
        scene_lamp.user_clear()
        bpy.data.lamps.remove(scene_lamp)


####################################################################################################
# @select_all
####################################################################################################
def select_all():
    """Select all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to True.
    for scene_object in bpy.context.scene.objects:
        scene_object.select = True


####################################################################################################
# @deselect_all
####################################################################################################
def deselect_all():
    """Deselect all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to False.
    for scene_object in bpy.context.scene.objects:
        scene_object.select = False


####################################################################################################
# @select_objects
####################################################################################################
def select_objects(object_list):
    """Select all the objects in a given list.

    :param object_list:
        A list of objects that exist in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to True
    for scene_object in object_list:
        scene_object.select = True


####################################################################################################
# @select_object_by_name
####################################################################################################
def select_object_by_name(object_name):
    """Select an object in the scene given its name.

    :param object_name:
        The name of object to be selected.
    """

    # Set the '.select' flag of the object to True
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            scene_object.select = True


####################################################################################################
# @deselect_object_by_name
####################################################################################################
def deselect_object_by_name(object_name):
    """Deselect an object in the scene given its name.

    :param object_name:
        The name of object to be deselected.
    """

    # Set the '.select' flag of the object to False
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            scene_object.select = False


####################################################################################################
# @select_all_meshes_in_scene
####################################################################################################
def select_all_meshes_in_scene():
    """Select all the mesh objects (those of type 'MESH') in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Select only the objects of type meshes
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            scene_object.select = True


####################################################################################################
# @deselect_all_meshes_in_scene
####################################################################################################
def deselect_all_meshes_in_scene():
    """Deselect all the mesh objects (those of type 'MESH') in the scene.
    """

    # Select only the objects of type meshes
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            scene_object.select = False


####################################################################################################
# @select_all_curves_in_scene
####################################################################################################
def select_all_curves_in_scene():
    """Selects all the curve objects (those of type 'CURVE') in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Deselect only the objects of type curves
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            scene_object.select = True


####################################################################################################
# @deselect_all_curves_in_scene
####################################################################################################
def deselect_all_curves_in_scene():
    """Deselects all the curve objects (those of type 'CURVE') in the scene.
    """

    # Deselect only the objects of type curves
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            scene_object.select = False


####################################################################################################
# @get_list_of_meshes_in_scene
####################################################################################################
def get_list_of_meshes_in_scene():
    """Return a list of references to all the meshes (objects of type 'MESH') in the scene.

    :return:
        A list of references to all the meshes (objects of type 'MESH') in the scene.
    """

    # Mesh list
    mesh_list = list()

    # Select only the objects of type meshes, and append their references to the list
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            mesh_list.append(scene_object)

    # Return a reference to the list
    return mesh_list


####################################################################################################
# @get_list_of_curves_in_scene
####################################################################################################
def get_list_of_curves_in_scene():
    """Return a list of references to all the curves (objects of type 'CURVE') in the scene.

    :return:
        A list of references to all the curves (objects of type 'CURVE') in the scene
    """

    # Curve list
    curve_list = list()

    # Select only the objects of type meshes, and append their references to the list
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            curve_list.append(scene_object)

    # Return a reference to the list
    return curve_list


####################################################################################################
# @get_reference_to_object_by_name
####################################################################################################
def get_reference_to_object_by_name(object_name):
    """Return a reference to an object in the scene given its name.

    :param object_name:
        The name of object.
    :return:
        A reference to the selected object.
    """

    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            return scene_object


####################################################################################################
# @delete_object
####################################################################################################
def delete_object_in_scene(scene_object):
    """Delete a given object from the scene.

    :param scene_object:
        A given object to be deleted from the scene.
    """

    # Deselect all the other objects in the scene
    deselect_all()

    # Select this particular object, to highlight it
    scene_object.select = True

    # Delete the selected object
    bpy.ops.object.delete(use_global=False)


####################################################################################################
# @delete_list_objects
####################################################################################################
def delete_list_objects(object_list):
    """Delete a given list of objects in the scene.

    :param object_list:
        A list of objects to be deleted from the scene.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Delete object by object from the list
    for scene_object in object_list:

        # Select this particular object, to highlight it
        scene_object.select = True

        # Delete the selected object
        bpy.ops.object.delete(use_global=False)


####################################################################################################
# @delete_all
####################################################################################################
def delete_all():
    """Delete all the objects in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Delete object by object from the scene
    for scene_object in bpy.context.scene.objects:

        # Select this particular object, to highlight it
        scene_object.select = True

        # Delete the selected object
        bpy.ops.object.delete(use_global=False)


####################################################################################################
# @set_active_object
####################################################################################################
def set_active_object(scene_object):
    """Set the active object in the scene to the given one.

    :param scene_object:
        A given object in the scene that is desired to be active.

    :return
        A reference to the active object.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Select the object
    scene_object.select = True

    # Set it active
    bpy.context.scene.objects.active = scene_object

    # Return a reference to the mesh object again for convenience
    return scene_object


####################################################################################################
# @rotate_object
####################################################################################################
def rotate_object(scene_object,
                  x=0.0, y=0.0, z=0.0):
    """Rotate the given object in the scene using Euler rotation.

    :param scene_object:
        A given object in the scene to be rotated.
    :param x:
        X angle.
    :param y:
        Y angle.
    :param z:
        Z angle.
    """

    # Rotate the object
    scene_object.rotation_euler = (x, y, z)


####################################################################################################
# @get_object_orientation
####################################################################################################
def get_object_orientation(scene_object):
    """Return the Euler orientation of the object.

    :param scene_object:
        A given object in the scene.
    :return:
        The current orientation of the given object in the scene.
    """

    # Returns the orientation vector
    return scene_object.rotation_euler


####################################################################################################
# @set_object_location
####################################################################################################
def set_object_location(scene_object,
                        location):
    """Set the given object a given location in the scene.

    :param scene_object:
        A given object in the scene to be translated.
    :param location:
        The new (or desired) location of the object.
    """

    # Set location
    scene_object.location = location


####################################################################################################
# @get_object_location
####################################################################################################
def get_object_location(scene_object):
    """Return the location of the given object in the scene.

    :param scene_object:
        The object required to know its current location.
    :return:
        The current location of the object.
    """

    # Returns the location vector
    return scene_object.location


####################################################################################################
# @scale_object
####################################################################################################
def scale_object(scene_object,
                 x=1.0, y=1.0, z=1.0):
    """Scale the given object in the scene non-uniformly.

    :param scene_object:
        The object to be scaled.
    :param x:
        X scale factor.
    :param y:
        Y scale factor.
    :param z:
        Z scale factor.
    """

    # Scale the object
    scene_object.scale = (x, y, z)


####################################################################################################
# @get_object_scale
####################################################################################################
def get_object_scale(scene_object):
    """Return the scale of the given object.

    :param scene_object:
        A given object in the scene.
    :return:
        The current scale of the given object.
    """

    # Returns the orientation vector
    return scene_object.scale


####################################################################################################
# @scale_object_uniformly
####################################################################################################
def scale_object_uniformly(scene_object,
                           scale_factor=1.0):
    """Scale the given object uniformly in XYZ.

    :param scene_object:
        A given object in the scene.
    :param scale_factor:
        Uniform scale factor.
    """

    # Scale the object.
    scale_object(scene_object, x=scale_factor, y=scale_factor, z=scale_factor)


####################################################################################################
# @scale_mesh_object_to_fit_within_unity_cube
####################################################################################################
def scale_mesh_object_to_fit_within_unity_cube(scene_object,
                                               scale_factor=1):
    """Scale a given mesh object within a cube.

    :param scene_object:
        A given scene object.
    :param scale_factor:
        A scale factor to rescale the unity cube.
    """

    # Compute the bounding box of the mesh
    mesh_bbox = nmv.bbox.get_object_bounding_box(scene_object)

    # Get the largest dimension of the mesh
    largest_dimension = mesh_bbox.bounds[0]
    if mesh_bbox.bounds[1] > largest_dimension:
        largest_dimension = mesh_bbox.bounds[1]
    if mesh_bbox.bounds[2] > largest_dimension:
        largest_dimension = mesh_bbox.bounds[2]

    # Compute the scale factor
    unified_scale_factor = scale_factor / largest_dimension

    # Scale the mesh
    nmv.scene.ops.scale_object_uniformly(scene_object, unified_scale_factor)


####################################################################################################
# @scale_object_uniformly
####################################################################################################
def center_mesh_object(scene_object):
    """Center a given mesh object at the origin.

    :param scene_object:
        A mesh object to be centered at the origin of the scene based on its bounding box.
    """

    # Compute the object bounding box center from all the vertices of the object
    bbox_center = Vector((0, 0, 0))
    p_max = Vector((-1e10, -1e10, -1e10))
    p_min = Vector((1e10, 1e10, 1e10))

    for vertex in scene_object.data.vertices:
        if vertex.co[0] > p_max[0]:
            p_max[0] = vertex.co[0]
        if vertex.co[1] > p_max[1]:
            p_max[1] = vertex.co[1]
        if vertex.co[2] > p_max[2]:
            p_max[2] = vertex.co[2]
        if vertex.co[0] < p_min[0]:
            p_min[0] = vertex.co[0]
        if vertex.co[1] < p_min[1]:
            p_min[1] = vertex.co[1]
        if vertex.co[2] < p_min[2]:
            p_min[2] = vertex.co[2]
    bounds = p_max - p_min
    bbox_center = p_min + (0.5 * bounds)

    # For each vertex in the mesh, center it
    for vertex in scene_object.data.vertices:
        vertex.co = vertex.co - bbox_center


####################################################################################################
# @rotate_object_towards_target
####################################################################################################
def rotate_object_towards_target(scene_object,
                                 object_normal,
                                 target_point):
    """Rotate a given object in the scene towards a target point using Euler rotation.

    :param scene_object:
        A given object in the scene.
    :param object_normal:
        Object normal.
    :param target_point:
        The target point for the rotation.
    """

    # Get the location of the object
    object_location = get_object_location(scene_object)

    # Compute the rotation direction
    rotation_direction = (target_point - object_location).normalized()

    # Compute the rotation difference, based on the normal
    rotation_difference = object_normal.rotation_difference(rotation_direction)

    # Get the euler angles
    rotation_euler = rotation_difference.to_euler()

    # Update the rotation angles
    scene_object.rotation_euler[0] = (rotation_euler[0])
    scene_object.rotation_euler[1] = (rotation_euler[1])
    scene_object.rotation_euler[2] = (rotation_euler[2])


####################################################################################################
# @convert_object_to_mesh
####################################################################################################
def convert_object_to_mesh(scene_object):
    """Convert a scene object (for example curve or poly-line) to a surface mesh.

    :param scene_object:
        A given scene object, for example curve or poly-line.
    :return:
        A reference to the created mesh object.
    """

    # Deselects all objects in the scene
    set_active_object(scene_object)

    # Convert the given object to a mesh
    bpy.ops.object.convert(target='MESH')

    # Return the mesh object
    return scene_object


####################################################################################################
# @duplicate_object
####################################################################################################
def duplicate_object(original_object,
                     duplicated_object_name=None,
                     link_to_scene=True):
    """
    Duplicates an object in the scene and returns a reference to the duplicated object.

    :param original_object:
        The original object that will be duplicated in the scene.
    :param duplicated_object_name:
        The name of the new object.
    :param link_to_scene:
        Link the duplicate object to the scene.
    :return:
        A reference to the duplicated object.
    """

    # Deselect all the objects in the scene
    for scene_object in bpy.context.scene.objects:
        scene_object.select = False

    # Duplicate the object
    duplicated_object = original_object.copy()

    # Make this a real duplicate (not linked)
    duplicated_object.data = original_object.data.copy()

    # Update the duplicate name
    if duplicated_object_name is None:
        duplicated_object.name = str(original_object.name) + '_duplicate'
    else:
        duplicated_object.name = str(duplicated_object_name)

    # Link it to the scene
    if link_to_scene:
        bpy.context.scene.objects.link(duplicated_object)

        # Deselect all the objects in the scene
        for scene_object in bpy.context.scene.objects:
            scene_object.select = False

    # Return a reference to the duplicate object
    return duplicated_object


####################################################################################################
# @clone_mesh_objects_into_joint_mesh
####################################################################################################
def clone_mesh_objects_into_joint_mesh(mesh_objects):
    """Clones a list of mesh objects and join the clones into a single object.

    NOTE: This function is normally used to export a mesh object without affecting any mesh in
    the scene.

    :param mesh_objects:
        A list of mesh objects in the scene.
    :return:
        A joint mesh object that can be used directly to export a mesh.
    """

    # Deselect all the other objects in the scene
    deselect_all()

    # Clones the mesh objects to join them together to export the mesh
    cloned_mesh_objects = list()
    for mesh_object in mesh_objects:
        cloned_mesh_objects.append(nmv.scene.duplicate_object(mesh_object))
    joint_mesh_object = nmv.mesh.join_mesh_objects(cloned_mesh_objects)

    # Deselect all the other objects in the scene
    deselect_all()

    # Activate the joint mesh object
    select_objects([joint_mesh_object])
    set_active_object(joint_mesh_object)

    # Return the clones mesh
    return joint_mesh_object


####################################################################################################
# @is_object_in_scene
####################################################################################################
def is_object_in_scene(input_object):
    """Verify if a given object exists in the scene or not.

    :param input_object:
        A given object to be checked if it exists in the scene or not.
    :return:
        True or False.
    """

    # If the object is None, then it cannot exist in the scene
    if input_object is None:
        return False

    # Loop over all the objects in the scene, and check by name
    for scene_object in bpy.context.scene.objects:

        # Verify
        if scene_object.name == input_object.name:

            # Yes it exists
            return True

    # No, it doesn't exist
    return False


####################################################################################################
# @is_object_in_scene_by_name
####################################################################################################
def is_object_in_scene_by_name(object_name):
    """Verify if a given object identified by its name exists in the scene or not.

    :param object_name:
        The object name.
    :return:
        True or False.
    """
    # If the object is None, then it cannot exist in the scene
    if object_name is None:
        return False

    # Loop over all the objects in the scene, and check by name
    for scene_object in bpy.context.scene.objects:

        # Verify the name
        if scene_object.name == object_name:

            # Yes it exists
            return True

    # No, it doesn't exist
    return False


####################################################################################################
# @view_all_scene
####################################################################################################
def view_all_scene():
    """View all the objects in the scene.
    """

    # Switch to the top view
    bpy.ops.view3d.viewnumpad(type='TOP')

    # View all the objects in the scene
    bpy.ops.view3d.view_all()
