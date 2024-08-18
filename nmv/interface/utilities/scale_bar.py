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

# System imports
import math

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.skeleton
import nmv.bbox
import nmv.consts
import nmv.shading
import nmv.scene
import nmv.enums
import nmv.utilities
import nmv.mesh
import nmv.geometry

from .text import *


####################################################################################################
# @get_user_friendly_scale_bar_length
####################################################################################################
def get_user_friendly_scale_bar_length(view_length):
    """Scale bars must be in a human-readable format. To obtain a human-readable or user-friendly
    value, we limit the options to numbers like 5, 10, 20, 25, 50, 100, 150, 200 um, etc...

    :param view_length:
        The current view size as calculated from the bounding box of the objects located in
        the scene.
    :return:
        The scale bar length in a human-readable form.
    """

    if view_length < 50:
        return 5
    elif view_length < 150:
        return 10
    elif view_length < 250:
        return 20
    elif view_length < 500:
        return 25
    elif view_length < 1000:
        return 50
    elif view_length < 2000:
        return 100
    else:
        return 150


####################################################################################################
# @get_scale_bar_length
####################################################################################################
def get_scale_bar_length(bounding_box,
                         view=nmv.enums.Camera.View.FRONT):
    """Gets the length of the scale bar depending on the content in the scene.

    :param bounding_box:
        The bounding box of the objects that we need to create a scale bar for,
    :param view:
        The camera view [nmv.enums.Camera.View:FRONT, SIDE or TOP]
    :return:
        The scale bar length.
    """

    # For front and side views, always use the height to maintain the relationships
    if view == nmv.enums.Camera.View.FRONT or view == nmv.enums.Camera.View.SIDE:
        return get_user_friendly_scale_bar_length(view_length=bounding_box.bounds[1])

    # For the top view, use the depth 
    else:
        return get_user_friendly_scale_bar_length(view_length=bounding_box.bounds[2])


####################################################################################################
# @draw_scale_bar_segment
####################################################################################################
def draw_scale_bar_segment():
    """Creates the scale bar segment object.

    :return:
        A reference to the created scale bar segment that this segment is located at the origin.
    """

    # Create a bevel object to build the segments, and delete it later
    bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, resolution=16, name='scale_bar_bevel')

    # Vertical segment
    p0 = Vector((0, 0, 0))
    p1 = Vector((0, 1, 0))
    p2 = Vector((0, -1, 0))
    vertical_segment = nmv.scene.convert_object_to_mesh(
        scene_object=nmv.geometry.draw_cone_line(
            point1=p1, point2=p2,
            point1_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            point2_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            bevel_object=bevel_object))

    # Top horizontal segment
    p3 = p1 - Vector((nmv.consts.Geometry.SCALE_BAR_NEGATIVE_SHIFT, 0, 0))
    p4 = p1 + Vector((nmv.consts.Geometry.SCALE_BAR_MAIN_EDGE_SIZE, 0, 0))
    top_segment = nmv.scene.convert_object_to_mesh(
        scene_object=nmv.geometry.draw_cone_line(
            point1=p3, point2=p4,
            point1_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            point2_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            bevel_object=bevel_object))

    # Bottom horizontal segment
    p5 = p2 - Vector((nmv.consts.Geometry.SCALE_BAR_NEGATIVE_SHIFT, 0, 0))
    p6 = p2 + Vector((nmv.consts.Geometry.SCALE_BAR_MAIN_EDGE_SIZE, 0, 0))
    bottom_segment = nmv.scene.convert_object_to_mesh(
        scene_object=nmv.geometry.draw_cone_line(
            point1=p5, point2=p6,
            point1_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            point2_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            bevel_object=bevel_object))

    # Center horizontal segment
    p7 = p0 + Vector((nmv.consts.Geometry.SCALE_BAR_CENTER_EDGE_SIZE, 0, 0))
    center_segment = nmv.scene.convert_object_to_mesh(
        scene_object=nmv.geometry.draw_cone_line(
            point1=p0, point2=p7,
            point1_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            point2_radius=nmv.consts.Geometry.SCALE_BAR_THICKNESS,
            bevel_object=bevel_object))

    # Delete the bevel object, since we converted all the segments into meshes
    nmv.scene.delete_object_in_scene(bevel_object)

    # Join all the scale bar segments into a single object 
    scale_bar_object = nmv.mesh.join_mesh_objects(
        mesh_list=[vertical_segment, top_segment, bottom_segment, center_segment],
        name='Scale Bar Segment')

    # Return a reference to the scale bar segment object 
    return scale_bar_object 


