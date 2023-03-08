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
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.mesh
import nmv.consts
import nmv.utilities


####################################################################################################
# @update_scene
####################################################################################################
def update_scene():
    """Updates the scene after any transformation
    """

    bpy.context.view_layer.update()


####################################################################################################
# @view_axis
####################################################################################################
def view_axis(axis='TOP'):
    """View the axis in the view.

    :param axis:
        An enum in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', 'BACK'].
    """

    if nmv.utilities.is_blender_280():
        bpy.ops.view3d.view_axis(type=axis)
    else:
        bpy.ops.view3d.viewnumpad(type=axis)


####################################################################################################
# @select_object
####################################################################################################
def select_object(scene_object):
    """Selects a given object in the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param scene_object:
        A given scene object to be selected.
    """

    if nmv.utilities.is_blender_280():
        scene_object.select_set(True)
    else:
        scene_object.select = True


####################################################################################################
# @deselect_object
####################################################################################################
def deselect_object(scene_object):
    """Deselects a given object in the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param scene_object:
        A given scene object to be deselected.
    """

    if nmv.utilities.is_blender_280():
        scene_object.select_set(False)
    else:
        scene_object.select = False


####################################################################################################
# @is_object_deleted
####################################################################################################
def is_object_deleted(scene_object):
    """Checks if an object in the scene is deleted or not.

    :param scene_object:
        A given scene object to check.
    :return:
        True if the object is deleted, otherwise False.
    """

    return not (scene_object.name in bpy.data.objects)


####################################################################################################
# @set_transparent_background
####################################################################################################
def set_transparent_background():
    """Sets the background image to transparent.
    """

    # 2.80 or higher
    if nmv.utilities.is_blender_280():

        # Transparency
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    # 2.79
    else:
        bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'


####################################################################################################
# @set_colors_to_raw
####################################################################################################
def set_colors_to_raw():
    """Use RAW colors with FLAT shading to lighten the results
    """
    bpy.context.scene.view_settings.view_transform = 'Raw'


####################################################################################################
# @set_colors_to_filimc
####################################################################################################
def set_colors_to_filimc():
    """Use filmic mode for rendering.
    """
    bpy.context.scene.view_settings.view_transform = 'Filmic'


####################################################################################################
# @set_background_color
####################################################################################################
def set_background_color(color,
                         transparent=False):
    """Sets the background image properties.

    :param color:
        A given color.
    :param transparent:
        A flag to indicate if the image is transparent or not. Setting this flag to True overrides
        the color.
    """

    # 2.80 or higher
    if nmv.utilities.is_blender_280():

        # Transparency
        bpy.context.scene.render.film_transparent = transparent

        # Image mode to avoid the alpha channel issues
        if transparent:
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        else:
            bpy.context.scene.render.image_settings.color_mode = 'RGB'

            # If Workbench render is used, adjust the color as follows
            if bpy.context.scene.render.engine == 'BLENDER_WORKBENCH':

                # Set the color selected
                bpy.context.scene.world.color = color

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bpy.context.scene.world.color = nmv.consts.Color.VERY_WHITE

            # Cycles and Eevee
            else:

                # Get a reference to the WORLD
                world = bpy.data.worlds['World']

                # Use nodes
                world.use_nodes = True

                # Get the background node
                bg = world.node_tree.nodes['Background']

                # Set the color
                bg.inputs[0].default_value = (color[0], color[1], color[2], 1)

                # Fix the WHITE BUG
                # if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                #    bg.inputs[0].default_value = (10, 10, 10, 1)
    # 2.79
    else:

        # Transparency background
        if transparent:
            bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'

        # Non-transparent background
        else:

            # If Cycles
            if bpy.context.scene.render.engine == 'CYCLES':

                # Get a reference to the WORLD
                world = bpy.data.worlds['World']

                # Use nodes
                world.use_nodes = True

                # Get the background node
                bg = world.node_tree.nodes['Background']

                # Set the color
                bg.inputs[0].default_value = (color[0], color[1], color[2], 1)

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bg.inputs[0].default_value = (10, 10, 10, 1)

            # If Blender render
            else:
                bpy.context.scene.render.alpha_mode = 'SKY'
                bpy.context.scene.render.image_settings.color_mode = 'RGB'

                # Color
                bpy.context.scene.world.horizon_color = color

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bpy.context.scene.world.horizon_color = nmv.consts.Color.VERY_WHITE


####################################################################################################
# @get_active_object
####################################################################################################
def get_active_object():
    """Returns a reference to the active object in the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :return:
        A reference to the active object in the scene.
    """

    if nmv.utilities.is_blender_280():
        return bpy.context.active_object
    else:
        return bpy.context.scene.objects.active


####################################################################################################
# @link_object_to_scene
####################################################################################################
def link_object_to_scene(input_object):
    """Links a reconstructed object to the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param input_object:
        The given object that will be linked to the scene.
    """

    if nmv.utilities.is_blender_280():
        bpy.context.scene.collection.objects.link(input_object)
    else:
        bpy.context.scene.objects.link(input_object)


####################################################################################################
# @unlink_object_from_scene
####################################################################################################
def unlink_object_from_scene(scene_object):
    """Links a reconstructed object to the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param scene_object:
        A scene object to be unlinked from the scene.
    """

    if nmv.utilities.is_blender_280():
        bpy.context.scene.collection.objects.unlink(scene_object)
    else:
        bpy.context.scene.objects.unlink(scene_object)


####################################################################################################
# @hide_object
####################################################################################################
def hide_object(scene_object):
    """Hides a shown object in the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param scene_object:
        A given object to be seen.
    """

    if nmv.utilities.is_blender_280():
        scene_object.hide_viewport = True
    else:
        scene_object.hide = True


####################################################################################################
# @unhide_object
####################################################################################################
def unhide_object(scene_object):
    """Shows a hidden object in the scene.
    NOTE: This function makes the code compatible with Blender 2.7 and 2.8.

    :param scene_object:
        A given object to be shown.
    """

    if nmv.utilities.is_blender_280():
        scene_object.hide_viewport = False
    else:
        scene_object.hide = False


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
            select_object(scene_object)

            # Delete the object
            nmv.utilities.disable_std_output()
            bpy.ops.object.delete()
            nmv.utilities.enable_std_output()


####################################################################################################
# @clear_scene
####################################################################################################
def clear_scene():
    """Clear a scene and remove all the existing objects in it and unlink their references.

    NOTE: This function targets clearing meshes, curve, objects and materials.
    """

    for i_object in bpy.data.objects:
        i_object.hide_set(False)
        i_object.hide_select = False
        i_object.hide_viewport = False

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Unlink all the objects in all the layers
    for scene in bpy.data.scenes:
        for scene_object in scene.objects:
            nmv.utilities.disable_std_output()
            unlink_object_from_scene(scene_object)
            nmv.utilities.enable_std_output()

    # Select all the meshes, unlink them and clear their data
    for scene_mesh in bpy.data.meshes:
        nmv.utilities.disable_std_output()
        bpy.data.meshes.remove(scene_mesh, do_unlink=True)
        nmv.utilities.enable_std_output()

    # Select all the curves, unlink them and clear their data
    for scene_curve in bpy.data.curves:
        nmv.utilities.disable_std_output()
        bpy.data.curves.remove(scene_curve, do_unlink=True)
        nmv.utilities.enable_std_output()

    # Select all the scene objects, unlink them and clear their data
    for scene_object in bpy.data.objects:
        nmv.utilities.disable_std_output()
        bpy.data.objects.remove(scene_object, do_unlink=True)
        nmv.utilities.enable_std_output()

    # Select all the scene materials, unlink them and clear their data
    for scene_material in bpy.data.materials:
        nmv.utilities.disable_std_output()
        bpy.data.materials.remove(scene_material, do_unlink=True)
        nmv.utilities.enable_std_output()


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
            select_object(scene_object)

            # Delete the object
            nmv.utilities.disable_std_output()
            bpy.ops.object.delete()
            nmv.utilities.enable_std_output()

    # Select all the light, unlink them and clear their data
    if nmv.utilities.is_blender_280():
        for scene_lamp in bpy.data.lights:
            nmv.utilities.disable_std_output()
            bpy.data.lights.remove(scene_lamp, do_unlink=True)
            nmv.utilities.enable_std_output()

    else:
        for scene_lamp in bpy.data.lamps:
            nmv.utilities.disable_std_output()
            bpy.data.lamps.remove(scene_lamp, do_unlink=True)
            nmv.utilities.enable_std_output()