####################################################################################################
# @create_default_scale_bar_legend
####################################################################################################
def create_default_scale_bar_legend(scale_bar_length,
                                    material_type,
                                    color=nmv.consts.Color.BLACK):
    """Creates a default scale bar legend that is located at the origin.

    :param scale_bar_length:
        The length of the scale bar in microns.
    :param material_type:
        The type of the material that will be assigned to the scale bar.
    :param color:
        The color of the scale bar legend, by default BLACK.
    :return:
        A reference to the created scale bar object.
    """

    # Draw the scale bar segment (in the XY plane)
    scale_bar_segment = draw_scale_bar_segment()

    # Draw the scale bar value as a text object (in the XY plane) and convert it to a mesh
    value_text_object = nmv.scene.convert_object_to_mesh(
        create_text_object(text_string='%d \u03BCm' % int(scale_bar_length), name='Value'))

    # Scale the text value a little (0.7 of the size to fall within the segment)
    nmv.scene.scale_object_uniformly(scene_object=value_text_object, scale_factor=0.7)

    # Rotate the text object 
    nmv.scene.rotate_object(scene_object=value_text_object, z=math.radians(90))

    # Shift the text object 
    nmv.scene.translate_object(scene_object=value_text_object, shift=Vector((0.5, 0, 0)))

    # Group all objects to result in a single mesh 
    scale_bar_legend = nmv.mesh.join_mesh_objects(
        mesh_list=[scale_bar_segment, value_text_object], name='Scale Bar Legend')

    # Assign the materials to the scale bar and the font object
    material = nmv.skeleton.create_single_material(
        name='scale_bar_legend', material_type=material_type, color=color)
    nmv.shading.set_material_to_object(mesh_object=scale_bar_legend, material_reference=material)

    # Return a reference to the scale bar legend 
    return scale_bar_legend


####################################################################################################
# @adjust_scale_bar_legend
####################################################################################################
def adjust_scale_bar_legend(legend,
                            bounding_box, 
                            view):
    """Adjusts the rotation and size of the scale bar legend depending on the projection
    and bounding box of the scene.

    :param legend:
        A reference to the scale bar legend.
    :param bounding_box:
        The frustum that will be rendered.
    :param view:
        The camera view [nmv.enums.Camera.View:FRONT, SIDE or TOP]
    :return:
    """

    # Top view  
    if view == nmv.enums.Camera.View.TOP: 

        # Rotate the legend 
        nmv.scene.rotate_object(scene_object=legend, x=math.radians(90), y=0)

        # Calculate the legend position
        x = bounding_box.p_min[0] + 0.05 * bounding_box.bounds[0] 
        y = bounding_box.p_min[1]
        z = bounding_box.p_min[2] + 0.20 * bounding_box.bounds[2]
        legend_position = Vector((x, y, z)) 

    # Side view 
    elif view == nmv.enums.Camera.View.SIDE:
        
        # Rotate the legend 
        nmv.scene.rotate_object(
            scene_object=legend, x=math.radians(90), y=-math.radians(90), z=-math.radians(90))

        # Calculate the legend position
        x = bounding_box.p_min[0]
        y = bounding_box.p_min[1] + 0.20 * bounding_box.bounds[1]
        z = bounding_box.p_min[2] + 0.05 * bounding_box.bounds[2] 
        legend_position = Vector((x, y, z))

    # The default legend is already created in the front view or the XY plane
    else:
        
        # Calculate the legend position
        x = bounding_box.p_min[0] + 0.05 * bounding_box.bounds[0]
        y = bounding_box.p_min[1] + 0.20 * bounding_box.bounds[1]
        z = bounding_box.p_max[2]
        legend_position = Vector((x, y, z))

    # Translate the legend 
    nmv.scene.set_object_location(legend, legend_position)

    # Return a reference to the adjusted legend 
    return legend


####################################################################################################
# @draw_scale_bar
####################################################################################################
def draw_scale_bar(bounding_box,
                   view,
                   material_type):
    """Draws a scale bar in the rendered image.

    :param bounding_box:
        The frustum that will be rendered.
    :param view:
        The camera view [nmv.enums.Camera.View:FRONT, SIDE or TOP]
    :param material_type:
        The material type used to shade the scale bar.
    :return:
        A reference to the created scale bar
    """

    # Make sure that the fonts are loaded to be able to draw the text correctly
    nmv.interface.load_fonts()

    # Get the scale bar length based on the bounding box of the scene to be rendered
    scale_bar_length = get_scale_bar_length(bounding_box=bounding_box, view=view)

    # Create the default scale bar legend at the XY plane 
    scale_bar_legend = create_default_scale_bar_legend(
        scale_bar_length=scale_bar_length, material_type=material_type)
    
    # Scale the size of the scale bar 
    scale_factor = scale_bar_length / scale_bar_legend.dimensions.y
    nmv.scene.scale_object_uniformly(scene_object=scale_bar_legend, scale_factor=scale_factor)

    # Adjust the scale bar legend depending on the view 
    return adjust_scale_bar_legend(legend=scale_bar_legend, bounding_box=bounding_box, view=view)