####################################################################################################
# @reset_scene
####################################################################################################
def reset_scene():
    """Resets the scene and does several operations that are needed to avoid any errors.
    """

    # Set all the objects in the scene to visible
    for scene_object in bpy.context.scene.objects:
        return
        # Switch to the object mode to avoid any errors if by default the editing mode was active
        #bpy.ops.object.mode_set(mode='OBJECT')

        # Un-hide any object in the scene to be able to delete all the objects
        #unhide_object(scene_object=scene_object)


####################################################################################################
# @select_all
####################################################################################################
def select_all():
    """Select all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to True.
    for scene_object in bpy.context.scene.objects:
        select_object(scene_object)


####################################################################################################
# @deselect_all
####################################################################################################
def deselect_all():
    """Deselect all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to False.
    for scene_object in bpy.context.scene.objects:
        deselect_object(scene_object)


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
        select_object(scene_object)


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
            select_object(scene_object)


####################################################################################################
# @get_object_by_name
####################################################################################################
def get_object_by_name(object_name):
    """Gets an object in the scene given its name.

    :param object_name:
        The name of object to be returned.
    """

    # Set the '.select' flag of the object to True
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            return scene_object


####################################################################################################
# @select_object_containing_string
####################################################################################################
def select_object_containing_string(search_string):
    """Select an object in the scene given part of its name.

    :param search_string:
        The name of first object that contains part of the given string.
    """

    # Set the '.select' flag of the object to True
    for scene_object in bpy.context.scene.objects:
        if search_string in scene_object.name:
            select_object(scene_object)


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
            deselect_object(scene_object)


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
            select_object(scene_object)


####################################################################################################
# @deselect_all_meshes_in_scene
####################################################################################################
def deselect_all_meshes_in_scene():
    """Deselect all the mesh objects (those of type 'MESH') in the scene.
    """

    # Select only the objects of type meshes
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            deselect_object(scene_object)


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
            select_object(scene_object)


####################################################################################################
# @deselect_all_curves_in_scene
####################################################################################################
def deselect_all_curves_in_scene():
    """Deselects all the curve objects (those of type 'CURVE') in the scene.
    """

    # Deselect only the objects of type curves
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            deselect_object(scene_object)


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
# @get_list_of_objects_in_scene
####################################################################################################
def get_list_of_objects_in_scene():
    """Return a list of references to all the objects in the scene.

    :return:
        A list of references to all the objects in the scene
    """

    # A list of all the objects in the scene
    object_list = list()

    # Simply add all the objects
    for scene_object in bpy.context.scene.objects:
        object_list.append(scene_object)

    # Return a reference to the list
    return object_list


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
    select_object(scene_object)

    # Delete the selected object
    nmv.utilities.disable_std_output()
    bpy.ops.object.delete(use_global=False)
    nmv.utilities.enable_std_output()


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
        select_object(scene_object)

        # Delete the selected object
        nmv.utilities.disable_std_output()
        bpy.ops.object.delete(use_global=False)
        nmv.utilities.enable_std_output()


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
        select_object(scene_object)

        nmv.utilities.disable_std_output()
        bpy.ops.object.delete(use_global=False)
        nmv.utilities.enable_std_output()


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
    select_object(scene_object)

    # Set it active
    if nmv.utilities.is_blender_280():
        bpy.context.view_layer.objects.active = scene_object
    else:
        bpy.context.scene.objects.active = scene_object

    # Return a reference to the mesh object again for convenience
    return scene_object


####################################################################################################
# @join_objects
####################################################################################################
def join_objects(scene_objects):
    """Joins a list of goven scene objects and return a reference to the resulting object.

    :param scene_objects:
        A list of the objects that need to be joined into a single element.
    :return:
        A reference to the resulting object.
    """

    # Make sure that the scene objects is not None
    if scene_objects is not None:

        # Make sure that it has at least a single element
        if len(scene_objects) == 0:
            return None

        elif len(scene_objects) == 0:
            return scene_objects[0]

        else:

            # Deselect all the objects in the scene
            deselect_all()

            # Set the first object to be the active object
            nmv.scene.set_active_object(scene_objects[0])

            # Select all the objects
            nmv.scene.select_objects(scene_objects)

            # Join all the objects in a single object
            bpy.ops.object.join()

            # Return a reference to the active object
            return scene_objects[0]


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
# @reset_orientation_of_objects
####################################################################################################
def reset_orientation_of_objects(scene_objects):
    """Reset the orientation of a group of objects in the scene.

    :param scene_objects:
        List of objects in the scene.
    """

    # Rotate all the objects as if they are a single object
    for scene_object in scene_objects:

        # Rotate the mesh object around the y axis
        scene_object.rotation_euler[1] = 0


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
# @translate_object
####################################################################################################
def translate_object(scene_object,
                     shift):
    """Set the given object a given location in the scene.

    :param scene_object:
        A given object in the scene to be translated.
    :param shift:
        A given shift to translate the object.
    """

    # Set location
    scene_object.location += shift


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
        deselect_object(scene_object)

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
        link_object_to_scene(duplicated_object)

        # Deselect all the objects in the scene
        for scene_object in bpy.context.scene.objects:
            deselect_object(scene_object)

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

    # Join all the mesh objects in a single object
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
    if nmv.utilities.is_blender_280():
        pass
    else:
        bpy.ops.view3d.viewnumpad(type='TOP')

    # View all the objects in the scene
    bpy.ops.view3d.view_all()

    # Update the end
    bpy.context.space_data.clip_end = 1e5


####################################################################################################
# @view_region
####################################################################################################
def view_region(x=0, y=0, delta=1):
    """View a specific region in the scene.

    :param x:
        Minimum X.
    :param y:
        Minimum Y.
    :param delta:
        Delta
    """
    bpy.ops.view3d.zoom(mx=x, my=y, delta=delta)

    # Update the end
    bpy.context.space_data.clip_end = 1e5


####################################################################################################
# @activate_neuromorphovis_mode
####################################################################################################
def activate_neuromorphovis_mode():
    """Switches the scene to black to make it easy to see the morphologies.
    """

    if nmv.utilities.is_blender_280():
        theme = bpy.context.preferences.themes['Default']
        # theme.view_3d.space.gradients.high_gradient = Vector((0, 0, 0))
        # theme.view_3d.space.gradients.gradient = Vector((0, 0, 0))
        # theme.view_3d.grid = Vector((0, 0, 0, 0))


####################################################################################################
# @deactivate_neuromorphovis_mode
####################################################################################################
def deactivate_neuromorphovis_mode():
    """Switches the scene the default theme.
    """

    if nmv.utilities.is_blender_280():
        bpy.ops.preferences.reset_default_theme()


####################################################################################################
# @set_scene_transparency
####################################################################################################
def set_scene_transparency(transparent=False):
    """Enables or disables scene transparency.

    :param transparent:
        If True, switch to the transparent mode, otherwise normal mode.
    """

    if nmv.utilities.is_blender_280():
        views3d = [a for a in bpy.context.screen.areas if a.type == 'VIEW_3D']
        for a in views3d:
            shading = a.spaces.active.shading
            shading.show_xray = transparent


####################################################################################################
# @switch_scene_shading
####################################################################################################
def switch_scene_shading(shading_type='SOLID'):
    """Switches the scene panel to the given shading type

    :param shading_type:
        One of the following:  'WIREFRAME' '(SOLID)' 'MATERIAL' 'RENDERED'
    """

    if nmv.utilities.is_blender_280():
        areas = bpy.context.workspace.screens[0].areas
        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = shading_type


####################################################################################################
# @switch_interface_to_edit_mode
####################################################################################################
def switch_interface_to_edit_mode():
    """Switch the user interface to the edit mode style.
    """

    if nmv.utilities.is_blender_280():

        # Update the transparency
        set_scene_transparency(True)

        # Use the solid mode
        nmv.scene.switch_scene_shading('SOLID')

        # Increase the vertex size
        bpy.context.preferences.themes['Default'].view_3d.vertex_size = 8

        # Make the vertex red
        bpy.context.preferences.themes['Default'].view_3d.vertex.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.b = 0.0

        # Make the selected vertex white
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.g = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.b = 1.0

        # Make the wire white to be able to see it
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.g = 1.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.b = 1.0


####################################################################################################
# @switch_interface_to_visualization_mode
####################################################################################################
def switch_interface_to_visualization_mode():
    """Switches the user interface to the visualization mode style.
    """

    if nmv.utilities.is_blender_280():

        # Update the transparency
        set_scene_transparency(False)

        # Solid mode
        switch_scene_shading('SOLID')

        # Make the vertex black again
        bpy.context.preferences.themes['Default'].view_3d.vertex.r = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.b = 0.0

        # Adjust the vertex size to the default value
        bpy.context.preferences.themes['Default'].view_3d.vertex_size = 3

        # Make the wire black again
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.r = 0.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.b = 0.0
